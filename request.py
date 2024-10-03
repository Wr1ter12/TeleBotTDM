class Requests:
    def __init__(self, bot, db, menu):
        self.bot = bot
        self.db = db
        self.menu = menu
    
    def request(self, message):
        msg = self.bot.reply_to(message, "Пожалуйста, введите ваше имя.")
        return msg

    def userName(self, message):
        name = message.text
        print(name)
        self.menu.showMainMenu(message)
