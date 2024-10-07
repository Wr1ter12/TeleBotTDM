Telegram-бот на Python, созданный с использованием нескольких соединенных между собой файлов на Python.
main.py - Основной Python файл, включающий в себя непосредственно запуск бота и обработку сообщений, обращающийся к остальным методам остальных файлов.
messages.py - Python файл с методами для обработки сообщений.
sql.py - Python файл с методами использования базы данных sqlite.
orderCall.py - Python файл для работы с заказами звонков.
request.py - Python файл для работы с обработкой заявок.
menu.py - Python файл для работы с клавиатурами и выпадающими кнопками.

Async - Дополнительная сборка Telegram-бота, использующая асинхронные sql-функции.

Telegram is a Python bot, created using several interconnected Python files.
main.py - The main Python file, which includes directly launching the bot and processing messages, accessing the rest of the methods of the remaining files.
messages.py - Python file with methods for processing messages.
sql.py - Python file with sqlite database usage methods.
orderCall.py - Python file for working with call orders. request.py -
Python file for processing applications.
menu.py - Python file for working with keyboards and drop-down buttons.

Async is an additional build of the Telegram bot that uses asynchronous sql functions.

Использованные дополнительные библиотеки:
Main: telebot, sqlite3
Async: asyncio, aiosqlite
(Есть в Requirements.txt) 
