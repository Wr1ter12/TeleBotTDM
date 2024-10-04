import aiosqlite

class db:
    def __init__(self, db):
        self.database = db

    async def start(self):
        async with aiosqlite.connect(self.database) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS Users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone VARCHAR(20), client VARCHAR(3), choice TEXT, pack TEXT, send TEXT, sendDate TEXT, reference TEXT, wishes TEXT);')
            await db.execute('CREATE TABLE IF NOT EXISTS phoneNumbers (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, username VARCHAR(50), phoneNumber VARCHAR(20))')
            await db.commit()

    async def phoneBook(self, userID, username, phoneNumber):
        async with aiosqlite.connect(self.database) as db:
            cursor = await db.execute('SELECT * FROM phoneNumbers WHERE (userID=? AND username=? AND phoneNumber=?)', (userID, username, phoneNumber))
            entry = await cursor.fetchone()
            if entry is None:
                await db.execute("INSERT INTO phoneNumbers (userID, username, phoneNumber) VALUES (?, ?, ?)", (userID, username, phoneNumber))
                await db.commit()

    async def requestDb(self, name, email, phone, client, choice, pack, send, sendDate, reference, wishes):
        async with aiosqlite.connect(self.database) as db:
            cursor = await db.execute('SELECT * FROM Users WHERE (name=? AND email=? AND phone=? AND client=? AND choice=? AND pack=? AND send=? AND sendDate=? AND reference=? AND wishes=?)', (name, email, phone, client, choice, pack, send, sendDate, reference, wishes))
            entry = await cursor.fetchone()
            if entry is None:
                await db.execute('INSERT INTO Users (name, email, phone, client, choice, pack, send, sendDate, reference, wishes) VALUES (?,?,?,?,?,?,?,?,?,?)', (name, email, phone, client, choice, pack, send, sendDate, reference, wishes))
                await db.commit()

            cursor = await db.execute('SELECT * FROM Users')
            users = await cursor.fetchall()

            for i in users:
                print('[log] ' + str(i))

            await db.commit()
            await cursor.close()
