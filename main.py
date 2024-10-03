import telebot
import sql
from re import match
from request import Requests
from messages import Messages
from orderCall import CallOrder
from menu import Menu

bot = telebot.TeleBot('7621236265:AAGs2_RbavfCZxKYQP2mLtiEYVTrcgzqNOk')
db = sql.db('TDM.db')

messages = Messages(bot)
menu = Menu(bot)
orderCall = CallOrder(bot, db, menu)
request = Requests(bot, db)

class Main:
    @bot.message_handler(commands=['start', 'info', 'help','request'])
    def commands(message):
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
                request.request(message)
            case _:
                print("[log] Неизвестная команда")

    @bot.message_handler(func=lambda message: message.text.lower() == 'заказать звонок')
    def handleOrderCall(message):
        orderCall.handleOrderCall(message)

    @bot.message_handler(func=lambda message: match(r'^\+?[1-9]\d{1,14}$', message.text) and len(message.text)>=7 and len(message.text)<=15)
    def handleManualPhoneNumber(message):
        orderCall.handleManualPhoneNumber(message)

    @bot.message_handler(content_types=['contact'])
    def handleContact(message):
        orderCall.handleContact(message)

    @bot.message_handler(func=lambda message: message.text.lower() == 'оставить заявку')
    def handleRequest(message):
        msg = request.request(message)
        bot.register_next_step_handler(msg, request.userName)

    @bot.callback_query_handler(func=lambda call: True)
    def handleCallbackQuery(call):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        if call.data == 'leave_request':
            Main.handleRequest(call.message)
        elif call.data == 'order_call':
            Main.handleOrderCall(call.message)
        elif call.data == 'information':
            messages.info(message)

    @bot.message_handler(content_types = ['text'])
    def messaging(message):
        match message.text.lower():
            case 'инфо':
                messages.info(message)
            case 'о нас':
                messages.info(message)
            case 'техническая поддержка':
                messages.bot.send_message(message.chat.id, "Свяжитесь с нами по номеру +7 (495) 927 95 17.")
            case 'обратная связь':
                messages.bot.send_message(message.chat.id, "Ваше сообщение отправлено! Мы свяжемся с вами.")
            case _:
                messages.usr_msg(message)

if __name__ == '__main__':
    print("[log] Запуск готов")
    bot.polling(none_stop=True)
