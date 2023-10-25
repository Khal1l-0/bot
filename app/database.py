import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id TEXT, "
                "name TEXT, "
                "number INTEGER, "
                "applications TEXT,"
                "lang TEXT NOT NULL DEFAULT ru)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT,"
                "desc TEXT, "
                "photo TEXT)")
    db.commit()

    

    
def first_select_user(chat_id):
    cur.execute('''SELECT * FROM accounts WHERE tg_id = ?''', (chat_id, ))
    user = cur.fetchone()
    db.commit()
    return user

def save_user_info(chat_id, number):
    cur.execute('''
                INSERT INTO accounts(tg_id, number) VALUES(?, ?)
    ''', (chat_id, number))
    db.commit()

async def add_application(state):
    async with state.proxy() as data:
        cur.execute('''
                    UPDATE accounts 
                    SET name = ?, applications = ?''', (data['name'], data['applications']))
    db.commit()
  
def get_lang(chat_id):
    cur.execute('''
                SELECT lang FROM accounts WHERE tg_id = ?''', (chat_id, ))
    language = cur.fetchone()[0]
    db.commit  
    return language
    
    
def change_lang(lang):
    cur.execute('''
                UPDATE accounts 
                SET lang = ?''', (lang, ))
    db.commit()
    

    
# def add_user(chat_id, lang):
#     cur.execute('''SELECT INTO accounts (tg_id, lang) VALUES (? , ?)''', (chat_id, lang))
#     db.commit()

# def get_lang(chat_id):
#     cur.execute('''SELECT lang FROM accounts WHERE tg_id = ?''', (chat_id,))
#     lang= cur..fetchone()[0]
#     db.commit()
    