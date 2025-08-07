import streamlit as st
import requests

st.title("Student Exam Score Predictor")

# Input form
with st.form("input_form"):
    gender = st.selectbox("Gender", ["male", "female"])
    race_ethnicity = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
    parental_level_of_education = st.selectbox(
        "Parental Level of Education", 
        ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
    )
    lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
    test_preparation_course = st.selectbox("Test Preparation Course", ["none", "completed"])
    
    submit = st.form_submit_button("Predict")

if submit:
    payload = {
        "gender": gender,
        "race_ethnicity": race_ethnicity,
        "parental_level_of_education": parental_level_of_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation_course
    }

    with st.spinner("Sending request to backend..."):
        response = requests.post(
            "https://firstapp-z6qg.onrender.com/predict",
            headers={"Content-Type": "application/json"},
            json=payload
        )

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        st.success(f"Predicted Exam Score: {prediction:.2f}")
    else:
        st.error("Failed to get prediction from backend.")
