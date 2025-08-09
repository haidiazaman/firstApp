from data_models import Student
from http.client import HTTPException
from sqlmodel import Session, select  


def register_student(student: Student, engine):
    with Session(engine) as session:
        session.add(student)
        session.commit()

def select_student_by_name(name: str, engine):
    with Session(engine) as session:
        statement = select(Student).where(Student.name == name)
        student = session.exec(statement).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student