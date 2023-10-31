from login import LoginPage
from signup import SignUpPage
import time
import customtkinter
from CTkMessagebox import CTkMessagebox
signup_page = SignUpPage()
login_page = LoginPage(signup_page=signup_page)
signup_page.assign_login_page(login_page)
login_page.turn_on()
import time
import customtkinter
from CTkMessagebox import CTkMessagebox