import json
import os

FILE_NAME = os.path.join(os.path.dirname(__file__), "students.json")


class Student:
    def __init__(self, name, surname, grade, present=True):
        self.name = name
        self.surname = surname
        self.grade = grade
        self.present = present

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "grade": self.grade,
            "present": self.present,
        }


def save_students(students):
    with open(FILE_NAME, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=4)


def load_students():
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
        return [Student(d["name"], d["surname"], d["grade"], d["present"]) for d in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []