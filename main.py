import telebot
import messages

bot = telebot.TeleBot('7403148851:AAGJ7G3PHOvgRDPx52iZTHVf3XO9m2wK4ss')

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
