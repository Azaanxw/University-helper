from typing import Optional, Tuple, Union
import customtkinter
import time
from functools import partial
from CTkMessagebox import CTkMessagebox
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
        back_to_login_button = customtkinter.CTkButton(master=self,text="Login",command=partial(back_to_login,self))
        back_to_login_button.pack(pady=12,padx=10)
    def assign_login_page(self,page):
             self.login_page = page
    

    def turn_on(self):
         self.deiconify()
         self.mainloop()
    def turn_off(self):
         self.withdraw()