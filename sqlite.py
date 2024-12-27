# File: sqlite_crud_gui_update.py

import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox, Frame, Text, Toplevel

import logging

# Configure the logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_operation(operation, details):
    """
    Logs an operation with details to the log file.
    """
    logging.info(f"{operation}: {details}")
# Database Functions
def connect_to_db(db_name="app_database.db"):
    return sqlite3.connect(db_name)


def create_table():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)
    connection.commit()
    connection.close()


def insert_user(name, age, email):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))
        connection.commit()
        log_operation("Insert", f"User added: {name}, Age: {age}, Email: {email}")
        messagebox.showinfo("Success", "User added successfully!")
    except sqlite3.IntegrityError as e:
        logging.error(f"Insert Error: {e}")
        messagebox.showerror("Error", f"Error adding user: {e}")
    finally:
        connection.close()


def update_user(user_id, name, age, email):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET name = ?, age = ?, email = ? WHERE id = ?", (name, age, email, user_id))
        connection.commit()
        log_operation("Update", f"User updated: ID {user_id}, Name: {name}, Age: {age}, Email: {email}")
    except sqlite3.Error as e:
        logging.error(f"Update Error: {e}")
    finally:
        connection.close()


def list_users(limit=5, offset=0, filter_by=None):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM users"
    params = []
    if filter_by:
        query += " WHERE name LIKE ? OR email LIKE ?"
        params.extend([f"%{filter_by}%", f"%{filter_by}%"])
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    users = cursor.fetchall()
    connection.close()
    return users


def get_total_user_count(filter_by=None):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM users"
    params = []
    if filter_by:
        query += " WHERE name LIKE ? OR email LIKE ?"
        params.extend([f"%{filter_by}%", f"%{filter_by}%"])

    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    connection.close()
    return count

def clear_fields():
    """
     Clears all input fields (Name, Age, Email) in the form.
    """
    name_entry.delete(0, END)  # Clear the name field
    age_entry.delete(0, END)  # Clear the age field
    email_entry.delete(0, END)  # Clear the email field


def refresh_logs():
    """
    Reads the log file and displays its content in the log viewer.
    """
    with open("app.log", "r") as log_file:
        log_content = log_file.read()
    log_text.delete("1.0", END)  # Clear existing content
    log_text.insert(END, log_content)  # Add new content

