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

# Function to retrieve data from Snowflake
def retrieve_from_snowflake(user_id):
    try:
        # Establish connection
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        # Retrieve data - using exact column names from your table
        cur.execute(
            "SELECT FNAME, LNAME, PHONE_NO, EMAIL, PASSWORD FROM users WHERE ID = %s",
            (user_id,)
        )
        
        result = cur.fetchone()
        
        # Close connections
        cur.close()
        conn.close()
        
        return result
    except Exception as e:
        print(f"Error retrieving from Snowflake: {e}")
        return None

# Function called when the search button is clicked
def search_user():
    user_id = id_entry.get()
    
    if not user_id:
        messagebox.showerror("Error", "Please enter a User ID.")
        return
    
    # Retrieve data from Snowflake
    user_data = retrieve_from_snowflake(user_id)
    
    if user_data:
        # Display the retrieved data
        fname_value.config(text=user_data[0])
        lname_value.config(text=user_data[1])
        phone_no_value.config(text=user_data[2])
        email_value.config(text=user_data[3])
        password_value.config(text=user_data[4])
        
        messagebox.showinfo("Success", "User data retrieved successfully!")
    else:
        # Clear previous data
        fname_value.config(text="")
        lname_value.config(text="")
        phone_no_value.config(text="")
        email_value.config(text="")
        password_value.config(text="")
        
        messagebox.showerror("Error", "User not found or error retrieving data.")

# Function to clear the form
def clear_form():
    id_entry.delete(0, tk.END)
    fname_value.config(text="")
    lname_value.config(text="")
    phone_no_value.config(text="")
    email_value.config(text="")
    password_value.config(text="")

# Create the main window
root = tk.Tk()
root.title("Customer Information Retrieval")
root.geometry("400x350")

# User ID input section
tk.Label(root, text="Enter User ID:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
id_entry = tk.Entry(root, width=30)
id_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=search_user, bg="#4CAF50", fg="white", width=15)
search_button.pack(pady=10)

# Separator
tk.Label(root, text="─" * 50).pack(pady=10)

# Display section with labels
tk.Label(root, text="User Information:", font=("Arial", 12, "bold")).pack(pady=(10, 10))

# Frame for displaying user info
info_frame = tk.Frame(root)
info_frame.pack(pady=10)

# First Name
tk.Label(info_frame, text="First Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
fname_value = tk.Label(info_frame, text="", font=("Arial", 10))
fname_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Last Name
tk.Label(info_frame, text="Last Name:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
lname_value = tk.Label(info_frame, text="", font=("Arial", 10))
lname_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Phone Number
tk.Label(info_frame, text="Phone No:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
phone_no_value = tk.Label(info_frame, text="", font=("Arial", 10))
phone_no_value.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Email
tk.Label(info_frame, text="Email:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
email_value = tk.Label(info_frame, text="", font=("Arial", 10))
email_value.grid(row=3, column=1, sticky="w", padx=10, pady=5)

# Password
tk.Label(info_frame, text="Password:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=5)
password_value = tk.Label(info_frame, text="", font=("Arial", 10))
password_value.grid(row=4, column=1, sticky="w", padx=10, pady=5)

# Clear button
clear_button = tk.Button(root, text="Clear", command=clear_form, bg="#f44336", fg="white", width=15)
clear_button.pack(pady=10)
``
# Run the UI loop
root.mainloop()


