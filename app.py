from typing import Optional, Tuple, Union
import customtkinter
import sqlite3
from functools import partial
from CTkMessagebox import CTkMessagebox
icon_path = "Images\\diploma icon.ico"    
class MainPage(customtkinter.CTk): 
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):  # default settings for the page
        super().__init__(fg_color, **kwargs)
        self.title("University Helper")
        self.geometry("920x600")
        self.iconbitmap(default=icon_path)
        self.resizable(False,False) 
        username_entry2 = customtkinter.CTkEntry(master=self, placeholder_text="ENTER SMTH HERE")
        username_entry2.pack(pady=12,padx=10)
        def back_to_login(self): # Function that sends user back to login page when the button is clicked
            # Deletes the previous local_credential values if remember_me isn't true

            conn = sqlite3.connect('database.db') # connects to the database file and creates one if there isn't one already
            conn.row_factory = sqlite3.Row # returns rows as special row objects and allows to use dictionary e.g. data[username] instead of data[0]
            cursor = conn.cursor() # creates cursor object that interacts with the SQLite database
            cursor.execute('DELETE FROM local_credentials')
            conn.commit()
            conn.close() # Closes the connection (saves up on resources)
            self.withdraw() # Makes the main app window disappear
            self.login_page.deiconify() # Makes the login page reappear
            self.login_page.mainloop() # Puts the login page on the mainloop
        self.back_to_login_button = customtkinter.CTkButton(master=self,text="Back to login",bg_color="transparent",fg_color="transparent",font=("Helvetica",15,"normal"),hover=False,command=partial(back_to_login,self))
        self.back_to_login_button.pack(side=customtkinter.BOTTOM)
        def on_enter_login_button(event):
            self.back_to_login_button.configure(text_color="#30C30F",font=("Helvetica",15,"bold"))
        
        def on_leave_login_button(event):
            self.back_to_login_button.configure(text_color="#DCE4EE",cursor="hand2",font=("Helvetica",15,"normal"))
        #Binds functions to events for the back to login button
        self.back_to_login_button.bind("<Enter>",on_enter_login_button) 
        self.back_to_login_button.bind("<Leave>",on_leave_login_button)
    def assign_login_page(self,page):
             self.login_page = page # assigns the login page to the main application
    def turn_off(self):
            self.withdraw() # makes the window disappear
    def turn_on(self):
         self.deiconify() # makes the window reappear
         self.mainloop() # makes the window the mainloop