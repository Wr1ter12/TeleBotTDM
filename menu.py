from telebot import types

class Menu:
    def __init__(self, bot):
        self.bot = bot
        self.yesNoKeyboard()
        self.productServiceKeyboard()
        self.productsKeyboard()
        self.servicesKeyboard()
        self.requestServiceKeyboard()
        self.requestProductKeyboard()
        self.requestProductSendKeyboard()
    
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
        
    def productsKeyboard(self):
        self.pKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='1.1')
        item2 = types.KeyboardButton(text='1.2')
        item3 = types.KeyboardButton(text='1.3')
        item4 = types.KeyboardButton(text='1.4')
        item5 = types.KeyboardButton(text='1.5')
        item6 = types.KeyboardButton(text='1.6.1')
        item7 = types.KeyboardButton(text='1.6.2')
        self.pKeyboard.add(item1, item2, item3)
        self.pKeyboard.add(item4, item5)
        self.pKeyboard.add(item6, item7)

    def servicesKeyboard(self):
        self.sKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='1.1.1')
        item2 = types.KeyboardButton(text='1.1.2')
        item3 = types.KeyboardButton(text='1.1.3')
        item4 = types.KeyboardButton(text='1.2')
        item5 = types.KeyboardButton(text='1.3.1')
        item6 = types.KeyboardButton(text='1.3.2')
        item7 = types.KeyboardButton(text='1.3.3')
        item8 = types.KeyboardButton(text='1.4')
        item9 = types.KeyboardButton(text='1.5.1')
        item10 = types.KeyboardButton(text='1.5.2')
        item11 = types.KeyboardButton(text='1.5.3')
        item12 = types.KeyboardButton(text='1.5.4')
        item13 = types.KeyboardButton(text='1.5.5')
        item14 = types.KeyboardButton(text='1.6.1')
        item15 = types.KeyboardButton(text='1.6.2')
        item16 = types.KeyboardButton(text='1.6.3')
        item17 = types.KeyboardButton(text='1.7.1')
        item18 = types.KeyboardButton(text='1.7.2')
        item19 = types.KeyboardButton(text='1.7.3')
        item20 = types.KeyboardButton(text='1.8')
        item21 = types.KeyboardButton(text='1.9.1')
        item22 = types.KeyboardButton(text='1.9.2')
        self.sKeyboard.add(item1, item2, item3)
        self.sKeyboard.add(item4)
        self.sKeyboard.add(item5, item6, item7)
        self.sKeyboard.add(item8)
        self.sKeyboard.add(item9, item10, item11, item12, item13)
        self.sKeyboard.add(item14, item15, item16)
        self.sKeyboard.add(item17, item18, item19)
        self.sKeyboard.add(item20)
        self.sKeyboard.add(item21, item22)

    def requestServiceKeyboard(self):
        self.rsKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Имя')
        item2 = types.KeyboardButton(text='Телефон')
        item3 = types.KeyboardButton(text='Почта')
        item4 = types.KeyboardButton(text='Клиент')
        item5 = types.KeyboardButton(text='Категория')
        item6 = types.KeyboardButton(text='Комментарии')
        self.rsKeyboard.add(item1, item2, item3)
        self.rsKeyboard.add(item4, item5, item6)
        
    def requestProductKeyboard(self):
        self.rpKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Имя')
        item2 = types.KeyboardButton(text='Телефон')
        item3 = types.KeyboardButton(text='Почта')
        item4 = types.KeyboardButton(text='Клиент')
        item5 = types.KeyboardButton(text='Категория')
        item6 = types.KeyboardButton(text='Упаковка')
        item7 = types.KeyboardButton(text='Комментарии')
        self.rpKeyboard.add(item1, item2, item3)
        self.rpKeyboard.add(item4, item5, item6)
        self.rpKeyboard.add(item7)
        
    def requestProductSendKeyboard(self):
        self.rpsKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text='Имя')
        item2 = types.KeyboardButton(text='Телефон')
        item3 = types.KeyboardButton(text='Почта')
        item4 = types.KeyboardButton(text='Клиент')
        item5 = types.KeyboardButton(text='Категория')
        item6 = types.KeyboardButton(text='Упаковка')
        item7 = types.KeyboardButton(text='Адрес доставки')
        item8 = types.KeyboardButton(text='Дата доставки')
        item9 = types.KeyboardButton(text='Комментарии')
        self.rpsKeyboard.add(item1, item2, item3)
        self.rpsKeyboard.add(item4, item5, item6)
        self.rpsKeyboard.add(item7, item8, item9)
        
