from ast import main
from login import LoginPage
from signup import SignUpPage
from app import MainPage
import customtkinter
signup_page = SignUpPage()
main_page = MainPage()
login_page = LoginPage()
signup_page.assign_login_page(login_page)
signup_page.assign_main_page(page= main_page)
login_page.assign_main_page(page= main_page)
login_page.assign_signup_page(page=signup_page)
login_page.turn_on() 

