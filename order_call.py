from main import bot, db

chatID = '...'

@bot.message_handler(func=lambda message: message.text == 'Заказать звонок')
def handle_order_call(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = telebot.types.KeyboardButton('Отправить номер телефона', request_contact=True)
    markup.add(item)
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваш номер телефона", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    userID = message.from_user.id
    username = message.from_user.username
    phoneNumber = message.contact.phone_number

    db.phoneBook(userID, username, phoneNumber)

    bot.send_message(ChatID, f"Новый запрос на звонок от пользователя {userID}: {phoneNumber}")

    bot.send_message(message.chat.id, "Спасибо! Ваш запрос на звонок принят.")
