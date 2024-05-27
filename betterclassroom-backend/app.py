import logging

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pydantic import BaseModel, ValidationError

from classroom import ClassroomRepository, Classroom, Table
from student import StudentRepository, Student
from course import CourseRepository, Course
from exercise import Exercise, SubExercise
from professor import ProfessorRepository, Professor

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
# username = "admin"
# password = "admin"

# Verbindungszeichenfolge erstellen
# connection = f"mongodb://{username}:{password}@mongodb.betterclassroom.svc.cluster.local:27017/"
connection = "mongodb://mongodb.betterclassroom.svc.cluster.local:27017/"
# connection = "mongodb://127.0.0.1:27017/"

print("MongoDB connection string:", connection)
client = MongoClient(connection)

try:
    client.admin.command("ping")
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

db = client["betterclassroom"]


classroom_repo = ClassroomRepository(db)

course_repo = CourseRepository(db)

students_repo = StudentRepository(db)

professor_repo = ProfessorRepository(db)


def validate_request(model: BaseModel):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if request.method == "POST":
                try:
                    data = request.get_json()
                    model(**data)
                except ValidationError as e:
                    return Response(str(e), 400)
                except TypeError:
                    return Response("No data provided", 400)
                return func(*args, **kwargs, data=data)
            else:
                return func(*args, **kwargs, data=None)

        wrapper.__name__ = f"validate_{func.__name__}"
        return wrapper

    return decorator


@app.route("/api")
def hello():
    return "Hello, World!"


# returns all students / creates new student
@app.route("/api/students", methods=["GET", "POST", "DELETE"])
@validate_request(Student)
def handle_students(data):
    if request.method == "GET":
        all_students = list(students_repo.get_collection().find({}))
        return all_students
    elif request.method == "POST":
        course = course_repo.get_collection().find_one(
            {"_id": data["course"]}, {"_id": 1}
        )
        if not course:
            return Response("Course not found", 404)
        students_repo.save(
            Student(
                id=data["id"],
                table=data["table"],
                course=data["course"],
            )
        )
        course_repo.get_collection().update_one(
            {"_id": data["course"]},
            {"$addToSet": {"participants": data["id"]}},
        )
        return Response("Student inserted successfully", status=201)
    elif request.method == "DELETE":
        students_repo.get_collection().delete_many({})
        return Response("All students deleted successfully", 200)


def to_boolean(value):
    """Converts a string that is 'true' or 'false' to a boolean value, otherwise returns the value unchanged."""
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
    return value


# returns student progress / updates student progress
@app.route("/api/students/<student>/progress", methods=["GET", "POST"])
def handle_student_progress(student):
    if request.method == "GET":
        student_data = students_repo.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        return student_data.progress

    elif request.method == "POST":
        progress_data = request.get_json()
        if not progress_data:
            return Response("No data provided", 400)
        try:
            progress_data = {k: to_boolean(v) for k, v in progress_data.items()} #k ist exercise_id, v ist true/false
            Student.__pydantic_validator__.validate_assignment(
                Student.model_construct(), "progress", progress_data
            )
        except ValidationError as e:
            return Response(str(e), 400)
        student_data = students_repo.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        course_data = course_repo.find_one_by({"id": student_data.course})

        exercise_ids = {exercise.id for exercise in course_data.exercises}
        if not all(ex_id in exercise_ids for ex_id in progress_data.keys()):
            return Response("Exercise not found in the course", 400)

        students_repo.get_collection().update_one(
            {"_id": student}, {"$set": {"progress": progress_data}}
        )
        return Response("Progress updated successfully", 200)


# returns student help status / updates student help status
@app.route("/api/students/<student>/help", methods=["GET", "POST"])
def handle_help(student):
    if request.method == "GET":
        student_data = students_repo.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        return jsonify(student_data.help_requested, student_data.table)
    elif request.method == "POST":
        student_data = students_repo.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        students_repo.get_collection().update_one(
            {"_id": student},
            {"$set": {"help_requested": not student_data.help_requested}},
        )
        return Response("Help status updated successfully", 200)


