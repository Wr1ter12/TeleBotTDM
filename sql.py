import sqlite3

class db:
    def __init__(self, db):
        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone VARCHAR(20), client VARCHAR(3), choice TEXT, pack TEXT, send TEXT, sendDate TEXT, wishes TEXT);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS phoneNumbers (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, username VARCHAR(50), phoneNumber VARCHAR(20))')
        self.connection.commit()

    def phoneBook(self, userID, username, phoneNumber):
        cursor = self.cursor.execute('SELECT * FROM phoneNumbers WHERE (userID=? AND username=? AND phoneNumber=?)', (userID, username, phoneNumber))
        entry = cursor.fetchone()
        if entry is None:
            self.cursor.execute("INSERT INTO phoneNumbers (userID, username, phoneNumber) VALUES (?, ?, ?)", (userID, username, phoneNumber))
            self.connection.commit()

    def requestDb(self, name, email, phone, client, choice, pack, send, sendDate, wishes):
        cursor = self.connection.execute('SELECT * FROM Users WHERE (name=? AND email=? AND phone=? AND client=? AND choice=? AND pack=? AND send=? AND sendDate=? AND wishes=?)', (name, email, phone, client, choice, pack, send, sendDate, wishes))
        entry = cursor.fetchone()
        if entry is None:
            self.cursor.execute('INSERT INTO Users (name, email, phone, client, choice, pack, send, sendDate, wishes) VALUES (?,?,?,?,?,?,?,?,?)', (name, email, phone, client, choice, pack, send, sendDate, wishes))
            self.connection.commit()

        self.cursor.execute('SELECT * FROM Users')
        users = self.cursor.fetchall()

        for i in users:
            print(i)

        self.connection.commit()
    def __del__(self):
        self.connection.close()
