import telebot, sqlite3
import messages

bot = telebot.TeleBot('7621236265:AAGs2_RbavfCZxKYQP2mLtiEYVTrcgzqNOk')
connection = sqlite3.connection("TDM.db")
cursor = connection.cursor()

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

    @bot.message_handler(content_types = ['text'])
    def messaging(message):
        messages.usr_msg(message)

if __name__ == '__main__':
    print("[log] Запуск готов")
    bot.polling(none_stop=True)
