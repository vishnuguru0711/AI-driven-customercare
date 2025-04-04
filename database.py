import sqlite3
from passlib.hash import pbkdf2_sha256
from datetime import datetime

# DB SETUP
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    email TEXT,
    role TEXT,
    message TEXT,
    timestamp TEXT
)
""")
conn.commit()

# AUTHENTICATION
def signup_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return False
    hashed_pw = pbkdf2_sha256.hash(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_pw))
    conn.commit()
    return True

def login_user(email, password):
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result:
        return pbkdf2_sha256.verify(password, result[0])
    return False

# MESSAGES
def save_message(email, role, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chats (email, role, message, timestamp) VALUES (?, ?, ?, ?)",
                   (email, role, message, now))
    conn.commit()

def get_chat_dates(email):
    cursor.execute("SELECT DISTINCT DATE(timestamp) FROM chats WHERE email = ?", (email,))
    return [row[0] for row in cursor.fetchall()]

def get_history_by_date(email, date):
    cursor.execute("SELECT role, message, timestamp FROM chats WHERE email = ? AND DATE(timestamp) = ?", (email, date))
    return cursor.fetchall()

def delete_history(email):
    cursor.execute("DELETE FROM chats WHERE email = ?", (email,))
    conn.commit()

def close_connection():
    conn.close()
