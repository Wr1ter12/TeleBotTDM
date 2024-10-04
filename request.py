class Requests:
    def __init__(self, bot, db, menu, main):
        self.bot = bot
        self.db = db
        self.menu = menu
        self.Main = main
        self.usrEmail = " "
        self.usrPhone = " "
        self.usrName = " "
        self.usrClient = " "

    def msgStr(self, message):
        return message.text()
    
    def request(self, message):
        msg = self.bot.reply_to(message, "Пожалуйста, введите ваше имя.")
        return msg

    def userName(self, message):
        self.usrName = message.text
        msg = self.bot.reply_to(message, "Введите ваш номер телефона.")
        self.Main.handleOrderCall(message)
        self.bot.register_next_step_handler(msg, self.Main.handleRequestSec)

    def userPhoneNumber(self, message):
        if message.text == None:
            self.usrPhone = message.contact.phone_number
        else:    
            self.usrPhone = message.text
        msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
        self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)

    def userEmail(self, message):
        self.usrEmail = message.text
        msg = self.bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)")
        self.bot.register_next_step_handler(msg, self.Main.handleRequestForth)

    def intProd(self, message):
        if message.text.lower() == "да":
            self.usrClient = "Да"
        else:
            self.usrClient = "Нет"
        msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?")
        self.db.requestDb(self.usrName, self.usrEmail, self.usrPhone, self.usrClient)
        self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def productsSelection(self,message):
        pass
        '''msg = message.text.lower()
        #print(msg)
        if msg == "продукция":
            self.bot.send_message("Категория продукции")
        elif msg == "услуга":
            self.bot.send_message("Виды услуг")
        else:
            self.bot.send_message("что то пошло не по плану")'''
