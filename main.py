## IMPORTS ##
import sqlite3
from login import LoginPage
from signUp import SignUpPage
from app import MainPage
from dataBase import DataBase
db_instance = DataBase() # creates an instance of the database class
db_instance.setup_database() #setups up the database 
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
previously_saved_login = db_instance.check_if_login_saved() # checks if user has logged in before and if they pressed remember me for the next time they login
# If they pressed remember me and logged in before, it redirects them straight to the main page instead of the login page for new users
if previously_saved_login: 
    print("Previously logged in")
    main_page.turn_on()
else:
    login_page.turn_on() 
# TO DO LIST
# FEATURES TO ADD TO THE MAIN APP
# OTP email token prompt and use it to send email to uni/lecturers (for common reasons e.g. sick)
# Notifier for train strikes - check for location maybe?
# Deadline notifier ( shows you how many days left till a certain deadline E.g. (exams,holiday,results) - custom
# Checklist for doing a habit daily e.g. (Study for # number of hours) - custom 
