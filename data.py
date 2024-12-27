import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox


# Database Functions
def connect_to_db(db_name="app_database.db"):
    return sqlite3.connect(db_name)
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

def create_table():
    """
    Creates the users table in the database if it doesn't already exist.
    """
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

# Main GUI Application
def list_all_users():
    """
    Lists all users in the Listbox with pagination and filtering.
    """
    global current_page, total_pages, filter_text

    user_listbox.delete(0, END)
    users = list_users(limit=ITEMS_PER_PAGE, offset=(current_page - 1) * ITEMS_PER_PAGE, filter_by=filter_text.get())
    for user in users:
        user_listbox.insert(END, f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}, Email: {user[3]}")

    total_users = get_total_user_count(filter_by=filter_text.get())
    total_pages = (total_users + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page_label.config(text=f"Page {current_page} of {total_pages}")


def main():
    global user_listbox, page_label, current_page, total_pages, ITEMS_PER_PAGE
    global name_entry, age_entry, email_entry, filter_text

    # Initialize the database and insert dummy data
    create_table()
    #insert_dummy_data()

def search_users():
    global current_page
    current_page = 1
    list_all_users()

    # Constants
    ITEMS_PER_PAGE = 5
    current_page = 1
    total_pages = 1

    # Create the main window
    app = Tk()
    app.title("SQLite CRUD Application")
    app.geometry("600x550")

    # Search Filters
    Label(app, text="Search").grid(row=0, column=0, padx=10, pady=10)
    filter_text = Entry(app)
    filter_text.grid(row=0, column=1, padx=10, pady=10)
    Button(app, text="Search", command=search_users).grid(row=0, column=2, padx=10, pady=10)

    # User Listbox with Scrollbar
    user_listbox = Listbox(app, width=70, height=15)
    user_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    scrollbar = Scrollbar(app)
    scrollbar.grid(row=1, column=3, sticky='ns')
    user_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=user_listbox.yview)

def previous_page():
        global current_page
        if current_page > 1:
            current_page -= 1
            list_all_users()

def next_page():
    global current_page, total_pages
    if current_page < total_pages:
        current_page += 1
        list_all_users()

    app = Tk()
    app.title("SQLite CRUD Application with Update Functionality")
    app.geometry("600x550")
    # Pagination
    Button(app, text="Previous", command=previous_page).grid(row=2, column=0, padx=10, pady=10)
    page_label = Label(app, text="Page 1 of 1")
    page_label.grid(row=2, column=1, padx=10, pady=10)
    Button(app, text="Next", command=next_page).grid(row=2, column=2, padx=10, pady=10)

    # Add User Fields
    Label(app, text="Name").grid(row=3, column=0, padx=10, pady=10)
    name_entry = Entry(app)
    name_entry.grid(row=3, column=1, padx=10, pady=10)

    Label(app, text="Age").grid(row=4, column=0, padx=10, pady=10)
    age_entry = Entry(app)
    age_entry.grid(row=4, column=1, padx=10, pady=10)

    Label(app, text="Email").grid(row=5, column=0, padx=10, pady=10)
    email_entry = Entry(app)
    email_entry.grid(row=5, column=1, padx=10, pady=10)

    Button(app, text="Add User", command=add_user).grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    Button(app, text="Edit Selected User", command=populate_fields).grid(row=7, column=0, columnspan=3, padx=10,
                                                                         pady=10)
    Button(app, text="Update User", command=update_user_details).grid(row=8, column=0, columnspan=3, padx=10, pady=10)
    Button(app, text="Delete Selected User", command=delete_selected_user).grid(row=9, column=0, columnspan=3, padx=10,
                                                                                pady=10)

    # Load users initially
    list_all_users()

    # Run the application
    app.mainloop()


if __name__ == "__main__":
    main()
