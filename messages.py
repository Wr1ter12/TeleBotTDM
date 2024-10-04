infoMsg = """
Общая информация:
ТДМ - ваш надежный партнер в сфере металлоконструкций!

Мы создаем:

* Металлоконструкции любой сложности 
* Малые архитектурные формы 
* Оборудование для парков и дворов (урны, скамейки, навесы, перголы...)
* И многое другое!

Наши преимущества:

* Опыт работы с 2017 года
* Высокое качество продукции, соответствующее стандартам
* Собственное производство, контроль качества на каждом этапе
* Опытные специалисты и современное оборудование
* Долгосрочное сотрудничество с клиентами
* Доставка по всей России

Свяжитесь с нами, чтобы получить информацию о наших продуктах и услугах!

Контакты:

Телефон: +7 (495) 927 95 17, +7 (925) 616 29 00
Сайт: <a href="https://tdmmag.ru">tdmmag.ru</a> 
Адрес: Москва, ул.1-я Мытищинская, 28 c1
"""

helpMsg = """Бот ТДМ предоставляет возможность:
Оставить заявку, заказать звонок, и получить информацию о нас благодаря клавиатуре.
Также можно использовать команды по типу:
/start - для начала работы с ботом
/info - для получения информации о нас
/help - для краткой информации о пользовании ботом
/request - для оформления заявки"""

class Messages:
    def __init__(self, bot):
        self.bot = bot
        
    def start(self, message):
        self.bot.send_message(message.chat.id, "Здравствуйте, бот готов к работе!")

    def info(self, message):
        self.bot.send_message(
            message.chat.id,
            infoMsg,
            parse_mode='HTML'
        )

    def help(self, message):
        self.bot.send_message(message.chat.id, helpMsg)

    def usr_msg(self, message):
        print("[log] Текстовое сообщение: " + message.text)
