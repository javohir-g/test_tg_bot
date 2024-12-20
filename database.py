import sqlite3

# Создание или подключение к базе данных
def connect_db():
    conn = sqlite3.connect('users.db')  # файл базы данных
    return conn

# Создание таблицы пользователей
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Добавление пользователя в базу данных
def add_user(user_id, name, phone_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, name, phone_number)
        VALUES (?, ?, ?)
    ''', (user_id, name, phone_number))
    conn.commit()
    conn.close()

# Получение данных пользователя по user_id
def get_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, phone_number FROM users WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Инициализация таблицы (если ее нет)
create_table()