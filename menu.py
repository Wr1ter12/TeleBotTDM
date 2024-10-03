from telebot import types

class Menu:
    def __init__(self, bot):
        self.bot = bot
    
    def showMainMenu(self, message):
        keyboard = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text='Оставить заявку', callback_data='leave_request')
        item2 = types.InlineKeyboardButton(text='Заказать звонок', callback_data='order_call')
        item3 = types.InlineKeyboardButton(text='О нас', callback_data='information')
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)

        self.bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=keyboard)

    def phoneKeyboard(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('Отправить номер телефона', request_contact=True)
        markup.add(item)
