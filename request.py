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
    
    def userName(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Некорректный формат!")
            self.request(message)
            return
        self.usrName = message.text
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.Main.handleOrderCall(message)
        self.bot.register_next_step_handler(message, self.Main.handleRequestSec)

    def userPhoneNumber(self, message, save):
        if message.content_type == 'text' or message.content_type == 'contact':
            if message.content_type == 'contact':
                self.usrPhone = message.contact.phone_number
            elif message.content_type == 'text':    
                self.usrPhone = message.text
            if match(r'^\+?[1-9]\d{1,14}$', self.usrPhone) and len(self.usrPhone)>=11 and len(self.usrPhone)<=12:
                if self.usrPhone.startswith("8") or self.usrPhone.startswith("7") or self.usrPhone.startswith("+7"):
                    if save == True:
                        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
                        return
                    msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
                    self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)
                else:
                    self.usrPhone = " "
                    self.bot.send_message(message.chat.id, "Неправильный формат номера телефона!")
                    self.Main.handleOrderCall(message)
                    self.bot.register_next_step_handler(message, self.Main.handleRequestSec)
            else:
                self.usrPhone = " "
                self.bot.send_message(message.chat.id, "Неправильный формат номера телефона!")
                self.Main.handleOrderCall(message)
                self.bot.register_next_step_handler(message, self.Main.handleRequestSec)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат номера телефона!")
            self.Main.handleOrderCall(message)
            self.bot.register_next_step_handler(message, self.Main.handleRequestSec)
                
    def userEmail(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат почты!")
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)
            return
        if match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", message.text):
            self.usrEmail = message.text
            if save == True:
                self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
                return
            msg = self.bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestForth)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат почты!")
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)

    def intProd(self, message, save):
        if message.content_type != 'text':
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
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
        self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def productsSelection(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Некорректный формат ответа!")
            msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)
        msg = message.text
        if msg.lower() == "продукция":
            self.bot.send_message(message.chat.id, productsMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории продукции:", reply_markup=self.menu.pKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestProductsCategories)
        elif msg.lower() == "услуга":
            self.bot.send_message(message.chat.id, servicesMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории услуги:", reply_markup=self.menu.sKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestTypeOfServices)
        else:
            self.bot.send_message(message.chat.id, "Некорректный выбор!")
            msg = self.bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=self.menu.PSKeyboard)
            self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def typeOfServices(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, servicesMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории услуги:", reply_markup=self.menu.sKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestTypeOfServices)
            return
        
        self.usrChoice = "Услуга: " + message.text
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, False)

    def productsCategories(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, productsMsg)
            self.bot.send_message(message.chat.id, "Введите номер категории продукции:", reply_markup=self.menu.pKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestProductsCategories)
            return
        
        self.usrChoice = "Категория продукции: " + message.text
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedPacking)

    def needPacking(self,message,save):
        if message.content_type != 'text':
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
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)

    def needSend(self,message,save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)
            return
        if message.text.lower() == "да":
            self.bot.send_message(message.chat.id, "Введите адрес доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendAddress)
        elif message.text.lower() == "нет":
            if save == True:
                self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
                return
            self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)

    def sendAddress(self, message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Введите адрес доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendAddress)
            return
        self.usrSendToPlace = message.text
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.bot.send_message(message.chat.id, "Введите дату доставки:")
        self.bot.register_next_step_handler(message, self.Main.handleRequestSendDate)

    def sendDate(self,message, save):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Введите дату доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendDate)
            return
        self.usrSendDate = message.text
        if save == True:
            self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, True)
            return
        self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes, False)

    def saveWishes(self, message, saving):
        if saving == False:
            if message.content_type == 'text':
                self.usrWishes = message.text
            else:
                self.usrWishes = ""
        if self.usrName == " " or self.usrEmail == " " or self.usrPhone == " ":
            self.bot.send_message(message.chat.id, "Не все обязательные поля заполнены! Переоформите заявку!")
            return
        if self.usrNeedPack == " ":
            self.bot.send_message(message.chat.id, "Имя: " + self.usrName + "\nТелефон: " + self.usrPhone + "\nПочта: " + self.usrEmail + "\nКлиент: " + self.usrClient + "\n" + self.usrChoice + "\nКомментарии: " + self.usrWishes)
        else:
            if self.usrSendToPlace == " ":
                self.bot.send_message(message.chat.id, "Имя: " + self.usrName + "\nТелефон: " + self.usrPhone + "\nПочта: " + self.usrEmail + "\nКлиент: " + self.usrClient + "\n" + self.usrChoice + "\nУпаковка: " + self.usrNeedPack + "\nКомментарии: " + self.usrWishes)
            else:
                self.bot.send_message(message.chat.id, "Имя: " + self.usrName + "\nТелефон: " + self.usrPhone + "\nПочта: " + self.usrEmail + "\nКлиент: " + self.usrClient + "\n" + self.usrChoice + "\nУпаковка: " + self.usrNeedPack + "\nАдрес Доставки: " + self.usrSendToPlace + "\nДата доставки: " + self.usrSendDate + "\nКомментарии: " + self.usrWishes)
        self.bot.send_message(message.chat.id, "Вы подтверждаете отправку заявки? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
        self.bot.register_next_step_handler(message, self.Main.handleRequestConfirmation)
        
    def saveRequest(self, message):
        if message.content_type != 'text':
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Вы подтверждаете отправку заявки? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestConfirmation)
            return
        if message.text.lower() == "да":
            self.db.requestDb(self.usrName, self.usrEmail, self.usrPhone, self.usrClient, self.usrChoice, self.usrNeedPack, self.usrSendToPlace, self.usrSendDate, self.usrWishes)
            self.bot.send_message(message.chat.id, "Заявка успешно сохранена! Благодарим за сотрудничество!")
            self.bot.send_message(self.chatID, f"Новая заявка от пользователя {message.from_user.first_name}")
            self.Main.users[str(message.from_user.username)][0] = False
            self.menu.showMainMenu(message)
        elif message.text.lower() == "нет":
            if self.usrNeedPack == " ":
                self.bot.send_message(message.chat.id, "Введите номер поля для изменения:", reply_markup=self.menu.rsKeyboard)
            else:
                if self.usrSendToPlace == " ":
                    self.bot.send_message(message.chat.id, "Введите номер поля для изменения:", reply_markup=self.menu.rpKeyboard)
                else:
                    self.bot.send_message(message.chat.id, "Введите номер поля для изменения:", reply_markup=self.menu.rpsKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestModification)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат ответа!")
            self.bot.send_message(message.chat.id, "Вы подтверждаете отправку заявки? (Да/Нет)", reply_markup=self.menu.YNKeyboard)
            self.bot.register_next_step_handler(message, self.Main.handleRequestConfirmation)
