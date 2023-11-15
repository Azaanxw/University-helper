import tkinter as tk

root = tk.Tk()
root.title("Label and Input on the Same Line")

# Create a label widget
label = tk.Label(root, text="Label:")
label.grid(row=0, column=0, padx=10, pady=10, sticky='e')  # 'e' means right-aligned

# Create an Entry widget for user input
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
