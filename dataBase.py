import sqlite3

class DataBase:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.username = None
        self.password = None
        self.remember_me = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def setup_database(self):
        self.connect()

        # Creates users table with specific columns which are id, username, email, and password
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                password TEXT NOT NULL
            )
        ''')

        self.cursor.execute('INSERT OR IGNORE INTO users (username, email, password) VALUES (?, ?, ?)',
                            ('admin', 'admin@test.com', '123'))  # Creates a default login for testing purposes

        # Commit the changes
        self.conn.commit()

        # Creates local_credentials table with specific columns which are username and password (for logging in the next time)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS local_credentials (
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        self.close()
        print("Database successfully loaded")
    def check_database(self, username, password, remember_me_boolean):
        self.connect()
        self.username = username
        self.password = password
        self.remember_me = remember_me_boolean
        self.cursor.execute('SELECT * FROM users')
        dataset = self.cursor.fetchall()

        for data in dataset:
            if data['username'] == self.username and data['password'] == self.password:
                if self.remember_me:
                    self.cursor.execute('INSERT OR REPLACE INTO local_credentials (username, password) VALUES (?, ?)',
                                        (self.username, self.password))
                    self.conn.commit()
                else:
                    # Deletes the previous local_credential values if remember_me isn't true
                    self.cursor.execute('DELETE FROM local_credentials WHERE username = ? AND password = ?',
                                        (self.username, self.password))
                    self.conn.commit()

                self.close()
                return True
        return False
    def check_if_login_saved(self):
        self.connect()
        self.cursor.execute('SELECT * FROM local_credentials')# grabs all the data from the table 'local_credentials'
        local_cred = self.cursor.fetchone() # fetches the first row in the table 'local_credentials'
        return local_cred
    def does_user_exist(self,user,password): # Checks if user already exists in database
            #CHECKS THE DATABASE
            self.connect()
            self.cursor.execute('SELECT * FROM users')
            dataset = self.cursor.fetchall()
            for data in dataset:
                if data['username'] == user and data['password'] == password:
                    self.close()
                    return True
            self.close()
            return False
        