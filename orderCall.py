class CallOrder:
    def __init__(self, bot, db, menu, chatID):
        self.bot = bot
        self.db = db
        self.Menu = menu
        self.chatID = chatID
        
    def handleOrderCall(self, message):
        self.Menu.phoneKeyboard(message)

    def handleContact(self, message):
        userID = message.from_user.id
        username = message.from_user.username
        phoneNumber = message.contact.phone_number

        self.db.phoneBook(userID, username, phoneNumber)
        self.bot.send_message(self.chatID, f"Новый запрос на звонок от пользователя {message.from_user.first_name}: {phoneNumber}")

        self.bot.send_message(message.chat.id, "Спасибо! Ваш запрос на звонок принят.")

    def handleManualPhoneNumber(self, message):
        userID = message.from_user.id
        username = message.from_user.username
        phoneNumber = message.text
        if phoneNumber.startswith("8") or phoneNumber.startswith("7") or phoneNumber.startswith("+7"):
            self.db.phoneBook(userID, username, phoneNumber)
            self.bot.send_message(self.chatID, f"Новый запрос на звонок от пользователя {message.from_user.first_name}: {phoneNumber}")

            self.bot.send_message(message.chat.id, "Спасибо! Ваш запрос на звонок принят.")
        else:
            self.bot.send_message(message.chat.id, "Некорректный формат номера телефона!")
