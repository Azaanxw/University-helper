from typing import Optional, Tuple, Union
import customtkinter
import sqlite3
from functools import partial
from CTkMessagebox import CTkMessagebox
icon_path = "Images\\diploma icon.ico"    
from dataBase import DataBase
db_instance = DataBase() #creates an instance of the database to interact with
class MainPage(customtkinter.CTk): 
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):  # default settings for the page
        super().__init__(fg_color, **kwargs)
        #Setup for the main app window
        self.title("University Helper")
        self.geometry("920x600")
        self.iconbitmap(default=icon_path)
        self.resizable(False,False) 
        def back_to_login(self): # Function that sends user back to login page and logs them out when the button is clicked
            db_instance.delete_saved_login() # Deletes the previous saved login in order to log them out
            self.withdraw() # Makes the main app window disappear
            self.login_page.deiconify() # Makes the login page reappear
            self.login_page.mainloop() # Puts the login page on the mainloop
        self.return_to_login_button = customtkinter.CTkButton(master=self,text="LOG OUT",bg_color="transparent",fg_color="#800000",font=("Nunito",16,"normal"),text_color="#F9F6EE",hover=False,corner_radius=5,command=partial(back_to_login,self))
        self.return_to_login_button.pack(side=customtkinter.BOTTOM,pady=5) # Places the log out button at the bottom with some y padding

        #Functions for when the house is hovered on the LOG OUT button (changes color and font weight)
        def on_enter_return_login_button(event):
            self.return_to_login_button.configure(text_color="#EDEADE",font=("Nunito",16,"bold"))
        
        def on_leave_return_login_button(event):
            self.return_to_login_button.configure(text_color="#F9F6EE",cursor="hand2",font=("Nunito",16,"normal"))
    
        #Binds functions to events for the back to login button
        self.return_to_login_button.bind("<Enter>",on_enter_return_login_button) 
        self.return_to_login_button.bind("<Leave>",on_leave_return_login_button)

    def assign_login_page(self,page):
             self.login_page = page # assigns the login page to the main application
    def turn_off(self):
            self.withdraw() # makes the window disappear
    def turn_on(self):
         self.deiconify() # makes the window reappear
         self.mainloop() # makes the window the mainloop