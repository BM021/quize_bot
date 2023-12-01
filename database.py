import sqlite3

from datetime import datetime


connection = sqlite3.connect('data.db')
sql = connection.cursor()

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name TEXT, 
    telegram_id INTEGER, 
    phone_number TEXT, 
    coin INTEGER,
    reg_date DATETIME
    );
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    correct_answer TEXT,
    options TEXT
    );
    """
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    correct_answer INTEGER,
    got_coins INTEGER,
    played_date DATETIME
    );
    """
)

def register_user(first_name, telegram_id, phone_number, coin=0):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute(" INSERT INTO users (first_name, telegram_id, phone_number, coin, reg_date) VALUES (?,?,?,?,?); ",
                 (first_name, telegram_id, phone_number, coin, datetime.now()))
    

    connection.commit()
    connection.close()


def check_user(telegram_id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    user = sql.execute(" SELECT telegram_id FROM users WHERE telegram_id=?; ", (telegram_id,)).fetchone()

    if user:
        return True
    
    else:
        return False
    

def add_history(telegram_id, correct_answer, got_coins):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute(" INSERT INTO history (telegram_id, correct_answer, got_coins, played_date) VALUES (?,?,?,?); ",
                (telegram_id, correct_answer, got_coins, datetime.now()))
    
    connection.commit()
    connection.close()


def get_history(telegram_id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    user_history = sql.execute(" SELECT correct_asnwer, got_coins, played_date FROM history WHERE telegram_id=?; ", (telegram_id,))

    if user_history:
        return user_history.fetchall()
    
    else:
        return False
    

def add_question(question, correct_answer, options):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute(" INSERT INTO questions (question, correct_answer, options) VALUES (?,?,?); ", 
                (question, correct_answer, options))
    
    connection.commit()
    connection.close()


def delete_question(question):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute(" DELETE FROM questions WHERE question=?; ", (question,))

    connection.commit()
    connection.close()


def update_question(new_question, question):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute(" UPDATE questions SET question=? WHERE question=?; ", (new_question, question))    

    connection.commit()
    connection.close()

