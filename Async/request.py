from asyncio import run

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
◦ Сварочные работы с черным, цветным металлом
        (дуговая сварка, 
        сварка в защитных средах,
        контактная сварка)
◦ Изготовление металлоконструкций
        Надежные конструкции для строительства,
        благоустройства территорий, возведения
        промышленных и дорожных сооружений.
◦ Покраска
        Мы предлагаем несколько видов покраски
        - порошковое покрытие, декоративное
        покрытие, цинкование.
◦ Ленточнопильная резка металла до 300 мм
◦ Сверление
        (Спиральное сверление,
        корончатое сверление,
        термическое сверление, зенкование,
        нарезание резьбы)
◦ Гибка металла
        Cоздание разнопольных уголков, профилей.
        Гибка профильных труб, круглых труб,
        Вальцевание листового металла,
        в том числе конусное. 
◦ Лазерная резка листового металла
        Перфорирование, художественная резка,
        резка по размерам
        толщина обрабатываемого
        материала от 1мм до 10мм.
◦ Лазерная резка труб и профилей
        Перфорирование, резка по параметрам.
◦ Дополнительные услуги
        Разработка и/или доработка разверток,
        разработка и доработка конструкторской
        документации по Вашим эскизам,
        чертежам и ТЗ (техническим заданиям).'''

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
        self.usrChoice = " "
        self.usrNeedPack = " "
        self.usrSendToPlace = " "
        self.usrSendDate = " "
        self.usrWishes = " "
        self.usrReference = " "

    def request(self, message):
        msg = self.bot.reply_to(message, "Пожалуйста, введите ваше имя.")
        return msg

    def userName(self, message):
        self.usrName = message.text
        self.Main.handleOrderCall(message)
        self.bot.register_next_step_handler(message, self.Main.handleRequestSec)

    def userPhoneNumber(self, message):
        if message.text == None:
            self.usrPhone = message.contact.phone_number
        else:    
            self.usrPhone = message.text
        from re import match
        if match(r'^\+?[1-9]\d{1,14}$', self.usrPhone) and len(self.usrPhone)>=7 and len(self.usrPhone)<=15: 
            msg = self.bot.reply_to(message, "Введите ваш адрес электронной почты.")
            self.bot.register_next_step_handler(msg, self.Main.handleRequestThr)
        else:
            self.bot.send_message(message.chat.id, "Неправильный формат номера телефона!")
            
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
        self.bot.register_next_step_handler(msg, self.Main.handleRequestFifth)

    def productsSelection(self, message):
        msg = message.text
        if msg.lower() == "продукция":
            self.bot.send_message(message.chat.id, productsMsg)
            self.bot.register_next_step_handler(message, self.Main.handleRequestProductsCategories)
        elif msg.lower() == "услуга":
            self.bot.send_message(message.chat.id, servicesMsg)
            self.bot.register_next_step_handler(message, self.Main.handleRequestTypeOfServices)

        else:
            self.bot.send_message(message.chat.id, "Некорректный выбор!")

    def typeOfServices(self, message):
        self.usrChoice = "Услуга: " + message.text

        self.bot.send_message(message.chat.id, "Хотите загрузить какой-либо файл? Например, техническую документацию или чертеж?")
        self.bot.register_next_step_handler(message, self.Main.handleRequestSendToObj)
       
    def productsCategories(self, message):
        self.usrChoice = "Категория продукции: " + message.text
        
        self.bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)")
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedPacking)

    def needPacking(self,message):
        self.usrNeedPack = message.text
        self.bot.send_message(message.chat.id, "Нужна ли доставка на объект? (Да/Нет)")
        self.bot.register_next_step_handler(message, self.Main.handleRequestNeedSend)

    def needSend(self,message):
        if message.text.lower() == "да":
            self.bot.send_message(message.chat.id, "Введите адрес доставки:")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendAddress)
        else:
            self.bot.send_message(message.chat.id, "Хотите загрузить какой-либо файл? Например, техническую документацию или чертеж?")
            self.bot.register_next_step_handler(message, self.Main.handleRequestSendToObj)

    def sendAddress(self, message):
        self.usrSendToPlace = message.text
        self.bot.send_message(message.chat.id, "Введите дату доставки:")
        self.bot.register_next_step_handler(message, self.Main.handleRequestSendDate)

    def sendDate(self,message):
        self.usrSendDate = message.text
        self.bot.send_message(message.chat.id, "Хотите загрузить какой-либо файл? Например, техническую документацию или чертеж?")
        self.bot.register_next_step_handler(message, self.Main.handleRequestSendToObj)

    def saveFile(self,message):
        try:
            if message.text == None:
                if message.document != None:
                    fileInfo = self.bot.get_file(message.document.file_id)
                    downloadedFile = self.bot.download_file(fileInfo.file_path)

                    src = self.Main.currentDir + '\\ДокументыПользователей\\' + message.document.file_name;
                    with open(src, 'wb') as new_file:
                        new_file.write(downloadedFile)
                else:
                    fileInfo = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
                    downloadedFile = self.bot.download_file(fileInfo.file_path)

                    src = self.Main.currentDir + '\\ДокументыПользователей\\' + fileInfo.file_path
                    with open(src, 'wb') as new_file:
                        new_file.write(downloadedFile)
                self.usrReference = src
        except Exception as e:
            print("[log] " + str(e))
            self.bot.send_message(message.chat.id, "Не удалось загрузить ваш файл")
        self.bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
        self.bot.register_next_step_handler(message, self.Main.handleRequestWishes)
        
    def saveWishes(self, message):
        self.usrWishes = message.text
        run(self.db.requestDb(self.usrName, self.usrEmail, self.usrPhone, self.usrClient, self.usrChoice, self.usrNeedPack, self.usrSendToPlace, self.usrSendDate, self.usrReference, self.usrWishes))
        self.Main.req_bool = False



