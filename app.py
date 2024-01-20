from typing import Optional, Tuple, Union
import customtkinter
import sqlite3
from emailSender import EmailSender
import time
from functools import partial
from CTkMessagebox import CTkMessagebox
from trainNotifier import RailInfoScraperApp
icon_path = "Images\\diploma icon.ico"
from dataBase import DataBase
from toDoList import ToDoList

db_instance = DataBase()  # creates an instance of the database to interact with

class MainPage(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):  
        super().__init__(fg_color, **kwargs)
        self.title("University Helper")
        self.geometry("920x650")
        self.iconbitmap(default=icon_path)
        self.resizable(True, True)
        self.current_time = time.time()
        self.last_button_press_time = time.time()
        self.button_press_delay = 0.5
        self.total_hours_worked = 0
        self.total_seconds_worked = 0
        self.is_running = False
        # LOG OUT button
        self.return_to_login_button = customtkinter.CTkButton(
            master=self, text="LOG OUT", bg_color="transparent", fg_color="#800000",
            font=("Nunito", 16, "normal"), text_color="#F9F6EE", hover=False,
            corner_radius=5, command=partial(self.back_to_login)
        )
        self.return_to_login_button.grid(row=2, column=2, pady=10)

        def on_enter_return_login_button(event):
            self.return_to_login_button.configure(text_color="#EDEADE", font=("Nunito", 16, "bold"))

        def on_leave_return_login_button(event):
            self.return_to_login_button.configure(text_color="#F9F6EE", cursor="hand2", font=("Nunito", 16, "normal"))

        self.return_to_login_button.bind("<Enter>", on_enter_return_login_button)
        self.return_to_login_button.bind("<Leave>", on_leave_return_login_button)

        # Features (Pomodoro timer)
        pomodoro_container = customtkinter.CTkFrame(self)
        pomodoro_container.grid(row=0, column=3, pady=10, padx=10, sticky='nswe')

        pomodoro_label = customtkinter.CTkLabel(
            pomodoro_container, text="Pomodoro Timer", font=("Nunito", 18, "bold")
        )
        pomodoro_label.grid(row=0, column=0, pady=10,padx=10,columnspan=2)

        self.timer_label = customtkinter.CTkLabel(
            pomodoro_container, text="25:00", font=("Nunito", 16, "normal")
        )
        self.timer_label.grid(row=1, column=0, pady=10,columnspan=2)

        self.mode_label = customtkinter.CTkLabel(
            pomodoro_container, text="Work Mode", font=("Nunito", 14, "normal")
        )
        self.mode_label.grid(row=2, column=0,columnspan=2)

        button_frame = customtkinter.CTkFrame(pomodoro_container)
        button_frame.grid(row=3, column=0, pady=10,columnspan=2)

        self.label_work = customtkinter.CTkLabel(
            pomodoro_container, text="Work Duration (min):", font=("Nunito", 12, "normal")
        )
        self.label_work.grid(row=4, column=0, pady=5)

        self.work_entry = customtkinter.CTkEntry(
            pomodoro_container, font=("Nunito", 12, "normal")
        )
        self.work_entry.insert(0, "25")
        self.work_entry.grid(row=5, column=0, padx=5)

        label_break = customtkinter.CTkLabel(
            pomodoro_container, text="Break Duration (min):", font=("Nunito", 12, "normal")
        )
        label_break.grid(row=4, column=1, pady=5)

        self.break_entry = customtkinter.CTkEntry(
            pomodoro_container, font=("Nunito", 12, "normal")
        )
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=5, column=1, padx=5)

        self.reset_button = customtkinter.CTkButton(
            button_frame, text="Reset", bg_color="transparent", fg_color="#FF0000",
            font=("Nunito", 14, "normal"), text_color="#F9F6EE", hover=False,
            corner_radius=5, command=self.reset_timer
        )
        self.reset_button.grid(row=0, column=0, padx=5)

        self.update_timer()
        self.start_stop_button = customtkinter.CTkButton(
            button_frame, text="Start", bg_color="transparent",
            font=("Nunito", 14, "normal"), text_color="#F9F6EE", hover=False,
            corner_radius=5, command=self.toggle_timer
        )
        self.start_stop_button.grid(row=0, column=1, padx=5)

        self.total_hours_label = customtkinter.CTkLabel(
            pomodoro_container, text="Total Time Worked: 00h 00m", font=("Nunito", 14, "normal")
        )
        self.total_hours_label.grid(row=6, column=0, pady=10,columnspan=2)

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.seconds_left = self.work_duration
        self.is_break = False

        self.update_timer()
        self.timer_label.grid(row=1, column=0, pady=10)
        self.mode_label.grid(row=2, column=0)
        self.work_entry.grid(row=5, column=0, padx=5, pady=5)
        self.break_entry.grid(row=5, column=1, padx=5, pady=5)
        self.start_stop_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.emailPageAlreadyExists = False

        email_container = customtkinter.CTkFrame(self)
        email_container.grid(row=0, column=1, pady=30, padx=10, sticky="nsew")

        def setup_email_page():
            if self.emailPageAlreadyExists:
                email_page.turn_on()
            else:
                email_page = EmailSender(self)
                email_page.turn_on()
                self.emailPageAlreadyExists = True

        email_label = customtkinter.CTkLabel(
            email_container, text="Email Sender", font=("Nunito", 18, "bold")
        )
        email_label.grid(row=0, column=0, pady=10, padx=20)

        send_button = customtkinter.CTkButton(
            email_container, text="Send Email", command=setup_email_page
        )
        send_button.grid(row=1, column=0, pady=10, padx=20)

        email__info_label = customtkinter.CTkLabel(
            email_container, text="In order to send emails, \n an app password is required \n which can be found in settings, \n you must have 2-factor \n authentication enabled to use it", font=("Nunito", 14, "bold")
        )
        email__info_label.grid(row=2,column=0,padx=10,pady=10)

        rail_info = RailInfoScraperApp().retrieve_rail_info()

        rail_info_frame = customtkinter.CTkScrollableFrame(self, width=300, height=200)
        rail_info_frame.grid(row=0, column=2,sticky="nsew", pady=10, padx=10)
        title_label = customtkinter.CTkLabel(
            rail_info_frame, text="National Rail Delays UK", font=("Nunito", 20, "bold")
        )
        title_label.pack(pady=5)
        self.rail_info_label = customtkinter.CTkLabel(
            rail_info_frame, text=rail_info, font=("Nunito", 14, "normal")
        )
        self.rail_info_label.pack()

        # Deadline Notifier
        values = ["Walk the dog", "Accept my application","Submit assignment"]
        self.scrollable_checkbox_frame = customtkinter.CTkScrollableFrame(self, label_text="To-do-list",width=100,height=100)
        self.scrollable_checkbox_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 20), sticky="nsew")

        self.checkbox_frame = ToDoList(self.scrollable_checkbox_frame, values=values, app=self,width=100,height=100)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

        self.button = customtkinter.CTkButton(self.scrollable_checkbox_frame, text="Add New Task", command=self.add_value_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def add_value_callback(self):
        dialog = customtkinter.CTkInputDialog(text="Enter a new task:", title="Add Task")
        new_value = dialog.get_input()
        if new_value:
            self.checkbox_frame.add_value(new_value)

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
                self.start_stop_button.configure(text="Stop", fg_color="#FF0000")
                self.reset_button.configure(state="disabled")
                self.update_timer()
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
                self.start_stop_button.configure(text="Start", fg_color="#008000")
                self.reset_button.configure(state="normal")
                self.total_seconds_worked += time.time() - self.start_time
                self.update_total_hours()
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
        self.seconds_left = self.work_duration
        self.is_break = False
        self.is_running = False
        self.mode_label.configure(text="Work Mode")

    def update_timer(self):
        if self.is_running:
            minutes, seconds = divmod(self.seconds_left, 60)
            time_format = "{:02d}:{:02d}".format(minutes, seconds)
            self.timer_label.configure(text=time_format)

            if self.seconds_left == 0:
                self.is_break = not self.is_break
                if self.is_break:
                    self.seconds_left = int(self.break_entry.get()) * 60
                    self.mode_label.configure(text="Break Mode")
                else:
                    self.seconds_left = int(self.work_entry.get()) * 60
                    self.mode_label.configure(text="Work Mode")

            if self.current_time is not None and self.current_time - self.last_button_press_time < 1:
                pass
            else:
                self.seconds_left -= 1

            self.after(1000, self.update_timer)

    def assign_login_page(self, page):
        self.login_page = page

    def turn_off(self):
        self.withdraw()

    def turn_on(self):
        self.deiconify()
        self.mainloop()

    def back_to_login(self):
        db_instance.delete_saved_login()
        self.withdraw()
        self.login_page.deiconify()
        self.login_page.mainloop()