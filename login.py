from tarfile import data_filter
from typing import Optional, Tuple, Union
import customtkinter
import time
import sqlite3
from CTkMessagebox import CTkMessagebox
from app import MainPage
icon_path = "Images\\diploma icon.ico"        
customtkinter.set_appearance_mode("system") # Sets appearance mode based on system settings (Lights or Dark)
customtkinter.set_default_color_theme("green")
class LoginPage(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):  # default settings for the page
        super().__init__(fg_color, **kwargs)
        self.title("Login")
        self.geometry("450x350")
        self.iconbitmap(default=icon_path)
        self.resizable(False,False)

        frame = customtkinter.CTkFrame(master=self)
        frame.pack(padx=0,pady=(10,5),fill="both",expand=True)
        label = customtkinter.CTkLabel(master=frame,text="Login",font =("Arial",35))
        label.pack(pady=12,padx=10)
    
         #Login page buttons
        username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        username_entry.pack(pady=12,padx=10)
        password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password",show="*")
        password_entry.pack(pady=12,padx=10)

        def login():
            username = username_entry.get()
            password = password_entry.get() 
            if username:
                username_words = username.split() #splits the username string into a list of words depending on if theres space or not
                username = "".join(username_words) #joins the words together with no spaces
            if not username:
                CTkMessagebox(title="Error",message="Please provide a username",icon="cancel",width=375,height=150)
                return
            elif not password:
                CTkMessagebox(title="Error",message="Please provide a password",icon="cancel",width=375,height=150)
                return

            #CHECKS THE DATABASE
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            dataset = cursor.fetchall() 
            for data in dataset:
                if data['username'] == username and data['password'] == password:
                    conn.close() 
                    self.withdraw()  #closes the previous login page
                    CTkMessagebox(title="Login successful!",message=f"Welcome {username},you are now logged in!",icon="check",fade_in_duration=1)
                    #Setup the main application window
                    setup_main_page(self)
                
            conn.close()
            CTkMessagebox(title="Error",message="Username/password is invalid!",icon="cancel",width=375,height=150)
                    
            
           
        #Login button
        login_button = customtkinter.CTkButton(master=frame,text="Login",command=login)
        login_button.pack(pady=12,padx=10)

        #Checkbox for "Remember me" when logging in
        checkbox = customtkinter.CTkCheckBox(master=frame,text="Remember Me")
        checkbox.pack(pady=12,padx=10)

        #Signup button functions
        def on_enter_signup(event):
            signup_label.configure(text_color="#30C30F",font=("Helvetica",15,"bold"))
        
        def on_leave_signup(event):
            signup_label.configure(text_color="#2FA572",cursor="hand2",font=("Helvetica",15,"underline"))
        
        def on_click_signup(event):
            setup_signup_page(self)  
        signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account? Sign up here", fg_color="transparent")
        signup_label.configure(font=("Helvetica",15,"underline"),text_color="#2FA572",underline=True)
        signup_label.pack(side="bottom") # makes the sign up button appear at the bottom
        signup_label.bind("<Enter>",on_enter_signup) 
        signup_label.bind("<Leave>",on_leave_signup)
        signup_label.bind("<Button-1>",on_click_signup)
        def setup_signup_page(self):
             self.withdraw()
             self.signup_page.deiconify()
             self.signup_page.mainloop()
        def setup_main_page(self):
             self.withdraw()
             self.main_page.mainloop()
    def assign_main_page(self,page):
             self.main_page = page
    def assign_signup_page(self,page):
             self.signup_page = page
    def turn_off(self):
            self.withdraw()
    def turn_on(self):
         self.deiconify()
         self.mainloop()