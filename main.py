import telebot
import sql
from re import match
from request import Requests
from messages import Messages
from orderCall import CallOrder
from menu import Menu
from os import getcwd, mkdir, path

token = ''

if not path.isdir('ДокументыПользователей'):
    mkdir("ДокументыПользователей")
    if not path.isdir('ДокументыПользователей//photos'):
        mkdir("ДокументыПользователей//photos")

bot = telebot.TeleBot(token)

db = sql.db('TDM.db')

messages = Messages(bot)
menu = Menu(bot)
orderCall = CallOrder(bot, db, menu)

class Main:
    users = {}
    currentDir = getcwd()

    def userAdd(userID):
        userID = str(userID)
        if userID not in Main.users.keys():
            Main.users[userID] = [False, False]
    
    @bot.message_handler(commands=['start', 'info', 'help', 'request'])
    def commands(message):
        Main.userAdd(message.from_user.username)
        match message.text:
            case "/start":
                messages.start(message)
                menu.showMainMenu(message)
            case "/info":
                messages.info(message)
                menu.showMainMenu(message)
            case "/help":
                messages.help(message)
                menu.showMainMenu(message)
            case "/request":
                Main.handleRequest(message)
            case _:
                print("[log] Неизвестная команда")

    @bot.message_handler(func=lambda message: message.text.lower() == 'оставить заявку')
    def handleRequest(message):
        Main.userAdd(message.from_user.username)
        Main.users[str(message.from_user.username)][0] = True
        msg = request.request(message)
        bot.register_next_step_handler(msg, request.userName)

    def handleRequestSec(message):
        msg = request.userPhoneNumber(message)

    @bot.message_handler(func=lambda message: '@' in message.text.lower())
    def handleRequestThr(message):
        request.userEmail(message)

    @bot.message_handler(func=lambda message: message.text.lower() == "Да" or message.text.lower() == "Нет" )
    def handleRequestForth(message):
        request.intProd(message)

    @bot.message_handler(func=lambda message: message.text.lower() == "продукция" or message.text.lower() == "услуга")
    def handleRequestFifth(message):
        request.productsSelection(message)

    def handleRequestTypeOfServices(message):
        request.typeOfServices(message)

    def handleRequestProductsCategories(message):
        request.productsCategories(message)

    def handleRequestNeedPacking(message):
        request.needPacking(message)

    def handleRequestNeedSend(message):
        request.needSend(message)

    def handleRequestSendAddress(message):
        request.sendAddress(message)
    
    def handleRequestSendDate(message):
        request.sendDate(message)

    def handleRequestSendToObj(message):
        request.saveFile(message)

    def handleRequestWishes(message):
        request.saveWishes(message)

    @bot.message_handler(func=lambda message: message.text.lower() == 'заказать звонок')
    def handleOrderCall(message):
        Main.userAdd(message.from_user.username)
        Main.users[str(message.from_user.username)][1] = True
        orderCall.handleOrderCall(message)

    @bot.message_handler(func=lambda message: match(r'^\+?[1-9]\d{1,14}$', message.text) and len(message.text)>=7 and len(message.text)<=15)
    def handleManualPhoneNumber(message):
        Main.userAdd(message.from_user.username)
        if Main.users[str(message.from_user.username)][0] == False:
            if Main.users[str(message.from_user.username)][1] == True:
                orderCall.handleManualPhoneNumber(message)
                menu.showMainMenu(message)
                Main.users[str(message.from_user.username)][1] = False
            else:
                bot.send_message(message.chat.id, "Не удалось обработать ваше сообщение, воспользуйтесь предоставленными функциями.")
                menu.showMainMenu(message)
        else:
            Main.handleRequestSec(message)

    @bot.message_handler(content_types=['contact'])
    def handleContact(message):
        Main.userAdd(message.from_user.username)
        if Main.users[str(message.from_user.username)][0] == False:
            orderCall.handleContact(message)
            menu.showMainMenu(message)
            Main.users[str(message.from_user.username)][1] = False
        else:
            Main.handleRequestSec(message)

    @bot.callback_query_handler(func=lambda call: True)
    def handleCallbackQuery(call):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        if call.data == 'leave_request':
            Main.handleRequest(call.message)
        elif call.data == 'order_call':
            Main.handleOrderCall(call.message)
        elif call.data == 'information':
            messages.info(call.message)
            Main.userAdd(call.message.from_user.username)
            menu.showMainMenu(call.message)

    @bot.message_handler(content_types = ['text'])
    def messaging(message):
        Main.userAdd(message.from_user.username)
        match message.text.lower():
            case 'инфо':
                messages.info(message)
            case 'о нас':
                messages.info(message)
            case 'техническая поддержка':
                bot.send_message(message.chat.id, "Свяжитесь с нами по номеру +7 (495) 927 95 17.")
            case 'обратная связь':
                bot.send_message(message.chat.id, "Свяжитесь с нами по номеру +7 (495) 927 95 17.")
            case _:
                if Main.users[str(message.from_user.username)][0] == False:
                    bot.send_message(message.chat.id, "Не удалось обработать ваше сообщение, воспользуйтесь предоставленными функциями.")
                else:
                    messages.usr_msg(message)
        menu.showMainMenu(message)
        
request = Requests(bot, db, menu, Main)

if __name__ == '__main__':
    print("[log] Запуск готов")
    bot.polling(none_stop=True)
