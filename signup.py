import email
from PIL import Image
from os import name
from tkinter import ANCHOR, LEFT
from turtle import width
from typing import Optional, Tuple, Union
import customtkinter
import time
import sqlite3
from functools import partial
from CTkMessagebox import CTkMessagebox
import re

def exit_application():
        import sys
        sys.exit(0)  # Exit the application gracefully
icon_path = "Images\\diploma icon.ico" 
class SignUpPage(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Sign up")
        self.geometry('620x400')
        self.iconbitmap(default=icon_path)
        self.resizable(False,False)
        def on_closing():
                self.destroy()  # Close the main window
                exit_application()  # Call a function to exit the application gracefully
        self.protocol("WM_DELETE_WINDOW", on_closing)
        def back_to_login(self):
            self.withdraw()
            self.login_page.deiconify()
            self.login_page.mainloop()
        signup_label = customtkinter.CTkLabel(master=self,text="Create your account",font =("Arial",35))
        signup_label.pack(pady=12,padx=10)
        signup_frame = customtkinter.CTkFrame(master=self,fg_color="transparent")
        signup_frame.pack(padx=10,pady=10)

        user_icon = customtkinter.CTkImage(dark_image=Image.open("Images\\user.png"),size=(30, 30))
        user_label = customtkinter.CTkLabel(master=signup_frame,text="  Username:",image=user_icon,compound="left",font=("Bahnschrift",20))
        user_label.grid(row=0, column=0, padx=10,pady=15)
        user_entry = customtkinter.CTkEntry(master=signup_frame,width=200)
        user_entry.grid(row=0, column=1, padx=10, pady=15)

       
        
        email_icon = customtkinter.CTkImage(dark_image=Image.open("Images\\email.png"),size=(30, 30))
        email_label = customtkinter.CTkLabel(master=signup_frame,text="   Email:",image=email_icon, compound="left",font=("Bahnschrift",20))
        email_label.grid(row=1, column=0, padx=10, pady=15)
        email_entry = customtkinter.CTkEntry(master=signup_frame,width=200)
        email_entry.grid(row=1, column=1, padx=10, pady=15)

        password_icon = customtkinter.CTkImage(dark_image=Image.open("Images\\padlock.png"),size=(30, 30))
        password_label = customtkinter.CTkLabel(master=signup_frame,text="   Password:",image=password_icon,compound="left",font=("Bahnschrift",20))
        password_label.grid(row=2, column=0, padx=10, pady=15)
        password_entry = customtkinter.CTkEntry(master=signup_frame,width=200)
        password_entry.grid(row=2, column=1, padx=10, pady=15)

        confirm_password_label = customtkinter.CTkLabel(master=signup_frame,text="   Confirm password:",image=password_icon,compound="left",font=("Bahnschrift",20))
        confirm_password_label.grid(row=3, column=0, padx=10, pady=10)
        confirm_password_entry = customtkinter.CTkEntry(master=signup_frame,width=200)
        confirm_password_entry.grid(row=3, column=1, padx=10, pady=15)
        #BINDING EVENTS 
        def on_enter(event,button): 
             button.configure(border_color="#42b0f5")
        def on_leave(event,button):
              button.configure(border_color="#565B5E")
        user_entry.bind("<Enter>", lambda event,button=user_entry: on_enter(event,button))
        user_entry.bind("<Leave>", lambda event,button=user_entry: on_leave(event,button))
        email_entry.bind("<Enter>", lambda event,button=email_entry: on_enter(event,button))
        email_entry.bind("<Leave>", lambda event,button=email_entry: on_leave(event,button))
        password_entry.bind("<Enter>", lambda event,button=password_entry: on_enter(event,button))
        password_entry.bind("<Leave>", lambda event,button=password_entry: on_leave(event,button))
        confirm_password_entry.bind("<Enter>", lambda event,button=confirm_password_entry: on_enter(event,button))
        confirm_password_entry.bind("<Leave>", lambda event,button=confirm_password_entry: on_leave(event,button))
        signup_frame.grid_rowconfigure(4, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)
        def validateSignUp ():
            user = user_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if not user or not email or not password or not confirm_password:
                CTkMessagebox(title="Error",message="Please fill in everything!",icon="cancel",width=375,height=150)
                return
            #FUNCTIONS
            def is_valid_email(email):
                email_pattern  = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                return re.match(email_pattern,email)
            def has_uppercase(password):
                return any(char.isupper() for char in password) 

            def valid_user(user):
                #CHECKS THE DATABASE
                conn = sqlite3.connect('database.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                dataset = cursor.fetchall()
                for data in dataset:
                    if data['username'] == user:
                        conn.close()
                        return 'Username already exists! Try a different one.'
                conn.close()
                if len(user) < 3:
                     return 'Username is too short!'
                special_chars = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/"
                for char in user:
                     if char in set(special_chars):
                               return 'Special characters are not allowed when creating usernames!'
                return          
            def valid_password(password):
                if len(password) < 6:
                    return "Password is too short!"
                    
                def has_number(password):
                        return any(char.isdigit() for char in password) 
                if not has_uppercase(password):
                    return "Password must contain an uppercase!"
                 
                if not has_number(password):
                      return "Password must contain at least 1 digit!"
                return
            def does_user_exist():
                #CHECKS THE DATABASE
                conn = sqlite3.connect('database.db')
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                dataset = cursor.fetchall()
                for data in dataset:
                    if data['username'] == user and data['password'] == password:
                        conn.close()
                        return True
                conn.close()
                return False
            
            if not is_valid_email(email):
                    CTkMessagebox(title="Error",message="Invalid email, try again!",icon="cancel",width=375,height=150)
                    return 
            
            pass_msg= valid_password(password)
            if pass_msg:
                    CTkMessagebox(title="Error",message=pass_msg,icon="cancel",width=375,height=150)
                    return
            if not password == confirm_password:
                    CTkMessagebox(title="Error",message="Password is not the same as the one entered in confirm password!",icon="cancel",width=375,height=150)
                    return
            user_msg = valid_user(user)
            if user_msg:
                    CTkMessagebox(title="Error",message=user_msg,icon="cancel",width=375,height=150)
                    return
            if does_user_exist():
                  CTkMessagebox(title="Error",message="Account already exists! Please login",icon="cancel",width=375,height=150)
                  return
            
            else:
                print("Passed all checks!")
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('INSERT OR IGNORE INTO users (username,email,password) VALUES (?,?,?)', (user,email,password))
                conn.commit()
                conn.close()
                CTkMessagebox(title="Account created!",message="Your account has been successfully created! You will now be redirected to main page",icon="check",fade_in_duration=1)
                setup_main_page(self)
        signup_button = customtkinter.CTkButton(master=self,text="SIGN UP",corner_radius=10,border_width = 3,border_color = "green",font=("Tahoma Bold",20),command=validateSignUp)
        signup_button.pack(padx=10, pady=10)
        def setup_main_page(self):
             self.withdraw()
             self.main_page.mainloop()
        
        def on_enter_login_button(event):
            back_to_login_button.configure(text_color="#30C30F",font=("Helvetica",15,"bold"))
        
        def on_leave_login_button(event):
            back_to_login_button.configure(text_color="#DCE4EE",cursor="hand2",font=("Helvetica",15,"normal"))
        back_to_login_button = customtkinter.CTkButton(master=self,text="Back to login",bg_color="transparent",fg_color="transparent",font=("Helvetica",15,"normal"),hover=False,command=partial(back_to_login,self))
        back_to_login_button.pack(side=customtkinter.BOTTOM)
        back_to_login_button.bind("<Enter>",on_enter_login_button) 
        back_to_login_button.bind("<Leave>",on_leave_login_button)
    def assign_login_page(self,page):
             self.login_page = page
    def assign_main_page(self,page):
             self.main_page = page
    
    def turn_on(self):
         self.deiconify()
         self.mainloop()
    def turn_off(self):
         self.withdraw()