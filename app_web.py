import streamlit as st
import snowflake.connector
import random

# Snowflake connection configuration
SNOWFLAKE_CONFIG = {
    'user': 'peju_tf',
    'password': 'Terr@formBy4ce',
    'account': 'ADNWXHP-PEJU',
    'warehouse': 'PJ_WH',
    'database': 'MICRO',
    'schema': 'PUBLIC'
}

# Function to generate a unique 10-digit account number
def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

# Function to check if account number exists
def account_number_exists(account_number):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "SELECT COUNT(*) FROM users WHERE ACCOUNT_NUMBER = %s",
            (account_number,)
        )
        
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return count > 0
    except Exception as e:
        st.error(f"Error checking account number: {e}")
        return False

# Function to get unique account number
def get_unique_account_number():
    max_attempts = 100
    for _ in range(max_attempts):
        account_number = generate_account_number()
        if not account_number_exists(account_number):
            return account_number
    return None

# Function to insert data into Snowflake
def insert_to_snowflake(fname, lname, phone_no, email, gender, loan_balance, account_number):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO users (fname, lname, phone_no, email, gender, loan_balance, account_number) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (fname, lname, phone_no, email, gender, loan_balance, account_number)
        )
        
        cur.close()
        conn.close()
        
        return True
    except Exception as e:
        st.error(f"Error inserting to Snowflake: {e}")
        return False

# Function to retrieve data from Snowflake by account number
def retrieve_from_snowflake(account_number):
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        cur.execute(
            "SELECT FNAME, LNAME, PHONE_NO, EMAIL, GENDER, LOAN_BALANCE, ACCOUNT_NUMBER FROM users WHERE ACCOUNT_NUMBER = %s",
            (account_number,)
        )
        
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return result
    except Exception as e:
        st.error(f"Error retrieving from Snowflake: {e}")
        return None

# Page configuration
st.set_page_config(
    page_title="User Management System",
    page_icon="👥",
    layout="centered"
)

# Main title
st.title("👥 User Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select an option:", ["Home", "Register New User", "Retrieve User Info"])

# Home Page
if page == "Home":
    st.markdown("---")
    st.header("Welcome to the User Management System")
    st.write("")
    st.write("Use the sidebar to navigate between different functions:")
    st.write("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**📝 Register New User**\n\nAdd new users to the system by providing their information.")
    
    with col2:
        st.info("**🔍 Retrieve User Info**\n\nSearch for existing users by their ID and view their details.")
    
    st.write("")
    st.success("Select an option from the sidebar to get started!")

# Register New User Page
elif page == "Register New User":
    st.markdown("---")
    st.header("📝 Register New User")
    st.write("Please fill in all the fields below:")
    
    # Initialize session state for form reset
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    # Reset form if needed
    if st.session_state.form_submitted:
        st.session_state.form_submitted = False
        st.rerun()
    
    with st.form("registration_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            fname = st.text_input("First Name*", placeholder="Enter first name")
            phone_no = st.text_input("Phone Number*", placeholder="Enter phone number")
            gender = st.selectbox("Gender*", ["Select", "Male", "Female"])
        
        with col2:
            lname = st.text_input("Last Name*", placeholder="Enter last name")
            email = st.text_input("Email*", placeholder="Enter email address")
            loan_balance = st.number_input("Loan Balance*", min_value=0.0, step=0.01, format="%.2f")
        
        st.info("💡 Account number will be automatically generated upon registration")
        
        submitted = st.form_submit_button("Register User", type="primary")
    
    # Process form submission outside the form
    if submitted:
        # Validate all fields are filled
        if not fname or not lname or not phone_no or not email or gender == "Select":
            st.error("❌ Please fill in all required fields.")
        else:
            # Generate unique account number
            with st.spinner("Generating account number..."):
                account_number = get_unique_account_number()
            
            if not account_number:
                st.error("❌ Unable to generate unique account number. Please try again.")
            else:
                # Insert data into Snowflake
                with st.spinner("Registering user..."):
                    success = insert_to_snowflake(fname, lname, phone_no, email, gender, loan_balance, account_number)
                
                if success:
                    st.success("✅ User registered successfully!")
                    st.balloons()
                    
                    # Display registered info
                    st.markdown("---")
                    st.write("**Registered Information:**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**First Name:** {fname}")
                        st.write(f"**Last Name:** {lname}")
                        st.write(f"**Phone Number:** {phone_no}")
                        st.write(f"**Email:** {email}")
                    
                    with col2:
                        st.write(f"**Gender:** {gender}")
                        st.write(f"**Loan Balance:** ${loan_balance:,.2f}")
                        st.write(f"**Account Number:** {account_number}")
                    
                    # Highlight account number
                    st.success(f"🔢 Generated Account Number: **{account_number}**")
                    
                    # Add a button to register another user (clears form)
                    if st.button("Register Another User"):
                        st.session_state.form_submitted = True
                        st.rerun()
                else:
                    st.error("❌ Failed to register user. Please check the error message above.")

# Retrieve User Info Page
elif page == "Retrieve User Info":
    st.markdown("---")
    st.header("🔍 Retrieve User Information")
    st.write("Enter the Account Number to search:")
    
    # Account Number input
    account_number = st.text_input("Account Number", placeholder="Enter 10-digit account number", key="account_number_search")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        search_button = st.button("Search", type="primary")
    
    with col2:
        clear_button = st.button("Clear")
    
    # Handle clear button
    if clear_button:
        st.rerun()
    
    # Handle search button
    if search_button:
        if not account_number:
            st.error("❌ Please enter an Account Number.")
        else:
            with st.spinner("Searching for user..."):
                user_data = retrieve_from_snowflake(account_number)
            
            if user_data:
                st.success("✅ User found!")
                st.markdown("---")
                st.subheader("User Information:")
                
                # Display user information in a nice format
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("First Name", user_data[0])
                    st.metric("Phone Number", user_data[2])
                    st.metric("Gender", user_data[4])
                
                with col2:
                    st.metric("Last Name", user_data[1])
                    st.metric("Email", user_data[3])
                    st.metric("Loan Balance", f"${user_data[5]:,.2f}")
                
                # Highlight account number
                st.markdown("---")
                st.success(f"🔢 Account Number: **{user_data[6]}**")
                
                # Also show as a table
                st.markdown("---")
                st.write("**Complete Details:**")
                st.table({
                    "Field": ["First Name", "Last Name", "Phone Number", "Email", "Gender", "Loan Balance", "Account Number"],
                    "Value": [user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], f"${user_data[5]:,.2f}", user_data[6]]
                })
            else:
                st.error("❌ User not found or error retrieving data.")

# Footer
st.markdown("---")
st.caption("User Management System v2.0 | Powered by Streamlit & Snowflake")