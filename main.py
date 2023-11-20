## IMPORTS ##
import sqlite3
from login import LoginPage
from signUp import SignUpPage
from app import MainPage
from dataBase import DataBase
db_instance = DataBase() # sets up the database with a default user and pass
db_instance.setup_database()
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
previously_saved_login = db_instance.check_if_login_saved()
if previously_saved_login:
    print("Previously logged in")
    main_page.turn_on()
else:
    login_page.turn_on() 

 