import tkinter as tk
from tkinter import messagebox
import snowflake.connector

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    'user': 'peju_tf',
    'password': 'Terr@formBy4ce',
    'account': 'ADNWXHP-PEJU',
    'warehouse': 'pj_wh',
    'database': 'MICRO',
    'schema': 'PUBLIC'
}

# Function to insert data into Snowflake
def insert_to_snowflake(fname, lname, phone_no, email, account_no):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (fname, lname, phone_no, email, account_no) VALUES (%s, %s, %s, %s, %s)",
            (fname, lname, phone_no, email, account_no)
        )

        cur.close()
        conn.close()

        return True
    except Exception as e:
        print(f"Error inserting to Snowflake: {e}")
        return False

# Function to retrieve data from Snowflake
def retrieve_from_snowflake(user_id):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()

        cur.execute(
            "SELECT FNAME, LNAME, PHONE_NO, EMAIL, ACCOUNT_NO FROM users WHERE ID = %s",
            (user_id,)
        )

        result = cur.fetchone()

        cur.close()
        conn.close()

        return result
    except Exception as e:
        print(f"Error retrieving from Snowflake: {e}")
        return None

# Function to show registration form
def show_registration():
    clear_window()

    tk.Label(root, text="User Registration", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(root, text="First Name:").pack(pady=(10, 0))
    global fname_entry
    fname_entry = tk.Entry(root, width=30)
    fname_entry.pack()

    tk.Label(root, text="Last Name:").pack(pady=(10, 0))
    global lname_entry
    lname_entry = tk.Entry(root, width=30)
    lname_entry.pack()

    tk.Label(root, text="Phone Number:").pack(pady=(10, 0))
    global phone_no_entry
    phone_no_entry = tk.Entry(root, width=30)
    phone_no_entry.pack()

    tk.Label(root, text="Email:").pack(pady=(10, 0))
    global email_entry
    email_entry = tk.Entry(root, width=30)
    email_entry.pack()

    tk.Label(root, text="Account_no:").pack(pady=(10, 0))
    global account_no_entry
    account_no_entry = tk.Entry(root, show="*", width=30)
    account_no_entry.pack()

    submit_button = tk.Button(root, text="Register", command=submit_form, bg="#4CAF50", fg="white", width=15)
    submit_button.pack(pady=20)

    back_button = tk.Button(root, text="Back to Menu", command=show_main_menu, bg="#808080", fg="white", width=15)
    back_button.pack()

# Function to show retrieval form
def show_retrieval():
    clear_window()

    tk.Label(root, text="User Information Retrieval", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(root, text="Enter User ID:", font=("Arial", 12)).pack(pady=(10, 5))
    global id_entry
    id_entry = tk.Entry(root, width=30)
    id_entry.pack(pady=5)

    search_button = tk.Button(root, text="Search", command=search_user, bg="#4CAF50", fg="white", width=15)
    search_button.pack(pady=10)

    tk.Label(root, text="─" * 50).pack(pady=10)

    tk.Label(root, text="User Information:", font=("Arial", 12, "bold")).pack(pady=(10, 10))

    global info_frame
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)

    tk.Label(info_frame, text="First Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    global fname_value
    fname_value = tk.Label(info_frame, text="", font=("Arial", 10))
    fname_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    tk.Label(info_frame, text="Last Name:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    global lname_value
    lname_value = tk.Label(info_frame, text="", font=("Arial", 10))
    lname_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    tk.Label(info_frame, text="Phone No:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    global phone_no_value
    phone_no_value = tk.Label(info_frame, text="", font=("Arial", 10))
    phone_no_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    tk.Label(info_frame, text="Email:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    global email_value
    email_value = tk.Label(info_frame, text="", font=("Arial", 10))
    email_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    tk.Label(info_frame, text="Account_no:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    global account_no_value
    account_no_value = tk.Label(info_frame, text="", font=("Arial", 10))
    account_no_value.grid(row=4, column=1, sticky="w", padx=10, pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    clear_button = tk.Button(button_frame, text="Clear", command=clear_retrieval_form, bg="#f44336", fg="white", width=15)
    clear_button.pack(side=tk.LEFT, padx=5)

    back_button = tk.Button(button_frame, text="Back to Menu", command=show_main_menu, bg="#808080", fg="white", width=15)
    back_button.pack(side=tk.LEFT, padx=5)

# Function to submit registration form
def submit_form():
    fname = fname_entry.get()
    lname = lname_entry.get()
    phone_no = phone_no_entry.get()
    email = email_entry.get()
    account_no = account_no_entry.get()

    if not fname or not lname or not phone_no or not email or not account_no:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    success = insert_to_snowflake(fname, lname, phone_no, email, account_no)

    if success:
        print("Fname:", fname)
        print("Lname:", lname)
        print("Phone_no:", phone_no)
        print("Email:", email)
        print("account_no:", account_no)
        messagebox.showinfo("Success", "User registered successfully!")

        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        phone_no_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        account_no_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Failed to register user. Check console for details.")

# Function to search for user
def search_user():
    user_id = id_entry.get()

    if not user_id:
        messagebox.showerror("Error", "Please enter a User ID.")
        return

    user_data = retrieve_from_snowflake(user_id)

    if user_data:
        fname_value.config(text=user_data[0])
        lname_value.config(text=user_data[1])
        phone_no_value.config(text=user_data[2])
        email_value.config(text=user_data[3])
        account_no_value.config(text=user_data[4])

        messagebox.showinfo("Success", "User data retrieved successfully!")
    else:
        fname_value.config(text="")
        lname_value.config(text="")
        phone_no_value.config(text="")
        email_value.config(text="")
        account_no_value.config(text="")

        messagebox.showerror("Error", "User not found or error retrieving data.")

# Function to clear retrieval form
def clear_retrieval_form():
    id_entry.delete(0, tk.END)
    fname_value.config(text="")
    lname_value.config(text="")
    phone_no_value.config(text="")
    email_value.config(text="")
    account_no_value.config(text="")

# Function to clear window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Function to show main menu
def show_main_menu():
    clear_window()

    tk.Label(root, text="User Management System", font=("Arial", 18, "bold")).pack(pady=40)

    tk.Label(root, text="Please select an option:", font=("Arial", 12)).pack(pady=10)

    register_button = tk.Button(root, text="Register New User", command=show_registration, 
                                bg="#4CAF50", fg="white", width=20, height=2, font=("Arial", 11))
    register_button.pack(pady=10)

    retrieve_button = tk.Button(root, text="Retrieve User Info", command=show_retrieval, 
                                bg="#2196F3", fg="white", width=20, height=2, font=("Arial", 11))
    retrieve_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, 
                           bg="#f44336", fg="white", width=20, height=2, font=("Arial", 11))
    exit_button.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("User Management System")
root.geometry("450x500")

# Show main menu on startup
show_main_menu()

# Run the UI loop
root.mainloop()