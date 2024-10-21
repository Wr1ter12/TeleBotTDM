import telebot
import sql
from re import match
from request import Requests
from messages import Messages
from orderCall import CallOrder
from menu import Menu

chatID = -1002332920843

bot = telebot.TeleBot('7621236265:AAGs2_RbavfCZxKYQP2mLtiEYVTrcgzqNOk')

db = sql.db('TDM.db')

messages = Messages(bot)
menu = Menu(bot)
orderCall = CallOrder(bot, db, menu, chatID)

class Main:
    users = {}

    def userAdd(userID):
        userID = str(userID)
        if userID not in list(Main.users.keys()):
            Main.users[userID] = [False, False]

    def stopCheck(func):
        def wrapper(message, save=None):
            if message.text == "/stop":
                Main.userAdd(message.from_user.username)
                Main.users[str(message.from_user.username)][0] = False
                bot.send_message(message.chat.id, "Оформление заявки успешно отменено!")
                menu.showMainMenu(message)
                return
            if save == None:
                return func(message)
            else:
                return func(message, save)
        return wrapper
    
    @bot.message_handler(commands=['start', 'info', 'help', 'request', 'stop'])
    def commands(message):
        Main.userAdd(message.from_user.username)
        match message.text.lower():
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
            case "/stop":
                Main.users[str(message.from_user.username)][0] = False
                menu.showMainMenu(message)
            case _:
                print("[log] Неизвестная команда")

    @bot.message_handler(func=lambda message: message.text.lower() == 'оставить заявку')
    def handleRequest(message, save):
        Main.userAdd(message.from_user.username)
        Main.users[str(message.from_user.username)][0] = True
        msg = request.request(message)
        bot.register_next_step_handler(msg, request.userName, save)

    @stopCheck
    def handleRequestSec(message, save=False):
        msg = request.userPhoneNumber(message, save)

    @bot.message_handler(func=lambda message: match(r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$', message.text))
    @stopCheck
    def handleRequestThr(message, save=False):
        request.userEmail(message, save)

    @stopCheck
    def handleRequestForth(message, save=False):
        request.intProd(message, save)

    @stopCheck
    def handleRequestFifth(message, save=False):
        request.productsSelection(message, save)

    @stopCheck
    def handleRequestTypeOfServices(message, save=False):
        request.typeOfServices(message, save)

    @stopCheck
    def handleRequestProductsCategories(message, save=False):
        request.productsCategories(message, save)

    @stopCheck
    def handleRequestNeedPacking(message, save=False):
        request.needPacking(message, save)

    @stopCheck
    def handleRequestNeedSend(message, save=False):
        request.needSend(message, save)

    @stopCheck
    def handleRequestSendAddress(message, save=False):
        request.sendAddress(message, False)

    @stopCheck
    def handleRequestSendDate(message, save=False):
        request.sendDate(message, False)

    @stopCheck
    def handleRequestWishes(message, save=False):
        request.saveWishes(message, save)
        
    def handleRequestConfirmation(message):
        request.saveRequest(message)

    def handleRequestModification(message):
        if message.content_type != 'text':
            bot.send_message(message.chat.id, "Неправильный формат ответа!")
            if request.usrNeedPack == " ":
                bot.send_message(message.chat.id, "Введите номер поля для изменения:", reply_markup=menu.rsKeyboard)
                bot.register_next_step_handler(message, Main.handleRequestSendDate)
            else:
                    bot.send_message(message.chat.id, "Введите номер поля для изменения:", reply_markup=menu.rpsKeyboard)
            return
        match message.text.lower():
            case "имя":
                msg = bot.reply_to(message, "Введите ваше имя.")
                bot.register_next_step_handler(msg, request.userName, True)
            case "телефон":
                Main.handleOrderCall(message)
                bot.register_next_step_handler(message, Main.handleRequestSec, True)
            case "почта":
                msg = bot.reply_to(message, "Введите ваш адрес электронной почты.")
                bot.register_next_step_handler(msg, Main.handleRequestThr, True)
            case "клиент":
                msg = bot.reply_to(message, "Являетесь ли вы нашим клиентом? (Да/Нет)", reply_markup=menu.YNKeyboard)
                bot.register_next_step_handler(msg, Main.handleRequestForth, True)
            case "категория":
                msg = bot.reply_to(message, "Что вас интересует: продукция или услуга?", reply_markup=menu.PSKeyboard)
                bot.register_next_step_handler(msg, Main.handleRequestFifth, True)
            case "упаковка":
                bot.send_message(message.chat.id, "Нужна ли упаковка? (Да/Нет)", reply_markup=menu.YNKeyboard)
                bot.register_next_step_handler(message, Main.handleRequestNeedPacking, True)
            case "адрес доставки":
                bot.send_message(message.chat.id, "Введите адрес доставки:")
                bot.register_next_step_handler(message, Main.handleRequestSendAddress, True)
            case "дата доставки":
                bot.send_message(message.chat.id, "Введите дату доставки:")
                bot.register_next_step_handler(message, Main.handleRequestSendDate, True)
            case "комментарии":
                bot.send_message(message.chat.id, "Вы можете ввести пожелания или комментарии")
                bot.register_next_step_handler(message, Main.handleRequestWishes, False)
            case _:
                bot.send_message(message.chat.id, "Некорректный ввод!")
                request.saveWishes(message, True)

    @bot.message_handler(func=lambda message: message.text.lower() == 'заказать звонок')
    def handleOrderCall(message):
        Main.userAdd(message.from_user.username)
        Main.users[str(message.from_user.username)][1] = True
        orderCall.handleOrderCall(message)

    @bot.message_handler(func=lambda message: match(r'^\+?[1-9]\d{1,14}$', message.text) and len(message.text)>=11 and len(message.text)<=12)
    def handleManualPhoneNumber(message):
        Main.userAdd(message.from_user.username)
        Main.users[str(message.from_user.username)][1] = True
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
            Main.handleRequest(call.message, False)
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
        
request = Requests(bot, db, menu, Main, chatID)

if __name__ == '__main__':
    print("[log] Запуск готов")
    bot.polling(none_stop=True)
