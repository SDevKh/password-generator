import random
import string
import json
import streamlit as st

# CSS styling (keep as is)
st.markdown("""
<style>
.stApp {
    background-image: linear-gradient( 156.2deg,  rgba(0,0,0,1) 14.8%, rgba(32,104,177,1) 68.1%, rgba(222,229,237,1) 129% );
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-image: radial-gradient( circle farthest-corner at 50.3% 47.3%,  rgba(113,42,92,1) 0.1%, rgba(40,25,46,1) 90% );
}

/* Title styling */
h1 {
    color: white !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

/* Input boxes */
.stTextInput > div > div > input {
    background-color: white;
    color: black;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Buttons */
.stButton > button {
    background-image: radial-gradient( circle 710px at 5.2% 7.2%,  rgba(37,89,222,1) 0%, rgba(37,89,222,1) 7.5%, rgba(4,4,29,1) 44.7% );;
    color: white;
    border: none;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

def login_page():
    st.title("🔐 Login Page")
    
    # Create input fields
    username = st.text_input("Username")  # Fixed: was st.input_text
    password_login = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        # Simple authentication
        if username == "admin" and password_login == "password123":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password!")

def password_checker(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!@#$%^&*" for char in password):
        return False
    return True

def save_password(name, password):
    try:
        with open("passwords.json", "r") as f:
            content = f.read().strip()
            if content:
                passwords = json.loads(content)
            else:
                passwords = []
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = []

    passwords.append({"name": name, "password": password})
    
    with open("passwords.json", "w") as f:
        json.dump(passwords, f, indent=2)

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def delete_password(index):
    passwords = load_passwords()
    if 0 <= index < len(passwords):
        deleted = passwords.pop(index)
        with open("passwords.json", "w") as f:
            json.dump(passwords, f, indent=2)
        return deleted
    return None

def main_page():
    st.title(f"Welcome, {st.session_state.username}!")
    
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    st.subheader("Password Saver, Generator and Strength Checker")
    password = st.text_input("Enter your password", type="password")

    if st.button("Check Password Strength"):
        if password_checker(password):
            st.success("Strong Password")
        else:
            st.error("Weak Password. Make sure it's at least 8 characters long and includes uppercase, lowercase, digits, and special characters.")

    name = st.text_input("Enter the name for the password: ")   
    saved_password = st.text_input("Enter password to save", type="password")

    if st.button("Save Password"):
        if saved_password and name:
            save_password(name, saved_password)
            st.success(f"Password for '{name}' saved successfully.")
        else:
            st.error("Please enter both name and password to save.")

    # Sidebar sections
    st.sidebar.title("📱 Password Manager")
    st.sidebar.header("💾 Saved Passwords")
    passwords = load_passwords()

    if passwords:
        for i, entry in enumerate(passwords):
            with st.sidebar.expander(f"🔑 {entry['name']}"):
                st.write(f"**Password:** `{entry['password']}`")
                if st.button(f"Delete", key=f"delete_{i}"):
                    deleted = delete_password(i)
                    if deleted:
                        st.sidebar.success(f"Deleted password for '{deleted['name']}'")
                        st.rerun()
    else:
        st.sidebar.write("No saved passwords yet.")

    st.sidebar.header("⚙️ Generator Settings")
    length = st.sidebar.slider("Password Length", 8, 50, 12)
    include_special = st.sidebar.checkbox("Include Special Characters", True)

    if st.sidebar.button("Generate Custom Password"):
        if include_special:
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
        else:
            characters = string.ascii_letters + string.digits
        
        custom_password = ''.join(random.choice(characters) for _ in range(length))
        st.sidebar.code(custom_password)

    st.sidebar.header("💡 Password Tips")
    st.sidebar.markdown("""
    - Use at least 8 characters
    - Include uppercase & lowercase
    - Add numbers and symbols
    - Avoid common words
    - Don't reuse passwords
    """)

    st.sidebar.header("📊 Statistics")
    st.sidebar.metric("Total Saved Passwords", len(passwords))
    if passwords:
        avg_length = sum(len(p['password']) for p in passwords) / len(passwords)
        st.sidebar.metric("Average Password Length", f"{avg_length:.1f}")

    st.subheader("Created by Dev")

def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Show appropriate page - FIXED LOGIC
    if st.session_state.logged_in:
        main_page()  # Show main page if logged in
    else:
        login_page()  # Show login page if not logged in

if __name__ == "__main__":
    main()