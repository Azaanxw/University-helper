import sqlite3
def setup_database():
#DATABASE SETUP FOR DEFAULT LOGIN
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    password TEXT NOT NULL
                    )
                    ''')
    cursor.execute('INSERT OR IGNORE INTO users (username,email,password) VALUES (?,?,?)', ('admin','admin@test.com','123'))
    conn.commit()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    print(data)
    conn.close()
if __name__ == "__main__":
    setup_database()