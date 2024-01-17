from typing import Optional, Tuple, Union
import customtkinter
import sqlite3
from emailSender import EmailSender
import time
from functools import partial
from CTkMessagebox import CTkMessagebox
icon_path = "Images\\diploma icon.ico"    
from dataBase import DataBase
db_instance = DataBase() #creates an instance of the database to interact with
class MainPage(customtkinter.CTk): 
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):  # default settings for the page
        super().__init__(fg_color, **kwargs)
        #Setup for the main app window
        self.title("University Helper")
        self.geometry("920x600")
        self.iconbitmap(default=icon_path)
        self.resizable(False,False) 
        self.current_time = time.time()
        self.last_button_press_time = time.time()
        self.button_press_delay = 0.5
        self.total_hours_worked = 0
        self.total_seconds_worked = 0
        def back_to_login(self): # Function that sends user back to login page and logs them out when the button is clicked
            db_instance.delete_saved_login() # Deletes the previous saved login in order to log them out
            self.withdraw() # Makes the main app window disappear
            self.login_page.deiconify() # Makes the login page reappear
            self.login_page.mainloop() # Puts the login page on the mainloop
        self.return_to_login_button = customtkinter.CTkButton(master=self,text="LOG OUT",bg_color="transparent",fg_color="#800000",font=("Nunito",16,"normal"),text_color="#F9F6EE",hover=False,corner_radius=5,command=partial(back_to_login,self))
        self.return_to_login_button.pack(side=customtkinter.BOTTOM,pady=5) # Places the log out button at the bottom with some y padding

        #Functions for when the house is hovered on the LOG OUT button (changes color and font weight)
        def on_enter_return_login_button(event):
            self.return_to_login_button.configure(text_color="#EDEADE",font=("Nunito",16,"bold"))
        
        def on_leave_return_login_button(event):
            self.return_to_login_button.configure(text_color="#F9F6EE",cursor="hand2",font=("Nunito",16,"normal"))

        #Binds functions to events for the back to login button
        self.return_to_login_button.bind("<Enter>",on_enter_return_login_button) 
        self.return_to_login_button.bind("<Leave>",on_leave_return_login_button)

        #Features (Pomodoro timer)
        pomodoro_container = customtkinter.CTkFrame(self)
        pomodoro_container.pack(side=customtkinter.TOP, pady=10)

        # Label for indicating Pomodoro timer
        pomodoro_label = customtkinter.CTkLabel(pomodoro_container, text="Pomodoro Timer", font=("Nunito", 18, "bold"))
        pomodoro_label.pack(side=customtkinter.TOP, pady=10)

        # Create labels for displaying the timer and current mode
        self.timer_label = customtkinter.CTkLabel(pomodoro_container, text="25:00", font=("Nunito", 16, "normal"))
        self.timer_label.pack(side=customtkinter.TOP, pady=10)

        self.mode_label = customtkinter.CTkLabel(pomodoro_container, text="Work Mode", font=("Nunito", 14, "normal"),)
        self.mode_label.pack(side=customtkinter.TOP)

        button_frame = customtkinter.CTkFrame(pomodoro_container)
        button_frame.pack(side=customtkinter.TOP, pady=10)

        # Entry widgets for customizing work and break durations
         # Label for work duration
        self.label_work = customtkinter.CTkLabel(pomodoro_container, text="Work Duration (min):", font=("Nunito", 12, "normal"))
        self.label_work.pack(side=customtkinter.TOP, pady=5)

        
        # Entry for work duration
        self.work_entry = customtkinter.CTkEntry(pomodoro_container, font=("Nunito", 12, "normal"))
        self.work_entry.insert(0, "25")  # Default work duration
        self.work_entry.pack(side=customtkinter.TOP, padx=5)

        # Label for break duration
        label_break = customtkinter.CTkLabel(pomodoro_container, text="Break Duration (min):", font=("Nunito", 12, "normal"))
        label_break.pack(side=customtkinter.TOP, pady=5)

        self.break_entry = customtkinter.CTkEntry(pomodoro_container, font=("Nunito", 12, "normal"))
        self.break_entry.insert(0, "5")  # Default break duration
        self.break_entry.pack(side=customtkinter.LEFT, padx=5)

        # Set initial values
        self.seconds_left = int(self.work_entry.get()) * 60
        self.is_break = False
        self.is_running = False
         # Create additional "Reset" button
        self.reset_button = customtkinter.CTkButton(button_frame, text="Reset", bg_color="transparent", fg_color="#FF0000",
                                                     font=("Nunito", 14, "normal"), text_color="#F9F6EE", hover=False,
                                                     corner_radius=5, command=self.reset_timer)
        self.reset_button.pack(side=customtkinter.LEFT, padx=5)

        self.update_timer()
        # Button to start/stop the timer
        self.start_stop_button = customtkinter.CTkButton(button_frame, text="Start", bg_color="transparent",
                                                          font=("Nunito", 14, "normal"), text_color="#F9F6EE", hover=False,
                                                          corner_radius=5, command=self.toggle_timer)
        self.start_stop_button.pack(side=customtkinter.LEFT, padx=5)

          # Create a label for displaying total time worked
        self.total_hours_label = customtkinter.CTkLabel(pomodoro_container, text="Total Time Worked: 00h 00m", font=("Nunito", 14, "normal"))
        self.total_hours_label.pack(side=customtkinter.TOP, pady=10)
        # Set initial values
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60  # 5 minutes in seconds
        self.seconds_left = self.work_duration
        self.is_break = False

        # Update the timer initially
        self.update_timer()
        self.timer_label.pack(side=customtkinter.TOP, pady=10)
        self.mode_label.pack(side=customtkinter.TOP)
        self.work_entry.pack(side=customtkinter.TOP, padx=5, pady=5)
        self.break_entry.pack(side=customtkinter.TOP, padx=5, pady=5)
        self.start_stop_button.pack(side=customtkinter.TOP, padx=5, pady=5)

        # Bind the event to the "Start" button
        pomodoro_container.pack(side=customtkinter.TOP, anchor='ne', pady=10)
        self.emailPageAlreadyExists = False
        # Email sender
        email_container = customtkinter.CTkFrame(self)
        email_container.pack(side=customtkinter.TOP, pady=30,padx=60, anchor="ne")
        def setup_email_page():
            if self.emailPageAlreadyExists:
                email_page.turn_on()
            else:
                email_page = EmailSender(self)
                email_page.turn_on()
                self.emailPageAlreadyExists = True
        
    
        email_label = customtkinter.CTkLabel(email_container, text="Email Sender", font=("Nunito", 18, "bold"))
        email_label.pack(side=customtkinter.TOP, pady=10,padx=20)
        send_button = customtkinter.CTkButton(email_container, text="Send Email",command=setup_email_page)
        send_button.pack(pady=10,padx=20)


    def toggle_timer(self):
        self.current_time = time.time()
        if self.current_time - self.last_button_press_time >= self.button_press_delay:
            if self.is_running:
                self.stop_timer()
            else:
                self.start_timer()

    

    def start_timer(self):
        self.current_time = time.time()
        if self.current_time - self.last_button_press_time >= self.button_press_delay:
            if not self.is_running:
                self.is_running = True
                self.start_stop_button.configure(text="Stop", fg_color="#FF0000")  # Red for stop button
                self.reset_button.configure(state="disabled")  # Disable reset button while running
                self.update_timer()
                 # Record the starting time for accurate time tracking
                self.start_time = time.time()
         

    def update_total_hours(self):
        total_hours, total_minutes = divmod(self.total_seconds_worked // 60, 60)
        time_format = "{:02.0f}h {:02.0f}m".format(total_hours, total_minutes)
        self.total_hours_label.configure(text=f"Total Time Worked: {time_format}")

    def stop_timer(self):
        self.current_time = time.time()
        if self.current_time - self.last_button_press_time >= self.button_press_delay:
            if self.is_running:
                self.is_running = False
                self.start_stop_button.configure(text="Start", fg_color="#008000")  # Green for start button
                self.reset_button.configure(state="normal")  # Enable reset button when stopped
                # Update total seconds worked based on the elapsed time since starting the timer
                self.total_seconds_worked += time.time() - self.start_time
                self.update_total_hours()  # Update the total hours label
                # Only update the timestamp when stopping the timer
                self.last_button_press_time = self.current_time

    def reset_timer(self):
        self.stop_timer()
        self.initialize_timer()
        self.update_timer()
        self.start_timer()
        self.stop_timer()
        self.total_hours_worked = 0
        self.update_total_hours()
    
    def initialize_timer(self):
        self.work_duration = int(self.work_entry.get()) * 60
        # Set initial values for the timer
        self.seconds_left = self.work_duration
        self.is_break = False
        self.is_running = False
        self.mode_label.configure(text="Work Mode")  # Initial mode is work mode

    def update_timer(self):
        if self.is_running:
            # Format the time in MM:SS
            minutes, seconds = divmod(self.seconds_left, 60)
            time_format = "{:02d}:{:02d}".format(minutes, seconds)

            # Update the timer label
            self.timer_label.configure(text=time_format)

            # Check if the timer reaches 0
            if self.seconds_left == 0:
                # Toggle between work and break modes
                self.is_break = not self.is_break
                if self.is_break:
                    self.seconds_left = int(self.break_entry.get()) * 60
                    self.mode_label.configure(text="Break Mode")  # Green for break mode
                else:
                    self.seconds_left = int(self.work_entry.get()) * 60
                    self.mode_label.configure(text="Work Mode")  # Red for work mode

            # Check if the time since the last button press is less than 1 second
            if self.current_time is not None and self.current_time - self.last_button_press_time < 1:
                # Do not decrement the seconds
                pass
            else:
                # Decrement the seconds
                self.seconds_left -= 1

            # Schedule the update every 1000 milliseconds (1 second)
            self.after(1000, self.update_timer)




    def assign_login_page(self,page):
             self.login_page = page # assigns the login page to the main application
    def turn_off(self):
            self.withdraw() # makes the window disappear
    def turn_on(self):
         self.deiconify() # makes the window reappear
         self.mainloop() # makes the window the mainloop