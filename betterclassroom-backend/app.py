import logging

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from pymongo import MongoClient

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

classroom = ClassroomRepository(db)

course = CourseRepository(db)

students = StudentRepository(db)

professor = ProfessorRepository(db)


@app.route("/api")
def hello():
    return "Hello, World!"


# returns all students / creates new student
@app.route("/api/students", methods=["GET", "POST"])
def handle_students():
    if request.method == "GET":
        all_students = list(students.get_collection().find({}))
        return all_students
    elif request.method == "POST":
        student_data = request.get_json()
        students.save(
            Student(
                id=student_data["id"],
                table=student_data["table"],
                course=student_data["course"],
                progress={},
                help_requested=False,
            )
        )
        # TODO check if course exists and if table exists and is not occupied
        course.get_collection().update_one(
            {"_id": student_data["course"]},
            {"$addToSet": {"participants": student_data["id"]}},
        )
        return Response("Student inserted successfully", status=201)


# returns student progress / updates student progress
@app.route("/api/students/<student>/progress", methods=["GET", "POST"])
def handle_student_progress(student):
    if request.method == "GET":
        student_data = students.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        return student_data.progress

    elif request.method == "POST":
        progress_data = request.get_json()
        if not progress_data:
            return Response("No data provided", 400)
        student_data = students.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        students.get_collection().update_one(
            {"_id": student}, {"$set": {"progress": progress_data}}
        )
        return Response("Progress updated successfully", 200)


# returns student help status / updates student help status
@app.route("/api/students/<student>/help", methods=["GET", "POST"])
def handle_help(student):
    if request.method == "GET":
        student_data = students.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        return jsonify(student_data.help_requested, student_data.table)
    elif request.method == "POST":
        student_data = students.find_one_by({"id": student})
        if student_data is None:
            return Response("Student not found", 404)
        students.get_collection().update_one(
            {"_id": student},
            {"$set": {"help_requested": not student_data.help_requested}},
        )
        return Response("Help status updated successfully", 200)


# returns all professors / creates new professor
@app.route("/api/professor", methods=["GET", "POST"])
def handle_professors():
    if request.method == "GET":
        all_professors = list(professor.get_collection().find({}))
        return all_professors
    elif request.method == "POST":
        data = request.get_json()
        professor.save(
            Professor(
                id=generate_professor_id(),
                name=data["name"],
            )
        )
        return Response("Inserted professor successfully", status=201)


def generate_professor_id() -> int:
    professorCount = professor.get_collection().count_documents({})
    return professorCount + 1


# returns all courses / creates new course
@app.route("/api/course", methods=["GET", "POST"])
def handle_courses():
    if request.method == "GET":
        all_courses = list(course.get_collection().find({}))
        return all_courses
    elif request.method == "POST":
        data = request.get_json()
        course.save(
            Course(
                id=data["id"],
                description=data["description"],
                exercises=[],
                participants=[],
                classroom=data["classroom"],
                professor=data["professor"],
            )
        )
        return Response("Inserted course successfully", status=201)


# returns all exercises / creates new exercise
@app.route("/api/course/<course_id>/exercise", methods=["GET", "POST"])
def handle_exercises(course_id):
    if request.method == "GET":
        courses = course.get_collection().find({"_id": course_id})
        course_exercises = [
            exercise for course in courses for exercise in course["exercises"]
        ]
        return course_exercises
    elif request.method == "POST":
        exercise_data = request.get_json()
        if not exercise_data:
            return Response("No data provided", 400)
        course_data = course.find_one_by({"_id": course_id})
        if course_data is None:
            return Response("Course not found", 404)
        course_data.exercises.append(exercise_data)
        course.save(course_data)
        return Response("Exercise added successfully", 201)


# returns all classrooms
@app.route("/api/classroom", methods=["GET"])
def get_classroom():
    all_classrooms = list(classroom.get_collection().find({}))
    return all_classrooms


def fill_db():

    classroom.save(
        Classroom(
            id="O-201",
            tablesPerRow=4,
            rows=5,
            tables=[Table(id=1, occupied=False), Table(id=2, occupied=False)],
        )
    )
    classroom.save(
        Classroom(
            id="O-301",
            tablesPerRow=4,
            rows=5,
            tables=[Table(id=1, occupied=False), Table(id=2, occupied=False)],
        )
    )

    professor.save(Professor(id=1, name="Prof. Dr. X"))


if __name__ == "__main__":
    fill_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
