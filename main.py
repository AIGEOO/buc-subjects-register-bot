from core.RegisterationActions import RegisterationActions

if __name__ == "__main__":
    try:
        bot = RegisterationActions()
        bot.start()
    except Exception as e:
        print(e)