import tkinter as tk
from tkinter import messagebox

def show_about():
    """Display information about the application."""
    messagebox.showinfo("About", "This is a simple questionnaire application built with Tkinter.")

def exit_app():
    """Exit the application."""
    root.quit()

# Main window
root = tk.Tk()
root.title("Questionnaire with Menu")

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=lambda: messagebox.showinfo("New", "New Questionnaire started!"))
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the root window
root.config(menu=menu_bar)

# Example content
label = tk.Label(root, text="Welcome to the Questionnaire App!")
label.pack(pady=20)

button = tk.Button(root, text="Start", command=lambda: messagebox.showinfo("Start", "Questionnaire started!"))
button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
