import sqlite3
import bcrypt
from datetime import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect('chatbot_users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        role TEXT,
        message TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# --- FUNCTIONS ---
def signup_user(email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True
    return False

def save_message(email, role, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chat_history (email, role, message, timestamp) VALUES (?, ?, ?, ?)",
                   (email, role, message, timestamp))
    conn.commit()

def get_chat_dates(email):
    cursor.execute("SELECT DISTINCT DATE(timestamp) FROM chat_history WHERE email = ? ORDER BY timestamp DESC", (email,))
    return [row[0] for row in cursor.fetchall()]

def get_history_by_date(email, date):
    cursor.execute("""
        SELECT role, message, timestamp 
        FROM chat_history 
        WHERE email = ? AND DATE(timestamp) = ? 
        ORDER BY timestamp
    """, (email, date))
    return cursor.fetchall()

def delete_history(email):
    cursor.execute("DELETE FROM chat_history WHERE email = ?", (email,))
    conn.commit()

def close_connection():
    conn.close()
