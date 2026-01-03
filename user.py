import tkinter as tk
from tkinter import messagebox
import snowflake.connector

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    'user': '',
    'password': '',
    'account': '',
    'warehouse': '',
    'database': 'MICRO',
    'schema': 'PUBLIC'
}

# Function to insert data into Snowflake
def insert_to_snowflake(fname, lname, phone_no, email, password):
    try:
        # Establish connection
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        # Insert data
        cur.execute(
            "INSERT INTO users (fname, lname, phone_no, email, password) VALUES (%s, %s, %s, %s, %s)",
            (fname, lname, phone_no, email, password)
        )
        
        # Close connections
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error inserting to Snowflake: {e}")
        return False

# Function called when the button is clicked
def submit_form():
    fname = fname_entry.get()
    lname = lname_entry.get()
    phone_no = phone_no_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not fname or not lname or not phone_no or not email or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Insert data into Snowflake
    success = insert_to_snowflake(fname, lname, phone_no, email, password)
    
    if success:
        print("Fname:", fname)
        print("Lname:", lname)
        print("Phone_no:", phone_no)
        print("Email:", email)
        print("Password:", password)
        messagebox.showinfo("Success", "Data saved to Snowflake successfully!")
        
        # Clear the form
        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        phone_no_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Failed to save data to Snowflake. Check console for details.")

# Create the main window
root = tk.Tk()
root.title("User Registration")
root.geometry("300x250")

# Labels & entry widgets
tk.Label(root, text="Fname:").pack(pady=(10, 0))
fname_entry = tk.Entry(root)
fname_entry.pack()

tk.Label(root, text="Lname:").pack(pady=(10, 0))
lname_entry = tk.Entry(root)
lname_entry.pack()

tk.Label(root, text="Phone_no:").pack(pady=(10, 0))
phone_no_entry = tk.Entry(root)
phone_no_entry.pack()

tk.Label(root, text="Email:").pack(pady=(10, 0))
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password:").pack(pady=(10, 0))
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack(pady=20)

# Run the UI loop
root.mainloop()