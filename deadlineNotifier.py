# Imports
import customtkinter
from datetime import datetime

class DeadlineNotifier(customtkinter.CTkFrame):
    def __init__(self, master, values, app):
        super().__init__(master)
        self.values = values
        self.app = app
        self.checkboxes = {}

        self.update_dates()  # Update dates and sort tasks initially

        # Creates checkboxes for each task
        for i, (value, data) in enumerate(self.values.items()):
            checkbox_text = f"{value} - {data['date']} (Days remaining: {data['days_remaining']})"
            checkbox = customtkinter.CTkCheckBox(self, text=checkbox_text, command=lambda v=value: self.checkbox_callback(v))
            checkbox.grid(row=i, column=0, padx=80, pady=(20, 0), sticky="nsew") 
            self.checkboxes[value] = checkbox

    def update_dates(self): # Updates the remaining days for each task based on the current date

        today = datetime.now().date()

        for value, data in self.values.items():
            task_date = datetime.strptime(data['date'], "%d/%m/%Y").date()
            days_remaining = (task_date - today).days
            data['days_remaining'] = days_remaining

        # Sort tasks based on the remaining days
        self.values = dict(sorted(self.values.items(), key=lambda item: item[1]['days_remaining']))

    def checkbox_callback(self, value): # Callback for when a checkbox is clicked - makes it disappear after 1 second
        checkbox = self.checkboxes.get(value)
        if checkbox:
            if checkbox.get() == 1:
                # Disable the checkbox once checked
                checkbox.configure(state="disabled")
                # Schedule deletion after 1 second
                self.after(1000, lambda v=value: self.delete_checkbox(v))

    def delete_checkbox(self, value): # Deletes the checkbox 
        checkbox = self.checkboxes.get(value)
        if checkbox:
            # Remove the value from the original dictionary
            del self.values[value]
            # Clear the checkbox state
            checkbox.deselect()
            self.after(10, lambda v=value: checkbox.destroy())

    def add_value(self, new_value, new_date): # Adds a new value to the deadline list
        # Check if the value is not already in the dictionary
        if new_value.strip() == "":
            return
        if new_value not in self.values:
            # Insert the new value with the provided date into the dictionary
            self.values[new_value] = {'date': new_date, 'days_remaining': 0}

            # Update dates and sort tasks
            self.update_dates()

            # Clear existing checkboxes
            for checkbox in self.checkboxes.values():
                checkbox.destroy()
            self.checkboxes.clear()

            # Recreate checkboxes for all values
            for i, (value, data) in enumerate(self.values.items()):
                checkbox_text = f"{value} - {data['date']} (Days remaining: {data['days_remaining']})"
                checkbox = customtkinter.CTkCheckBox(self, text=checkbox_text, command=lambda v=value: self.checkbox_callback(v))
                checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="nsew")  # Center content
                self.checkboxes[value] = checkbox
