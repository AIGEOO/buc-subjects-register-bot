import os, time

from dotenv import load_dotenv
from termcolor import cprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.support.ui import Select // check about it

load_dotenv()

class RegisterationActions:
    def __init__(self) -> None:
        self.username = os.getenv('STUDENT_USERNAME')
        self.password = os.getenv('STUDENT_PASSWORD')
        self.is_logged_in = False
        self.choosen_subjects = []

    # initializing chrome drivers
    def init_chrome_driver(self) -> None:
        """"Initializing chrome drivers"""
        # If there is no instance create one
        try:
            # Creating chrome options
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            chrome_options = webdriver.ChromeOptions()

            prefs = {"profile.managed_default_content_settings.images": 2,
                        "profile.default_content_settings.images": 2}

            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--log-level=OFF')
            chrome_options.add_argument('--disable-extensions')

            # , options=chrome_options
            self.chrome_driver = webdriver.Chrome(executable_path=os.getenv('CHROME_DRIVER_PATH'))
        except Exception as e:
            raise ConnectionError("Couldn't init chrome drivers" + str(e))

    def login(self) -> None:
        self.chrome_driver.get('http://sisweb.buc.edu.om/portal/pls/portal/logsisw.cow_start')
        time.sleep(5)

        cprint("Start Log in process...", "yellow")
        choose_student_button = self.chrome_driver.find_element_by_xpath("/html/body/table[7]/tbody/tr/td[3]/p/a")
        choose_student_button.click()
        time.sleep(5)

        try:
            username = self.chrome_driver.find_element_by_xpath('//input[@name="ssousername"]')
            username.clear()
            username.send_keys(self.username)

            password = self.chrome_driver.find_element_by_xpath("//input[@name='password']")
            password.clear()
            password.send_keys(self.password)

            password.send_keys(keys.Keys.RETURN)
        except NoSuchElementException as e:
            cprint("username & password inputs field does not exsist!")

        cprint("Login process finished :)", "green")

    def logout(self) -> None:
        cprint("Start Logout Process...", "yellow")

        logout_link = self.chrome_driver.find_element_by_xpath('//table[@class="stu_header"]/tbody/tr[1]/td[2]/a')
        logout_link.click()

        cprint("Logout process finished successfully :)", "green")
        self.chrome_driver.quit()

    def redirect_to_register_page(self) -> None:

        cprint("redirect to registeration page...", "blue")

        register_in_courses_link = self.chrome_driver.find_element_by_xpath("//ul[@id='registration']/li[3]/a").get_attribute('href')
        self.chrome_driver.get(register_in_courses_link)

    def list_subjects(self) -> list:

        cprint("Listing available courses...", "yellow")

        available_courses_array = []
        
        try:
            for i in range(2, 30):
                available_courses = self.chrome_driver.find_element_by_xpath(f'//select[@name="Add_Crs"]/option[{i}]')

                available_courses_array.append((f'{i}', available_courses.get_attribute('value'), available_courses.text))
        except Exception as e:
            pass

        for i in range(len(available_courses_array)):
            print(f'{available_courses_array[i][0]}. ', available_courses_array[i][2])
            pass

        return available_courses_array

    def register_in_courses(self, available_courses):
        
        input_field = input("Please Enter Subjects Numbers: e.g. 1, 14, 3 \n")

        choosen_subjects_id = input_field.split(', ')

        add_btn = self.chrome_driver.find_element_by_xpath("//input[@name='ADD'][1]")

        submit_btn = self.chrome_driver.find_element_by_xpath('//input[@name="CUST_BUT4"]')

        for i in range(len(choosen_subjects_id)):
            for x in range(len(available_courses)):
                if choosen_subjects_id[i] == available_courses[x][0]:

                    self.chrome_driver.find_element_by_xpath(f'//option[@value="{available_courses[x][1]}"]').click()

                    add_btn.click()

                    self.choosen_subjects.append(available_courses[x][1])
        # submit_btn.click()
        cprint("Subjects Registred Successfully :)", "green")

    def start(self) -> None:
        self.init_chrome_driver()
        self.login()
        time.sleep(5)
        self.redirect_to_register_page()
        time.sleep(5)
        self.register_in_courses(self.list_subjects())
        time.sleep(5)
        self.logout()

        cprint("Thank you for using my tool ;)", "red")