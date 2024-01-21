# Imports # 
import sqlite3

class DataBase: # Allows users to connect to the database and do certain tasks
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.username = None
        self.password = None
        self.remember_me = None

    def connect(self): # Connects to the database
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row # returns rows as special row objects and allows to use dictionary e.g. data[username] instead of data[0]
        self.cursor = self.conn.cursor()

    def close(self):  # Closes the connection to the database to save resources etc
        if self.conn:
            self.conn.close()

    def setup_database(self): # Sets up the initial database 
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

    def check_database(self, username, password, remember_me_boolean): # checks if login details were saved before in the database
        self.connect()
        self.username = username
        self.password = password
        self.remember_me = remember_me_boolean
        self.cursor.execute('SELECT * FROM users')
        dataset = self.cursor.fetchall()

        for data in dataset:
            if data['username'] == self.username and data['password'] == self.password:
                if self.remember_me: # Checks if the remember_me checkbox was enabled and if so adds the current login to the local_credentials so that they dont have to login next time
                    self.cursor.execute('INSERT OR REPLACE INTO local_credentials (username, password) VALUES (?, ?)',
                                        (self.username, self.password))
                    self.conn.commit()
                else:
                    # Deletes the previous local_credential values if remember_me isn't true and makes the user login next time they open the application
                    self.cursor.execute('DELETE FROM local_credentials WHERE username = ? AND password = ?',
                                        (self.username, self.password))
                    self.conn.commit() # Commits the changes

                self.close() # Closes the connection
                return True
        return False
    
    def check_if_login_saved(self): # Checks to see if the user previously saved their login for when they pressed "Remember Me" checkbox
        self.connect() # Connects to the database
        self.cursor.execute('SELECT * FROM local_credentials')# grabs all the data from the table 'local_credentials'
        local_cred = self.cursor.fetchone() # fetches the first row in the table 'local_credentials'
        return local_cred # returns True if there is previous saved data and False if there isn't any
    
    def does_user_exist(self,user,password=None): # Checks if user already exists in database with optional password parameter
            #CHECKS THE DATABASE
            self.connect() # Connects to the database
            self.cursor.execute('SELECT * FROM users')
            dataset = self.cursor.fetchall() # Gets all the data
            for data in dataset: 
                if data['username'] == user: # Checks to see if user already exists in the database or not 
                    if password and data['password'] == password: # If the function had password argument, it checks if the password also matches 
                        self.close()
                        return True
                    else: # If no password was given, but the username is in the database it still returns True 
                        self.close()
                        return True
            self.close() # Closes the connection
            return False # returns False if username/ username & password doesn't exist in the database
    
    def add_new_user(self,user,email,password): # Adds the user to the database
        self.connect() # Connects to the database
        self.cursor.execute('INSERT OR IGNORE INTO users (username,email,password) VALUES (?,?,?)', (user,email,password)) # Adds the new user,email and pass to the database
        self.conn.commit() # Commits the changes
        self.close() # Closes the connection
        
    def delete_saved_login(self): # Deletes the previous local_credential values
        self.connect() # Connects to the database
        self.cursor.execute('DELETE FROM local_credentials') # Deletes the data from the local_credentials table
        self.conn.commit() # Commits the changes
        self.close() # Closes the connection (saves up on resources)