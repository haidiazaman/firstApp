import pandas as pd
import requests
import streamlit as st
from app import PREFIX_URL

st.title("View Student Records")

if st.button("View All Students"):
    with st.spinner("Sending request to backend..."):
        response = requests.get(
            f"{PREFIX_URL}/view_all_students",
            headers={"Content-Type": "application/json"},
        )

    if response.status_code == 200:
        st.success(f"Succesfully retrieved all students")
        try:
            data = response.json()
            # st.json(data) # nicely displays the json output
            df = pd.DataFrame(data)
            df = df[["name", "gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]]
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to parse respones JSON: {e}")
    else:
        st.error("Failed to retrieve records.")


name = st.text_input("Input the student name")
if st.button("View Student by Name"):
    if not name.strip():
        st.error("Please enter a valid student name before clicking the button.")
    else:
        with st.spinner("Sending request to backend..."):
            response = requests.get(
                f"{PREFIX_URL}/students/{name}",
                headers={"Content-Type": "application/json"},
            )

        if response.status_code == 200:
            st.success(f"Succesfully retrieved record for {name}")
            try:
                data = response.json()
                st.json(data)
            except Exception as e:
                st.error(f"Failed to parse respones JSON: {e}")
        else:
            st.error("Failed to retrieve records. {name} does not exist in database.")