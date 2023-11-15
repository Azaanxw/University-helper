import email
from PIL import Image
from os import name
from tkinter import ANCHOR, LEFT
from turtle import width
from typing import Optional, Tuple, Union
import customtkinter
import time
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

        name_icon = customtkinter.CTkImage(dark_image=Image.open("Images\\user.png"),size=(30, 30))
        name_label = customtkinter.CTkLabel(master=signup_frame,text="   Full name:",image=name_icon,compound="left",font=("Bahnschrift",20))
        name_label.grid(row=0, column=0, padx=10,pady=15)
        name_entry = customtkinter.CTkEntry(master=signup_frame,width=200)
        name_entry.grid(row=0, column=1, padx=10, pady=15)

       
        
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
        name_entry.bind("<Enter>", lambda event,button=name_entry: on_enter(event,button))
        name_entry.bind("<Leave>", lambda event,button=name_entry: on_leave(event,button))
        email_entry.bind("<Enter>", lambda event,button=email_entry: on_enter(event,button))
        email_entry.bind("<Leave>", lambda event,button=email_entry: on_leave(event,button))
        password_entry.bind("<Enter>", lambda event,button=password_entry: on_enter(event,button))
        password_entry.bind("<Leave>", lambda event,button=password_entry: on_leave(event,button))
        confirm_password_entry.bind("<Enter>", lambda event,button=confirm_password_entry: on_enter(event,button))
        confirm_password_entry.bind("<Leave>", lambda event,button=confirm_password_entry: on_leave(event,button))
        signup_frame.grid_rowconfigure(4, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)
        def validateSignUp ():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if not name or not email or not password or not confirm_password:
                CTkMessagebox(title="Error",message="Please fill in everything!",icon="cancel",width=375,height=150)
                return
            #FUNCTIONS
            def has_number(string):
                    return re.search('\d',string)
            def has_space(string):
                  return ' ' in string
            def is_valid_email(email):
                email_pattern  = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                return re.match(email_pattern,email)
            def has_uppercase(password):
                return any(char.isupper() for char in password)    
            def valid_password(password):
                if len(password) < 6:
                    return "Password is too short!"
                    
                def has_number(password):
                        return any(char.isdigit() for char in password) 
                if not has_uppercase(password):
                    return "Password must contain an uppercase!"
                 
                if not has_number(password):
                      return "Password must contain at least 1 digit!"
                        
                
                    
            if has_number(name):
                    CTkMessagebox(title="Error",message="Numbers not allowed when giving name",icon="cancel",width=375,height=150)
                    return
            if not has_space(name):
                    CTkMessagebox(title="Error",message="Full name required, only 1 was given",icon="cancel",width=375,height=150)
                    return
            if not is_valid_email(email):
                    CTkMessagebox(title="Error",message="Invalid email, try again!",icon="cancel",width=375,height=150)
                    return 
            
            msg = valid_password(password)
            if msg:
                    CTkMessagebox(title="Error",message=msg,icon="cancel",width=375,height=150)
                    return
            if not password == confirm_password:
                    CTkMessagebox(title="Error",message="Password is not the same as the one entered in confirm password!",icon="cancel",width=375,height=150)
                    return
            print("Passed all checks!")
        signup_button = customtkinter.CTkButton(master=self,text="SIGN UP",corner_radius=10,border_width = 3,border_color = "green",font=("Tahoma Bold",20),command=validateSignUp)
        signup_button.pack(padx=10, pady=10)

        
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


    def turn_on(self):
         self.deiconify()
         self.mainloop()
    def turn_off(self):
         self.withdraw()