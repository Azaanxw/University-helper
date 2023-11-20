## IMPORTS ##
import sqlite3
from database_setup import setup_database
from login import LoginPage
from signup import SignUpPage
from app import MainPage

setup_database() # sets up the database with a default user and pass

# Creates all the relevant pages
signup_page = SignUpPage()
main_page = MainPage()
login_page = LoginPage()

# Assigns the relevant pages to other pages for them to redirect to
signup_page.assign_login_page(login_page)
signup_page.assign_main_page(page= main_page)
login_page.assign_main_page(page= main_page)
login_page.assign_signup_page(page=signup_page)
main_page.assign_login_page(page=login_page)
# Starts up the login page as the first page to be shown
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM local_credentials') # grabs all the data from the table 'local_credentials'
local_cred = cursor.fetchone() # fetches the first row in the table 'local_credentials'
if local_cred:
    print("Previously logged in")
    main_page.turn_on()
else:
    login_page.turn_on() 
conn.close()
 