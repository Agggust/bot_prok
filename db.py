import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS "users" ("id" Integer not null, "tg_id" Integer not null, primary key("id" AUTOINCREMENT));')
connect.commit()

cursor.execute('CREATE TABLE IF NOT EXISTS "categories" ("id" Integer not null, "name" Text not null, primary key("id" AUTOINCREMENT));')
connect.commit()

cursor.execute('CREATE TABLE IF NOT EXISTS "subscribes" ("user_id" Integer not null, "cat_id" Integer not null);')
connect.commit()

cats = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

def addCategory(connect, category):
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO categories('name') VALUES(?);''', (category,))
    connect.commit()

def delSub(user_id, cat_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('''DELETE FROM subscribes WHERE user_id = ? AND cat_id = ?;''', (user_id, cat_id[0],))
    connect.commit()

def isSub(user_id, cat_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    print(type(cat_id))
    if type(cat_id) is int:
        return cursor.execute('SELECT cat_id FROM subscribes WHERE user_id = ? AND cat_id = ?;',
                              (user_id, cat_id)).fetchone()
    else:
        return cursor.execute('SELECT cat_id FROM subscribes WHERE user_id = ? AND cat_id = ?;', (user_id, cat_id[0])).fetchone()

def insertUser(user_id):
    connect = sqlite3.connect('database.db')
    # пися попа чилен
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO users('tg_id') VALUES(?);''', (user_id,))
    connect.commit()

def getUser(tg_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM users WHERE tg_id = ?;',(tg_id,)).fetchone()

def getIdCat(name):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT id FROM categories WHERE name = ?;',(name,)).fetchone()

def insertSub(user_id, cat_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO subscribes('user_id', 'cat_id') VALUES(?,?);''', (user_id,cat_id,))
    connect.commit()

def getIdSubUser(user_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT cat_id FROM subscribes WHERE user_id = ?;', (user_id,)).fetchall()

def getSubUser(user_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    # титька
    return cursor.execute('SELECT categories.name FROM subscribes INNER JOIN categories ON cat_id = categories.id WHERE user_id = ?;', (user_id,)).fetchall()


def getCategories():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT name FROM categories;').fetchall()

def subs(user_id):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM subscribes INNER JOIN categories ON categories.id = subscribes.cate_id WHERE user_id = ?;',(user_id)).fetchall()
