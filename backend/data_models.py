from requests import Session
from sqlalchemy import create_engine
from sqlmodel import Field, SQLModel
from enum import Enum
from typing import Dict
from pydantic import BaseModel

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

class StudentCreate(InputData):
    name: str

class Student(StudentCreate, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)