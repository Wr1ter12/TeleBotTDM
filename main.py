import telebot
import messages, sql, orderCall
import re

bot = telebot.TeleBot('7621236265:AAGs2_RbavfCZxKYQP2mLtiEYVTrcgzqNOk')
db = sql.db('TDM.db')

class Messages:
    @bot.message_handler(commands=['start', 'info', 'help'])
    def commands(message):
        match message.text:
            case "/start":
                messages.start(message)
            case "/info":
                messages.info(message)
            case "/help":
                messages.help(message)
            case _:
                print("[log] Неизвестная команда")

    @bot.message_handler(func=lambda message: message.text.lower() == 'заказать звонок')
    def handleOrderCall(message):
        orderCall.handleOrderCall(message)

    @bot.message_handler(func=lambda message: re.match(r'^\+?[1-9]\d{1,14}$', message.text))
    def handleManualPhoneNumber(message):
        orderCall.handleManualPhoneNumber(message)

    @bot.message_handler(content_types = ['text'])
    def messaging(message):
        messages.usr_msg(message)

    @bot.message_handler(content_types=['contact'])
    def handleContact(message):
        orderCall.handleContact(message)




if __name__ == '__main__':
    print("[log] Запуск готов")
    bot.polling(none_stop=True)

