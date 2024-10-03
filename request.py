def request(message):
    from main import bot

    msg = bot.reply_to(message, "Пожалуйста, введите ваше имя.")
    return msg

def userName(message):
    name = message.text
    print(name)
