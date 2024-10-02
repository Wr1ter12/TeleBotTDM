import sqlite3

"""connection = sqlite3.connect("TDM.db", check_same_thread=False)
cursor = connection.cursor()"""

class db:
    def __init__(self, db):
        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), email VARCHAR(100), phone VARCHAR(20));')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS phoneNumbers (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, username VARCHAR(50), phoneNumber VARCHAR(20))')
        self.connection.commit()

    def phoneBook(self, userID, username, phoneNumber):
        self.cursor.execute("INSERT INTO phoneNumbers (userID, username, phoneNumber) VALUES (?, ?, ?)", (userID, username, phoneNumber))
        self.connection.commit()
        
    def example(self):
        self.cursor.execute('INSERT INTO Users (name, email, phone) VALUES (?,?,?)', ('Andrew', 'Andrew@gmail.com', '+79345021324'))
        self.connection.commit()
        self.cursor.execute('SELECT * FROM Users')
        users = self.cursor.fetchall()

        for i in users:
            print(i)

    def __del__(self):
        self.connection.close()
