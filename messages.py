infoMsg = """
Контакты:

Телефон: +7 (495) 927 95 17, +7 (925) 616 29 00
Сайт: <a href="https://tdmmag.ru">tdmmag.ru</a> 
Адрес: Москва, ул.1-я Мытищинская, 28 c1
"""

class Messages:
    def __init__(self, bot):
        self.bot = bot
        
    def start(self, message):
        self.bot.send_message(message.chat.id, "Здравствуйте, бот готов к работе!")

    def info(self, message):
        self.bot.send_message(
            message.chat.id,
            infoMsg,
            parse_mode='HTML'
        )

    def help(self, message):
        self.bot.send_message(message.chat.id, "Помощь в пользовании ботом")

    def usr_msg(self, message):
        print("[log] Текстовое сообщение: " + message.text)
