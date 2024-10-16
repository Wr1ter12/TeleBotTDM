from asyncio import run
from re import match

productsMsg = '''Категория продукции: 
1.1 Игровые комплексы
1.2 МАФы
1.3 Профнастил
1.4 Штакетник металлический
1.5 Металлоконструкции
1.6 Изготовление под заказ
    1.6.1 Перфорация листов
    1.6.2 Фасадные кассеты'''

servicesMsg = '''
Виды услуг:
◦ 1.1 Сварочные работы с черным, цветным металлом
        1.1.1 Дуговая сварка 
        1.1.2 Сварка в защитных средах
        1.1.3 Контактная сварка
◦ 1.2 Изготовление металлоконструкций
        (Надежные конструкции для строительства,
        благоустройства территорий, возведения
        промышленных и дорожных сооружений.)
◦ 1.3 Покраска
        1.3.1 Порошковое покрытие
        1.3.2 Декоративное покрытие
        1.3.3 Цинкование
◦ 1.4 Ленточнопильная резка металла до 300 мм
◦ 1.5 Сверление
        1.5.1 Спиральное сверление
        1.5.2 Корончатое сверление
        1.5.3 Термическое сверление
        1.5.4 Зенкование
        1.5.5 Нарезание резьбы
◦ 1.6 Гибка металла
        1.6.1 Cоздание разнопольных уголков, профилей
        1.6.2 Гибка профильных труб, круглых труб
        1.6.3 Вальцевание листового металла, в том числе конусное 
◦ 1.7 Лазерная резка листового металла
        1.7.1 Перфорирование
        1.7.2 Художественная резка
        1.7.3 Резка по размерам
        (Толщина обрабатываемого
        материала от 1мм до 10мм.)
◦ 1.8 Лазерная резка труб и профилей
        (Перфорирование, резка по параметрам.)
◦ 1.9 Дополнительные услуги
        1.9.1 Разработка и/или доработка разверток
        1.9.2 Разработка и доработка конструкторской
        документации по Вашим эскизам,
        чертежам и ТЗ (техническим заданиям)'''

class Requests:
    def __init__(self, bot, db, menu, main, chatID):
        self.bot = bot
        self.db = db
        self.menu = menu
        self.Main = main
        self.usrEmail = " "
        self.usrPhone = " "
        self.usrName = " "
        self.usrClient = " "
        self.usrChoice = " "
        self.usrNeedPack = " "
        self.usrSendToPlace = " "
        self.usrSendDate = " "
        self.usrWishes = " "
        self.chatID = chatID

    def request(self, message):
        msg = self.bot.reply_to(message, "Пожалуйста, введите ваше имя.")
        return msg
    
    def userName(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Некорректный формат!")
            self.request(message)
            return
        self.usrName = message.text
        self.Main.handleOrderCall(message)
        self.bot.register_next_step_handler(message, self.Main.handleRequestSec)

    def userPhoneNumber(self, message):
        if message.text == None:
            self.usrPhone = message.contact.phone_number
        else:    
            self.usrPhone = message.text
        if match(r'^\+?[1-9]\d{1,14}$', self.usrPhone) and len(self.usrPhone)>=7 and len(self.usrPhone)<=15: 
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат номера телефона!")
            self.Main.handleOrderCall(message)
            self.bot.register_next_step_handler(message, self.Main.handleRequestSec)

    def userEmail(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат почты!")
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)
            return
        if '@' in message.text:
            self.usrEmail = message.text
            msg = self.bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestForth)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат почты!")
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)

    def intProd(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            msg = self.bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestForth)
            return
        if message.text.lower() == "да":
            self.usrClient = "Да"
        elif message.text.lower() == "нет":
            self.usrClient = "Нет"
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            msg = self.bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestForth)
            return
        msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
        self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def productsSelection(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Некорректный формат ответа!")
            msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)
        msg = message.text
        if msg.lower() == "продукция":
            self.bot.send_message(message.chat.id, productsMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории продукции:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestProductsCategories)
        elif msg.lower() == "услуга":
            self.bot.send_message(message.chat.id, servicesMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории услуги:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestTypeOfServices)
        else:
            self.bot.send_message(message.chat.id, "Некорректный выбор!")
            msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def typeOfServices(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, servicesMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории услуги:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestTypeOfServices)
            return
        
        self.usrChoice = "Услуга: " + message.text

        self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes)

    def productsCategories(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, productsMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории продукции:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestProductsCategories)
            return
        
        self.usrChoice = "Категория продукции: " + message.text
            
        self.bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedPacking)

    def needPacking(self,message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedPacking)
            return
        if message.text.lower() == "да":
            self.usrNeedPack = "Да"
        elif message.text.lower() == "нет":
            self.usrNeedPack = "Нет"
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedPacking)
            return
        self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)

    def needSend(self,message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)
            return
        if message.text.lower() == "да":
            self.bot.send_message(message.chat.id, "Введите адрес доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendAddress)
        elif message.text.lower() == "нет":
            self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)

    def sendAddress(self, message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Введите адрес доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendAddress)
            return
        self.usrSendToPlace = message.text
        self.bot.send_message(message.chat.id, "Введите дату доставки:")
        self.bot.register_next_step_handler(message, self.Main.handleRequestSendDate)

    def sendDate(self,message):
        if message.text == None:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Введите дату доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendDate)
            return
        self.usrSendDate = message.text
        self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes)

    def saveWishes(self, message):
        if message.text != None:
            self.usrWishes = message.text
        run(self.db.requestDb(self.usrName, self.usrEmail, self.usrPhone, self.usrClient, self.usrChoice, self.usrNeedPack, self.usrSendToPlace, self.usrSendDate, self.usrWishes))
        self.bot.send_message(self.chatID, f"Новая заявка от пользователя {message.from_user.first_name}")
        self.Main.users[str(message.from_user.username)][0] = False
        self.menu.showMainMenu(message)

