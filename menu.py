from telebot import types

class Menu:
    def __init__(self, bot):
        self.bot = bot
        self.yesNoKeyboard()
        self.productServiceKeyboard()
    
    def showMainMenu(self, message):
        keyboard = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text='Оставить заявку', callback_data='leave_request')
        item2 = types.InlineKeyboardButton(text='Заказать звонок', callback_data='order_call')
        item3 = types.InlineKeyboardButton(text='О нас', callback_data='information')
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)

        self.bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=keyboard)

    def phoneKeyboard(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('Отправить номер телефона', request_contact=True)
        markup.add(item)

        self.bot.send_message(message.chat.id, "Пожалуйста, отправьте ваш номер телефона", reply_markup=markup)

    def yesNoKeyboard(self):
        self.YNKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Да')
        item2 = types.KeyboardButton(text='Нет')
        self.YNKeyboard.add(item1)
        self.YNKeyboard.add(item2)

    def productServiceKeyboard(self):
        self.PSKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Продукция')
        item2 = types.KeyboardButton(text='Услуга')
        self.PSKeyboard.add(item1)
        self.PSKeyboard.add(item2) 
