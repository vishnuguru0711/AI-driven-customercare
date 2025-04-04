import sqlite3

conn = sqlite3.connect("chatbot_users.db")
cursor = conn.cursor()

print("=== Users ===")
for row in cursor.execute("SELECT * FROM users"):
    print(row)

print("\n=== Chat History ===")
for row in cursor.execute("SELECT * FROM chat_history"):
    print(row)

conn.close()
