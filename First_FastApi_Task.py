from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

student = {
    1: {"name": "asma",
        "age": 24,
        "section": "bs"
        }
}


class students(BaseModel):
    name: str
    age: int
    section: str


class updatestd(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    section: Optional[str] = None


@app.get("/")
def index():
    return {"name": "hellow"}


@app.get("/get_student/{std_id}")
def get_student(stdi_id: int):
    return student[stdi_id]

# query endpoint


@app.get("/get_by_name")
def get_by_name(*, std_id: Optional[int] = None, name: str):
    for std_id in student:
        if student[std_id]["name"] == name:
            return student[std_id]
    return {"data": "not found"}
# post method


@app.post("/create_std/{st_id}")
def create(std_id: int, students: students):
    if std_id in student:
        return {"student ": "exist"}
    student[std_id] = students
    return student[std_id]

# put method


@app.put("/update_by_id/{std_id}")
def update(std: int, students: updatestd):
    if std not in student:
        return {"data": "not found"}
    if students.name != None:
        student[std].name = students.name
    if students.age != None:
        student[std].age = students.age
    if students.section != None:
        student[std].section = students.section
    # student[std] = students
    return student[std]

# delete request


@app.delete("/delete/{std_id}")
def delete_std(std: int):
    if std not in student:
        return {"not found"}
    del student[std]
    return {"deleted"}
