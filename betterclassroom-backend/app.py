import logging

from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from classroom import ClassroomRepository, Classroom, Table
from student import StudentRepository, Student
from course import CourseRepository, Course
from exercise import Exercise, SubExercise

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
# username = "admin"
# password = "admin"

# Verbindungszeichenfolge erstellen
# connection = f"mongodb://{username}:{password}@mongodb.betterclassroom.svc.cluster.local:27017/"
connection = f"mongodb://mongodb.betterclassroom.svc.cluster.local:27017/"

print("MongoDB connection string:", connection)
client = MongoClient(connection)

try:
    client.admin.command("ping")
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

db = client["betterclassroom"]

# Example: Create a classroom
classroom = ClassroomRepository(db)

classroom.save(
    Classroom(
        id="O-301",
        tablesPerRow=4,
        rows=5,
        tables=[
            Table(_id=1, occupied=False),
            Table(_id=2, occupied=False),
        ],
    )
)


classroom.save(
    Classroom(
        id="O-201",
        tablesPerRow=4,
        rows=5,
        tables=[
            Table(_id=1, occupied=False),
            Table(_id=2, occupied=False),
            Table(_id=3, occupied=False),
            Table(_id=4, occupied=False),
        ],
    )
)


students = StudentRepository(db)
students.save(Student(id="Alice", table=Table(id=1, occupied=True), progress={}))
students.save(Student(id="Bernardo", table=Table(id=2, occupied=True), progress={}))


course = CourseRepository(db)
course.save(
    Course(
        id="SWQS",
        description="Software quality",
        exercises=[
            Exercise(
                id="User stories",
                description="Construct user stories",
                exercises=[SubExercise(id="Setup", description="")],
            )
        ],
        participants=["Bernardo"],
        classroom="O-201",
        professor="Prof. Dr. X",
    )
)


@app.route("/api")
def hello():
    return "Hello, World!"


# Test API and MongoDB
@app.route("/api/students")
def get_students():
    # # Retrieve student
    all_students = list(students.find({}, {"_id": 0}))
    return jsonify(all_students)


@app.route("/api/students/<student>/exercises", method="GET")
def get_student_exercises(student):
    course = db["course"].find_one({"participants": student})
    exercises = course["exercises"]

    return jsonify(exercises)


@app.route("/api/classroom")
def get_classroom():
    classroom1 = list(classroom.get_collection().find({"_id": "O-201"}))
    return jsonify(classroom1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
