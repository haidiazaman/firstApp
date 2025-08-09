import requests
import streamlit as st
from Home import PREFIX_URL

st.title("Register a New Student")

# Input form
with st.form("input_form"):
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["male", "female"])
    race_ethnicity = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
    parental_level_of_education = st.selectbox(
        "Parental Level of Education", 
        ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
    )
    lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
    test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
    
    submit = st.form_submit_button("Register")

if submit:
    if name.strip():
        payload = {
            "name": name,
            "gender": gender,
            "race_ethnicity": race_ethnicity,
            "parental_level_of_education": parental_level_of_education,
            "lunch": lunch,
            "test_preparation_course": test_preparation_course
        }

        with st.spinner("Sending request to backend..."):
            response = requests.post(
                f"{PREFIX_URL}/register",
                headers={"Content-Type": "application/json"},
                json=payload
            )

        if response.status_code == 200:
            st.success(f"Student registered!")
        else:
            st.error("Failed to register student.")
    else:
        st.error("Name cannot be null.")