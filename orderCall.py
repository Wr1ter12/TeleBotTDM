from telebot import types

chatID = -1002332920843

def handleOrderCall(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Отправить номер телефона', request_contact=True)
    markup.add(item)
    
    from main import bot
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваш номер телефона", reply_markup=markup)

def handleContact(message):
    userID = message.from_user.id
    username = message.from_user.username
    phoneNumber = message.contact.phone_number

    from main import bot, db
    db.phoneBook(userID, username, phoneNumber)
    bot.send_message(chatID, f"Новый запрос на звонок от пользователя {message.from_user.first_name}: {phoneNumber}")

    bot.send_message(message.chat.id, "Спасибо! Ваш запрос на звонок принят.")

def handleManualPhoneNumber(message):
    userID = message.from_user.id
    username = message.from_user.username
    phoneNumber = message.text

    from main import bot, db
    db.phoneBook(userID, username, phoneNumber)
    bot.send_message(chatID, f"Новый запрос на звонок от пользователя {message.from_user.first_name}: {phoneNumber}")

    bot.send_message(message.chat.id, "Спасибо! Ваш запрос на звонок принят.")
