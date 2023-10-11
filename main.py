import customtkinter

#GUI settings
customtkinter.set_appearance_mode("system") # Sets appearance mode based on system settings (Lights or Dark)
customtkinter.set_default_color_theme("green") # Sets dark blue theme 

#App setup
app = customtkinter.CTk() #adds CTk window 
app.title("University Helper") #name of the app
app.geometry("450x350")#size of the window
icon_path = "Images\\diploma icon.ico"
app.iconbitmap(default=icon_path)
app.resizable(False, False) # makes the window non-resizable

frame = customtkinter.CTkFrame(master=app)

def setup_login_page():

    #Frame Setup 
    frame.pack(padx=0,pady=(10,5),fill="both",expand=True)
    label = customtkinter.CTkLabel(master=frame,text="Login",font =("Arial",35))
    label.pack(pady=12,padx=10)

    #Login page buttons
    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
    username_entry.pack(pady=12,padx=10)
    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password",show="*")
    password_entry.pack(pady=12,padx=10)

    #Login button functions
    def login():
        print("Logging in")

    def signup():
        print("Sign up")

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
        print("test")
        signup()
        frame.pack_forget()  
    #Signup button
    signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account? Sign up here", fg_color="transparent")
    signup_label.configure(font=("Helvetica",15,"underline"),text_color="#2FA572",underline=True)
    signup_label.pack(side="bottom") # makes the sign up button appear at the bottom
    signup_label.bind("<Enter>",on_enter_signup) 
    signup_label.bind("<Leave>",on_leave_signup)
    signup_label.bind("<Button-1>",on_click_signup)

def signup_page():
    frame2 = customtkinter.CTkFrame(master=app)
    frame2.pack(padx=0,pady=(10,5),fill="both",expand=True)
    progress_bar = customtkinter.CTkProgressBar(master=frame2,orientation="horizontal")
    progress_bar.pack(pady=10,padx=10)
setup_login_page()
print("First commit")
app.mainloop()