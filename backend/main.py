from http.client import HTTPException
from typing import Dict
import warnings
warnings.filterwarnings("ignore")
from enum import Enum
from fastapi import FastAPI 
from pydantic import BaseModel
import joblib
import numpy as np

# load model and label encoders
model = joblib.load("random_forest_model.joblib")
encoders = joblib.load("label_encoders.joblib")

app = FastAPI()

class Gender(str, Enum):
    FEMALE = "female"
    MALE = "male"

class RaceEthnicity(str, Enum):
    GROUP_A = "group A"
    GROUP_B = "group B"
    GROUP_C = "group C"
    GROUP_D = "group D"
    GROUP_E = "group E"

class ParentalEducation(str, Enum):
    ASSOCIATES = "associate's degree"
    BACHELORS = "bachelor's degree"
    HIGHSCHOOL = "high school"
    MASTERS = "master's degree"
    SOME_COLLEGE = "some college"
    SOME_HIGH_SCHOOL = "some high school"

class Lunch(str, Enum):
    FREE_REDUCED = "free/reduced"
    STANDARD = "standard"

class TestPrepCourse(str, Enum):
    COMPLETED = "completed"
    NONE = "none"

class InputData(BaseModel):
    gender: Gender
    race_ethnicity: RaceEthnicity
    parental_level_of_education: ParentalEducation
    lunch: Lunch
    test_preparation_course: TestPrepCourse

class PredictionResult(BaseModel):
    user_input: Dict[str, str]
    prediction: float

@app.get("/")
def home():
    return "welcome to the homepage"

@app.get("/get_features")
def get_features():
    return list(encoders.keys())

@app.post("/predict", response_model=PredictionResult)
def predict(user_input: InputData):
    user_input = user_input.model_dump()
    X_test_sample = []

    for col in user_input:
        label_enc = encoders[col]  
        data = label_enc.transform([user_input[col]])
        X_test_sample.append(data.item())

    X_test_sample = np.array(X_test_sample).reshape(1, -1)
    try:
        pred = model.predict(X_test_sample)
        prediction = pred.item()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    return PredictionResult(user_input=user_input, prediction=prediction)

@app.get("/ping")
def ping():
    return {"status": "ok"}