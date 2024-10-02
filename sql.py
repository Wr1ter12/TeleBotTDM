from main import connection, cursor

def example():
    cursor.execute('INSERT INTO Users (name, email, phone) VALUES (?,?,?)', ('Andrew', 'Andrew@gmail.com', '+79345021324'))
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()

    for i in users:
        print(i)

    connection.commit()
