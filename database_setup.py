import sqlite3
def setup_database():
#DATABASE SETUP FOR DEFAULT LOGIN
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Creates users table with specific columns which are id,username,email and password
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    password TEXT NOT NULL
                    )     
                    ''')
    cursor.execute('INSERT OR IGNORE INTO users (username,email,password) VALUES (?,?,?)', ('admin','admin@test.com','123')) # Creates a default login for testing purposes 
    conn.commit() #Commits the changes 
    
     # Creates local_credentials table with specific columns which are username and password (for logging in the next time)
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS local_credentials (
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )     
                    ''')
    # cursor.execute('SELECT * FROM users')
    # data = cursor.fetchall() # Fetches all the data from users table
    # print(data)  # Prints the data on startup
    conn.close()
if __name__ == "__main__":  # Calls the setup_database function when the script is run as the main program and prevents it from running when it is imported as a module in the main.py script
    setup_database()