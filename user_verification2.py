import streamlit as st
import sqlite3

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new user
def create_user(conn, name, email, password):
    sql = ''' INSERT INTO users(name,email,password)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, email, password))
    conn.commit()
    return cur.lastrowid

# Function to verify user credentials
def verify_user(conn, email, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    return user

import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def signup(conn):
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if not validate_email(email):
            st.error("Invalid email format. Please enter a valid email.")
        elif password == confirm_password:
            create_user(conn, name, email, password)
            st.success("You have successfully signed up!")
            st.info("Please proceed to sign in.")
        else:
            st.error("Passwords do not match.")

def signin(conn):
    st.subheader("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if not validate_email(email):
            st.error("Invalid email format. Please enter a valid email.")
        user = verify_user(conn, email, password)
        if user:
            st.success("You have successfully signed in!")
            st.write(f"Welcome back, {email}!")
        else:
            st.error("Invalid credentials. Please try again.")

def main():
    st.title("User Verification System")

    # Create a database connection
    conn = create_connection("user_verification.db")
    if conn is not None:
        # Create users table if it doesn't exist
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """
        with conn:
            conn.execute(create_table_sql)

        menu = ["Sign Up", "Sign In"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Sign Up":
            signup(conn)
        elif choice == "Sign In":
            signin(conn)
    else:
        st.error("Error: Unable to establish database connection.")

if __name__ == "__main__":
    main()