def delete_user(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        connection.commit()
        log_operation("Delete", f"User ID deleted: {user_id}")
    except sqlite3.Error as e:
        logging.error(f"Delete Error: {e}")
    finally:
        connection.close()


# GUI Functions
def list_all_users():
    global current_page, total_pages, filter_text

    user_listbox.delete(0, END)
    users = list_users(limit=ITEMS_PER_PAGE, offset=(current_page - 1) * ITEMS_PER_PAGE, filter_by=filter_text.get())
    for user in users:
        user_listbox.insert(END, f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}, Email: {user[3]}")

    # Update pagination info
    total_users = get_total_user_count(filter_by=filter_text.get())
    total_pages = (total_users + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page_label.config(text=f"Page {current_page} of {total_pages}")


def next_page():
    global current_page, total_pages
    if current_page < total_pages:
        current_page += 1
        list_all_users()


def previous_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        list_all_users()


def search_users():
    global current_page
    current_page = 1
    list_all_users()


def add_user():
    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    if name and age and email:
        try:
            insert_user(name, int(age), email)
            list_all_users()
            clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
    else:
        messagebox.showerror("Error", "All fields are required.")


def delete_selected_user():
    selected = user_listbox.curselection()
    if selected:
        user_data = user_listbox.get(selected[0])
        user_id = int(user_data.split(",")[0].split(":")[1].strip())
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user with ID {user_id}?")
        if confirm:
            delete_user(user_id)
            list_all_users()
    else:
        messagebox.showerror("Error", "No user selected. Please select a user to delete.")


def populate_fields():
    """
    Populates the input fields with the details of the selected user.
    """
    selected = user_listbox.curselection()  # Get the index of the selected item
    if selected:
        # Retrieve the selected item's data
        user_data = user_listbox.get(selected[0])
        # Example format: "ID: 1, Name: John Doe, Age: 25, Email: john.doe@example.com"

        # Parse the data
        user_id = int(user_data.split(",")[0].split(":")[1].strip())
        name = user_data.split(",")[1].split(":")[1].strip()
        age = user_data.split(",")[2].split(":")[1].strip()
        email = user_data.split(",")[3].split(":")[1].strip()

        # Populate input fields
        name_entry.delete(0, END)
        name_entry.insert(0, name)

        age_entry.delete(0, END)
        age_entry.insert(0, age)

        email_entry.delete(0, END)
        email_entry.insert(0, email)

        # Store the user ID for updating
        return user_id
    else:
        messagebox.showerror("Error", "No user selected. Please select a user to edit.")
        return None


def update_user_details():
    """
    Updates the user details based on the input fields.
    """
    selected = user_listbox.curselection()
    if selected:
        user_data = user_listbox.get(selected[0])
        user_id = int(user_data.split(",")[0].split(":")[1].strip())
        name = name_entry.get()
        age = age_entry.get()
        email = email_entry.get()
        if name and age and email:
            confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update user with ID {user_id}?")
            if confirm:
                try:
                    update_user(user_id, name, int(age), email)
                    list_all_users()
                    messagebox.showinfo("Success", "User details updated successfully!")
                except ValueError:
                    messagebox.showerror("Error", "Age must be a number.")
        else:
            messagebox.showerror("Error", "All fields are required for update.")
    else:
        messagebox.showerror("Error", "No user selected. Please select a user to update.")



# Main Application
def main():
    global user_listbox, page_label, current_page, total_pages, ITEMS_PER_PAGE
    global name_entry, age_entry, email_entry, filter_text, log_text

    # Initialize the database
    create_table()

    def refresh_logs_in_window(log_text_widget):
        """
        Refreshes the logs displayed in the Text widget of the log window.
        """
        with open("app.log", "r") as log_file:
            log_content = log_file.read()
            log_text_widget.delete("1.0", END)  # Clear existing content
            log_text_widget.insert(END, log_content)  # Add new content
    # Constants
    ITEMS_PER_PAGE = 5
    current_page = 1
    total_pages = 1

    # Create the main window
    app = Tk()
    app.title("SQLite CRUD Application with Logging")
    app.geometry("800x600")
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_rowconfigure(1, weight=1)

    # Search Filters
    Label(app, text="Search").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    filter_text = Entry(app)
    filter_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    Button(app, text="Search", command=search_users).grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # User Listbox with Scrollbar
    user_listbox_frame = Frame(app)
    user_listbox_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    user_listbox_frame.grid_rowconfigure(0, weight=1)
    user_listbox_frame.grid_columnconfigure(0, weight=1)

    user_listbox = Listbox(user_listbox_frame, width=70, height=15)
    user_listbox.grid(row=0, column=0, sticky="nsew")

    scrollbar = Scrollbar(user_listbox_frame, orient="vertical", command=user_listbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    user_listbox.config(yscrollcommand=scrollbar.set)

    # Pagination
    Button(app, text="Previous", command=previous_page).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    page_label = Label(app, text="Page 1 of 1")
    page_label.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    Button(app, text="Next", command=next_page).grid(row=2, column=2, padx=10, pady=10, sticky="e")

    # Add User Fields
    Label(app, text="Name").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    name_entry = Entry(app)
    name_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    Label(app, text="Age").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    age_entry = Entry(app)
    age_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    Label(app, text="Email").grid(row=5, column=0, padx=10, pady=10, sticky="w")
    email_entry = Entry(app)
    email_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

    def open_log_window():
        """
        Opens a new window to display the logs from the log file.
        """
        # Create a new top-level window
        log_window = Toplevel()
        log_window.title("Log Viewer")
        log_window.geometry("800x400")
        log_window.grid_columnconfigure(0, weight=1)
        log_window.grid_rowconfigure(0, weight=1)

        # Create a frame for the log viewer
        log_frame = Frame(log_window)
        log_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        # Add a Text widget to display the logs
        log_text = Text(log_frame, wrap="none", state="normal")
        log_text.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the Text widget
        log_scrollbar = Scrollbar(log_frame, orient="vertical", command=log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky="ns")
        log_text.config(yscrollcommand=log_scrollbar.set)

        # Load log content into the Text widget
        refresh_logs_in_window(log_text)

        # Add a button to refresh the logs
        Button(log_window, text="Refresh Logs", command=lambda: refresh_logs_in_window(log_text)).grid(row=1, column=0,
                                                                                                       padx=10, pady=10,
                                                                                                       sticky="ew")

    def refresh_logs_in_window(log_text_widget):
        """
        Refreshes the logs displayed in the Text widget of the log window.
        """
        with open("app.log", "r") as log_file:
            log_content = log_file.read()
        log_text_widget.delete("1.0", END)  # Clear existing content
        log_text_widget.insert(END, log_content)  # Add new content
    Button(app, text="Add User", command=add_user).grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    Button(app, text="Edit Selected User", command=populate_fields).grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    Button(app, text="Update User", command=update_user_details).grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    Button(app, text="Delete Selected User", command=delete_selected_user).grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    Button(app, text="Clear Fields", command=clear_fields).grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    Button(app, text="View Logs", command=open_log_window).grid(row=13, column=0, columnspan=3, padx=10, pady=10,
                                                                sticky="ew")

    # Log Viewer Section




#    Load users initially
    list_all_users()

    # Run the application
    app.mainloop()


def insert_dummy_data():
        """
        Inserts a predefined set of dummy data into the users table.
        """
        dummy_users = [
            ("John Doe", 25, "john.doe@example.com"),
            ("Jane Smith", 30, "jane.smith@example.com"),
            ("Alice Johnson", 35, "alice.johnson@example.com"),
            ("Bob Brown", 40, "bob.brown@example.com"),
            ("Charlie Davis", 28, "charlie.davis@example.com"),
            ("Diana Prince", 33, "diana.prince@example.com"),
            ("Eve Adams", 22, "eve.adams@example.com"),
            ("Frank Miller", 50, "frank.miller@example.com"),
            ("Grace Hopper", 45, "grace.hopper@example.com"),
            ("Hank Green", 38, "hank.green@example.com")
        ]

        connection = connect_to_db()
        cursor = connection.cursor()
        try:
            cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", dummy_users)
            connection.commit()
            print("Dummy data inserted successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting dummy data: {e}")
        finally:
            connection.close()


if __name__ == "__main__":

    # Call the function to insert the dummy data
    #insert_dummy_data()

    main()
