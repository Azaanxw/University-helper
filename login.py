## IMPORTS ##
from typing import  Tuple
import customtkinter
from dataBase import DataBase
from CTkMessagebox import CTkMessagebox

# Customtkinter settings       
customtkinter.set_appearance_mode("system") # Sets appearance mode based on system settings (Lights or Dark)
customtkinter.set_default_color_theme("green") # Sets color theme to green

icon_path = "Images\\diploma icon.ico" # Icon path for login window 
db_instance = DataBase() # creates an instance of the database to interact with
# Login class 
class LoginPage(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs): 
        super().__init__(fg_color, **kwargs)
        self.title("Login") # Name of the login window
        self.geometry("450x350") # Size of the login window
        self.iconbitmap(default=icon_path) # Icon that will be displayed for the login window
        self.resizable(False,False) # Makes the window non-resizable 

        frame = customtkinter.CTkFrame(master=self) # Frame for the login page
        frame.pack(padx=0,pady=(10,5),fill="both",expand=True) 

        label = customtkinter.CTkLabel(master=frame,text="Login",font =("Arial",35)) # Title label 
        label.pack(pady=12,padx=10)
    
        #Login page entries
        username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        username_entry.pack(pady=12,padx=10)
        password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password",show="*") 
        password_entry.pack(pady=12,padx=10)

        def login(): # Function that gets executed every time the "Login" button is pressed
            # gets the string value at the input box
            self.username = username_entry.get() # gets username value
            self.password = password_entry.get() # gets password value
            self.remember_me = checkbox.get() # checks if remember me checkbox is enabled or not (0 or 1)
            if self.username:
                username_words = self.username.split() #splits the username string into a list of words depending on if there is a space or not
                self.username = "".join(username_words) #joins the words together with no spaces
            if not self.username:  #checks if user has inputted anything in the input box
                CTkMessagebox(title="Error",message="Please provide a username",icon="cancel",width=375,height=150)
                return
            elif not self.password: #checks if user has inputted anything in the input box
                CTkMessagebox(title="Error",message="Please provide a password",icon="cancel",width=375,height=150)
                return
            has_correct_login = db_instance.check_database(username=self.username,password=self.password,remember_me_boolean=self.remember_me) #returns Boolean depending on if the login details are correct
            if has_correct_login: # Checks to see if the login details are correct and if they are, it redirects the user to the main page
                CTkMessagebox(title="Login successful!",message=f"Welcome {self.username},you are now logged in!",icon="check",fade_in_duration=1) # Message box if the user successfully logs in with a fade effect
                setup_main_page(self) #Setups up the main application window
            else:
                CTkMessagebox(title="Error",message="Username/password is invalid!",icon="cancel",width=375,height=150) # Gives error if login info doesn't exist in database
                    
        #Login button
        login_button = customtkinter.CTkButton(master=frame,text="Login",command=login)
        login_button.pack(pady=12,padx=10)

        #Checkbox for "Remember me" when logging in
        checkbox = customtkinter.CTkCheckBox(master=frame,text="Remember Me")
        checkbox.pack(pady=12,padx=10)

        #Signup button functions
        def on_enter_signup(event): # Changes text color and font to bold when mouse hovers on the label
            signup_label.configure(text_color="#30C30F",font=("Helvetica",15,"bold"))
        
        def on_leave_signup(event): # Changes text color and font to underline when mouse exits the label
            signup_label.configure(text_color="#2FA572",cursor="hand2",font=("Helvetica",15,"underline"))
        
        def on_click_signup(event): # Calls up the signup setup function when button is clicked
            setup_signup_page(self) 

        #Signup labels 
        signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account? Sign up here", fg_color="transparent")
        signup_label.configure(font=("Helvetica",15,"underline"),text_color="#2FA572",underline=True)
        signup_label.pack(side="bottom") # makes the sign up button appear at the bottom

        #Signup label binding events
        signup_label.bind("<Enter>",on_enter_signup) 
        signup_label.bind("<Leave>",on_leave_signup)
        signup_label.bind("<Button-1>",on_click_signup)
        
        #Signup functions
        def setup_signup_page(self): # Sets up the signup window and makes the login window disappear
             self.withdraw()
             self.signup_page.deiconify()
             self.signup_page.mainloop()
        def setup_main_page(self): # Makes the login window disappear and puts the main page on the mainloop
             self.withdraw()
             self.main_page.deiconify()
             self.main_page.mainloop()

    #Public login functions to be used by main.py
    def assign_main_page(self,page):
             self.main_page = page # assigns the main page to the object
    def assign_signup_page(self,page):
             self.signup_page = page # assigns the signup page to the object
    def turn_off(self):
            self.withdraw() # makes the window disappear
    def turn_on(self):
         self.deiconify() # makes the window reappear
         self.mainloop() # makes the window the mainloop