# streamlit_app.py
import streamlit as st
from admin_interface import admin_interface
from user_interface import user_interface

def login_screen():
    """
    Simple login for demonstration. In real usage, implement something more secure.
    """
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "secret":
            st.session_state["is_admin"] = True
            st.success("Logged in as Admin!")
            return True
        else:
            st.error("Invalid credentials.")
    return False

def main():
    st.set_page_config(page_title="FAISS RAG App", layout="wide")
    st.title("Ask me Anything!")
    # st.sidebar.write("Switch between User and Admin")

    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    mode = st.sidebar.radio("Switch between User and Admin", ["Admin", "User"])

    if mode == "Admin":
        if not st.session_state["is_admin"]:
            authenticated = login_screen()
            if authenticated:
                admin_interface()
        else:
            admin_interface()
    else:
        user_interface()

if __name__ == "__main__":
    main()
