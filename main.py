import customtkinter
from CTkMessagebox import CTkMessagebox
from tkinter import *

#GUI settings
customtkinter.set_appearance_mode("system") # Sets appearance mode based on system settings (Lights or Dark)
customtkinter.set_default_color_theme("green") # Sets dark blue theme 
#Login setup
login_tab = customtkinter.CTk() #adds CTk window 
login_tab.title("University Helper") #name of the app
login_tab.geometry("450x350")#size of the window
icon_path = "Images\\diploma icon.ico"
login_tab.iconbitmap(default=icon_path)
login_tab.resizable(False, False) # makes the window non-resizable

frame = customtkinter.CTkFrame(master=login_tab)

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
        username = username_entry.get()
        if username:
            username_words = username.split() #splits the username string into a list of words depending on if theres space or not
            username = "".join(username_words) #joins the words together with no spaces
        else:
            CTkMessagebox(title="Error",message="Please provide a username",icon="cancel",width=375,height=150)
        password = password_entry.get()  
        
        if username=="admin" and password=="123":
            print(('Logged in!'))
             #closes the previous login page
            login_tab.withdraw()
            main_tab = customtkinter.CTk()
            main_tab.title("App")
            main_tab.geometry('920x600')
            main_tab.config(bg="grey")
           
            username_entry2 = customtkinter.CTkEntry(master=main_tab, placeholder_text="Username")
            username_entry2.pack(pady=12,padx=10)
            def on_closing():
                main_tab.destroy()  # Close the main window
                # Optionally, you can add code here to perform any cleanup before exiting the application.
                # For example, saving data, closing files, etc.
                exit_application()  # Call a function to exit the application gracefully

    # Set the function to handle window closure
            main_tab.protocol("WM_DELETE_WINDOW", on_closing)
        
            main_tab.mainloop()
            main_tab.mainloop()
            
        else:
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
        
    def exit_application():
        # Add code here to perform any final cleanup or exit actions.
        # For example, saving data, closing files, etc.
        import sys
        sys.exit(0)  # Exit the application gracefully

    def on_click_signup(event):
        print("test")  
    #Signup button
    signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account? Sign up here", fg_color="transparent")
    signup_label.configure(font=("Helvetica",15,"underline"),text_color="#2FA572",underline=True)
    signup_label.pack(side="bottom") # makes the sign up button appear at the bottom
    signup_label.bind("<Enter>",on_enter_signup) 
    signup_label.bind("<Leave>",on_leave_signup)
    signup_label.bind("<Button-1>",on_click_signup)

setup_login_page()
print("First commit")
print("hew")
login_tab.mainloop()