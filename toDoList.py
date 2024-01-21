# Imports
import customtkinter

class ToDoList(customtkinter.CTkFrame):
    def __init__(self, master, values, app,width,height):
        super().__init__(master)
        self.width = width
        self.height = height
        self.values = values
        self.app = app
        self.checkboxes = {}

        # Creates checkboxes for each task
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, command=lambda v=value: self.checkbox_callback(v))
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes[value] = checkbox

    # Callback for when a checkbox is clicked
    def checkbox_callback(self, value):
        checkbox = self.checkboxes.get(value)
        if checkbox:
            if checkbox.get() == 1:
                # Disable the checkbox once checked
                checkbox.configure(state="disabled")
                # Schedule deletion after 1 second
                self.after(1000, lambda v=value: self.delete_checkbox(v))
    
    # Deletes the given checkbox after it gets clicked
    def delete_checkbox(self, value):
        checkbox = self.checkboxes.get(value)
        if checkbox:
            # Remove the value from the original array
            self.values.remove(value)
            # Clear the checkbox state
            checkbox.deselect()
            self.after(10, lambda v=value: checkbox.destroy())
    
    # Adds a new task to the list
    def add_value(self, new_value):
        # Check if the value is not already in the array
        if new_value.strip() == "":
            return 
        if new_value not in self.values:
            # Insert the new value at the beginning of the array
            self.values.insert(0, new_value)

            # Clear existing checkboxes
            for checkbox in self.checkboxes.values():
                checkbox.destroy()
            self.checkboxes.clear()

            # Recreate checkboxes for all values
            for i, value in enumerate(self.values):
                checkbox = customtkinter.CTkCheckBox(self, text=value, command=lambda v=value: self.checkbox_callback(v))
                checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
                self.checkboxes[value] = checkbox
