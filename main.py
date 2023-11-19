## IMPORTS ##
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

# Starts up the login page as the first page to be shown
login_page.turn_on() 
 
 