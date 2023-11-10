from login import LoginPage
from signup import SignUpPage
import customtkinter
signup_page = SignUpPage()
login_page = LoginPage(signup_page=signup_page)
signup_page.assign_login_page(login_page)
login_page.turn_on() 