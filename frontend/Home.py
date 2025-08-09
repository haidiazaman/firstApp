import streamlit as st

PREFIX_URL = "http://127.0.0.1:8000" 
# PREFIX_URL = "https://firstapp-z6qg.onrender.com"

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


st.title("Welcome to the Student Management App 🎓")

st.write("""
There are **6 different things** you can do — just use the sidebar to navigate:

- Register a student
- View existing student records
- Predict exam score for a sample student
- Predict exam score for an existing student
- Edit student records (if you have permissions)
- Delete student records (if you have permissions)

Click on the page names in the sidebar to get started!
""")
