## IMPORTS ##
from PIL import Image
from os import name
from dataBase import DataBase
from tkinter import ANCHOR, LEFT
from typing import  Tuple
import customtkinter
import sqlite3
from functools import partial
from CTkMessagebox import CTkMessagebox
import re

icon_path = "Images\\diploma icon.ico"  # Icon path for Signup tab
def exit_application(): # Exits the signup page w out any errors from callbacks etc
        import sys
        sys.exit(0)
db_instance = DataBase() # creates an instance of the database to interact with it
#Signup class
class SignUpPage(customtkinter.CTk): 
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Sign up") #Name of the signup window
        self.geometry('620x400') # Size of the signup window
        self.iconbitmap(default=icon_path) # Icon that will be displayed for the login window
        self.resizable(False,False) # Makes the window non-resizable 
        def on_closing():
                self.destroy()  # Close the main window
                exit_application()  # Call a function to exit the application gracefully
        self.protocol("WM_DELETE_WINDOW", on_closing) # Assigns on_closing function when the window is destroyed
        def back_to_login(self): # Function that sends user back to login page when the button is clicked
            self.withdraw() # Makes the signup window disappear
            self.login_page.deiconify() # Makes the login page reappear
            self.login_page.mainloop() # Puts the login page on the mainloop
        #Signup page title
        signup_label = customtkinter.CTkLabel(master=self,text="Create your account",font =("Arial",35))
        signup_label.pack(pady=12,padx=10)

        #Signup frame setup (using a different frame so that i can use the grid method as the current self is already set up by pack)
        signup_frame = customtkinter.CTkFrame(master=self,fg_color="transparent")
        signup_frame.pack(padx=10,pady=10)

        #Labels and inputs for the sign up page
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

        #Makes the input bar glow when hovered on
        def on_enter(event,entry_box): 
             entry_box.configure(border_color="#42b0f5") # Changes input border to blue
        def on_leave(event,entry_box):
              entry_box.configure(border_color="#565B5E") # Changes input border color back to dark gray
        
        #Binds all the entry boxes to the given functions
        user_entry.bind("<Enter>", lambda event,entry_box=user_entry: on_enter(event,entry_box))
        user_entry.bind("<Leave>", lambda event,entry_box=user_entry: on_leave(event,entry_box))
        email_entry.bind("<Enter>", lambda event,entry_box=email_entry: on_enter(event,entry_box))
        email_entry.bind("<Leave>", lambda event,entry_box=email_entry: on_leave(event,entry_box))
        password_entry.bind("<Enter>", lambda event,entry_box=password_entry: on_enter(event,entry_box))
        password_entry.bind("<Leave>", lambda event,entry_box=password_entry: on_leave(event,entry_box))
        confirm_password_entry.bind("<Enter>", lambda event,entry_box=confirm_password_entry: on_enter(event,entry_box))
        confirm_password_entry.bind("<Leave>", lambda event,entry_box=confirm_password_entry: on_leave(event,entry_box))
        
        #Signup frame grid setup
        signup_frame.grid_rowconfigure(4, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)
        def validateSignUp (): # Checks if user can signup or not
            #Gets the current string values from input box
            user = user_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            if user:
                user_words = user.split() #splits the username string into a list of words depending on if there is a space or not
                user = "".join(user_words) #joins the words together with no spaces
            if not user or not email or not password or not confirm_password: # Checks if the string is empty or not
                CTkMessagebox(title="Error",message="Please fill in everything!",icon="cancel",width=375,height=150)
                return
            #FUNCTIONS
            def is_valid_email(email): # returns whether email matches the pattern
                email_pattern  = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                return re.match(email_pattern,email)
            
            def has_uppercase(password): # Checks if at least 1 char has an uppercase
                return any(char.isupper() for char in password) 

            def valid_user(user): # Sees if username meets requirement and if it already exists or not
                does_username_exist = db_instance.does_user_exist(user=user)
                if does_username_exist:
                    return 'Username already exists! Try a different one.'
                if len(user) < 3: # Checks if the length of the user is less than 3
                     return 'Username is too short!'
                special_chars = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/" 
                for char in user: # Loops through every character in user
                     if char in set(special_chars): # Checks if any of the characters in user have a special character 
                               return 'Special characters are not allowed when creating usernames!'
                return          
            def valid_password(password): # Checks if password meets all given conditions
                if len(password) < 6:  # Checks if password length is shorter than 6 
                    return "Password is too short!"
                    
                def has_number(password): # Checks if password has at least 1 number 
                        return any(char.isdigit() for char in password) 
                if not has_uppercase(password): # Checks if password has at least 1 uppercase
                    return "Password must contain an uppercase!"
                 
                if not has_number(password): # Returns message if password doesn't have atleast 1 number
                      return "Password must contain at least 1 digit!"
                return
            does_user_exist = db_instance.does_user_exist(user,password)
            # Message input boxes for errors
            if not is_valid_email(email):
                    CTkMessagebox(title="Error",message="Invalid email, try again!",icon="cancel",width=375,height=150)
                    return 
            
            pass_msg= valid_password(password)
            if pass_msg: # checks if there's an error message in pass_msg and if there is then it displays it in the message box
                    CTkMessagebox(title="Error",message=pass_msg,icon="cancel",width=375,height=150)
                    return
            if not password == confirm_password: # checks to see if the password string is the same as the one entered in confirm_password
                    CTkMessagebox(title="Error",message="Password is not the same as the one entered in confirm password!",icon="cancel",width=375,height=150)
                    return
            
            user_msg = valid_user(user) #checks to see if the username is valid
            if user_msg:
                    CTkMessagebox(title="Error",message=user_msg,icon="cancel",width=375,height=150)
                    return
            if does_user_exist: # Checks to see if user already exists
                  CTkMessagebox(title="Error",message="Account already exists! Please login",icon="cancel",width=375,height=150)
                  return
            
            else: # Executes if user meets all requirements for creating account
                print("Passed all checks!")
                db_instance.add_new_user(user=user,email=email,password=password) # Adds the new data to the dataset
                CTkMessagebox(title="Account created!",message="Your account has been successfully created! You will now be redirected to main page",icon="check",fade_in_duration=1)
                setup_main_page(self) # Sets up the main page
               
        #Signup button 
        signup_button = customtkinter.CTkButton(master=self,text="SIGN UP",corner_radius=10,border_width = 3,border_color = "green",font=("Tahoma Bold",20),command=validateSignUp)
        signup_button.pack(padx=10, pady=10)

        #Signup Functions
        def setup_main_page(self):
             self.withdraw()
             self.main_page.deiconify()
             self.main_page.mainloop()
        #Functions for when mouse is hovered over the login button (changes font weight and text color)
        def on_enter_login_button(event):
            back_to_login_button.configure(text_color="#30C30F",font=("Helvetica",15,"bold"))
        
        def on_leave_login_button(event):
            back_to_login_button.configure(text_color="#DCE4EE",cursor="hand2",font=("Helvetica",15,"normal"))
        
        #Back to login button
        back_to_login_button = customtkinter.CTkButton(master=self,text="Back to login",bg_color="transparent",fg_color="transparent",font=("Helvetica",15,"normal"),hover=False,command=partial(back_to_login,self))
        back_to_login_button.pack(side=customtkinter.BOTTOM)

        #Binds functions to events for the back to login button
        back_to_login_button.bind("<Enter>",on_enter_login_button) 
        back_to_login_button.bind("<Leave>",on_leave_login_button)
    #PUBLIC Signup functions
    def assign_login_page(self,page): # Assigns the login page 
             self.login_page = page

    def assign_main_page(self,page): # Assigns the main page
             self.main_page = page

    def turn_on(self): # Makes the page visible
         self.deiconify()
         self.mainloop()
         
    def turn_off(self):  # Hides the page
         self.withdraw()