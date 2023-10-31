from typing import Optional, Tuple, Union
import customtkinter
import time
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