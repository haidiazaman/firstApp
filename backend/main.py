import warnings

warnings.filterwarnings("ignore")
import joblib
import numpy as np
from fastapi import FastAPI 
from http.client import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select  
from sql_utils import register_student, select_student_by_name
from data_models import (
    StudentCreate, InputData, PredictionResult, Student
)

# load model and label encoders 
model = joblib.load("random_forest_model.joblib")
encoders = joblib.load("label_encoders.joblib")

# load sql db -- will create if it doesnt exist yet
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine) 

app = FastAPI()

@app.get("/")
def home():
    return "welcome to the homepage"

@app.get("/ping")
def ping():
    return {"status": "ok"}
    
@app.post("/register")
def register(student_create: StudentCreate):
    student = Student.model_validate(student_create)
    register_student(student=student, engine=engine)
    return {"message": "Student Registered!"}

@app.get("/view_all_students")
def view_all_students():
    with Session(engine) as session:  
        statement = select(Student)  
        results = session.exec(statement).all()
        return [s.model_dump() for s in results]

@app.get("/students/{name}")
def get_student_by_name(name: str):
    student = select_student_by_name(name, engine=engine)
    return student

# put / patch?
@app.get("/edit")
def edit():
    return {"message": "<in progress>"}

# delete --> add auth later
@app.get("/delete")
def delete():
    return {"message": "<in progress>"}


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