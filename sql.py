import sqlite3

class db:
    def __init__(self, db):
        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone VARCHAR(20), client VARCHAR(3), choice TEXT, pack TEXT, send TEXT, sendDate TEXT, reference TEXT, wishes TEXT);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS phoneNumbers (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, username VARCHAR(50), phoneNumber VARCHAR(20))')
        self.connection.commit()

    def phoneBook(self, userID, username, phoneNumber):
        self.cursor.execute("INSERT INTO phoneNumbers (userID, username, phoneNumber) VALUES (?, ?, ?)", (userID, username, phoneNumber))
        self.connection.commit()

    def requestDb(self, name, email, phone, client, choice, pack, send, sendDate, reference, wishes):
        self.cursor.execute('INSERT INTO Users (name, email, phone, client, choice, pack, send, sendDate, reference, wishes) VALUES (?,?,?,?,?,?,?,?,?,?)', (name, email, phone, client, choice, pack, send, sendDate, reference, wishes))
        self.connection.commit()

        self.cursor.execute('SELECT * FROM Users')
        users = self.cursor.fetchall()

        for i in users:
            print(i)

        self.connection.commit()
    def __del__(self):
        self.connection.close()