# returns all professors / creates new professor
@app.route("/api/professor", methods=["GET", "POST"])
@validate_request(Professor)
def handle_professors(data):
    if request.method == "GET":
        all_professors = list(professor_repo.get_collection().find({}))
        return all_professors
    elif request.method == "POST":
        professor_repo.save(
            Professor(
                id=generate_professor_id(),
                name=data["name"],
            )
        )
        return Response("Inserted professor successfully", status=201)


def generate_professor_id() -> int:
    professorCount = professor_repo.get_collection().count_documents({})
    return professorCount + 1


# returns all courses / creates new course
@app.route("/api/course", methods=["GET", "POST"])
@validate_request(Course)
def handle_courses(data):
    if request.method == "GET":
        all_courses = list(course_repo.get_collection().find({}))
        return all_courses
    elif request.method == "POST":
        professor_data = professor_repo.find_one_by({"id": data["professor"]})
        if professor_data is None:
            return Response("Professor not found", 404)
        classroom_data = classroom_repo.find_one_by({"id": data["classroom"]})
        if classroom_data is None:
            return Response("Classroom not found", 404)

        course_repo.save(
            Course(
                id=data["id"],
                description=data["description"],
                classroom=data["classroom"],
                professor=data["professor"],
            )
        )
        return Response("Inserted course successfully", status=201)


@app.route("/api/course/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    course_repo.get_collection().delete_one({"_id": course_id})
    return Response("Course deleted successfully", 200)


# returns all exercises / creates new exercise
@app.route("/api/course/<course_id>/exercise", methods=["GET", "POST"])
@validate_request(SubExercise)
def handle_exercises(course_id, data):
    if request.method == "GET":
        course = course_repo.get_collection().find_one(
            {"_id": course_id}, {"exercises": 1} #exercises ist hier alle Hauptaufgaben?
        )
        if not course or "exercises" not in course: #exercises ist hier alle Hauptaufgaben?
            return Response("Course not found or no exercises available", 404)
        return jsonify(course["exercises"])
    elif request.method == "POST":
        course = course_repo.get_collection().find_one(
            {"_id": course_id}, {"exercises": 1} #exercises ist hier alle Hauptaufgaben?
        )
        if not course:
            return Response("Course not found", 404)
        if any(ex["id"] == data["id"] for ex in course.get("exercises", [])):
            return Response("An exercise with this ID already exists.", 400)
        course_repo.get_collection().update_one(
            {"_id": course_id}, {"$push": {"exercises": data}}
        )
        return Response("Exercise added successfully", 201)


@app.route("/api/course/<course_id>/exercise/<exercise_id>", methods=["DELETE"])
def delete_exercise(course_id, exercise_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    course_repo.get_collection().update_one(
        {"_id": course_id}, {"$pull": {"exercises": {"id": exercise_id}}}
    )
    return Response("Exercise deleted successfully", 200)


# returns all classrooms
@app.route("/api/classroom", methods=["GET"])
def get_classroom():
    all_classrooms = list(classroom_repo.get_collection().find({}))
    if not all_classrooms:
        return Response("No classrooms found", 404)
    return all_classrooms


def fill_db():

    classroom_repo.save(
        Classroom(
            id="O-201",
            tablesPerRow=4,
            rows=5,
            tables=[Table(id=1, occupied=False), Table(id=2, occupied=False)],
        )
    )
    classroom_repo.save(
        Classroom(
            id="O-301",
            tablesPerRow=4,
            rows=5,
            tables=[Table(id=1, occupied=False), Table(id=2, occupied=False)],
        )
    )

    professor_repo.save(Professor(id=1, name="Prof. Dr. X"))


if __name__ == "__main__":
    fill_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
