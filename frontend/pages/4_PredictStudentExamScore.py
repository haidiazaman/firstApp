import time
import requests
import streamlit as st
from Home import PREFIX_URL

st.title("Predict Exam Score for an Existing Student")

name = st.text_input("Input the student name")
if st.button("Predict Exam Score"):
    if not name.strip():
        st.error("Please enter a valid student name before clicking the button.")
    else:
        with st.spinner("Sending request to backend..."):
            response = requests.get(
                f"{PREFIX_URL}/students/{name}",
                headers={"Content-Type": "application/json"},
            )

        if response.status_code == 200:
            st.success(f"Student details:")
            try:
                data = response.json()
                st.json(data)
                
            except Exception as e:
                st.error(f"Failed to parse respones JSON: {e}")

            data.pop("name") # remove name as it is not part of /predict API expected payload
            payload = data

            with st.spinner("Sending request to backend..."):
                response = requests.post(
                    f"{PREFIX_URL}/predict",
                    headers={"Content-Type": "application/json"},
                    json=payload
                )
                time.sleep(2) # pause for 1 second

            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"Predicted Exam Score: {prediction:.2f}")
            else:
                st.error("Failed to get prediction from backend.")
        else:
            st.error(f"Failed to retrieve records. {name} does not exist in database.")


