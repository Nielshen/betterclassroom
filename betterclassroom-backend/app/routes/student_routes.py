from flask import Blueprint, request, Response, jsonify
from pydantic import ValidationError
from app.db_models import Student
from app import students_repo, course_repo, socketio
from app.utils.helpers import validate_request


student_bp = Blueprint("students", __name__)


# returns all students / creates new student
@student_bp.route("/api/students", methods=["GET", "POST", "DELETE"])
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
        socketio.emit("student", {"data": data}, namespace="/student")
        return Response("Student inserted successfully", status=201)
    elif request.method == "DELETE":
        students_repo.get_collection().delete_many({})
        return Response("All students deleted successfully", 200)


@student_bp.route("/api/students/<student_id>", methods=["GET", "DELETE"])
def handle_student(student_id):
    if request.method == "GET":
        student = students_repo.get_collection().find_one({"_id": student_id})
        if not student:
            return Response("Student not found", 404)
        return student
    elif request.method == "DELETE":
        student = students_repo.find_one_by_id(student_id)
        if not student:
            return Response("Student not found", 404)
        students_repo.delete_by_id(student.id)
        return Response("Student deleted successfully", 200)


def to_boolean(value):
    """Converts a string that is 'true' or 'false' to a boolean value, otherwise returns the value unchanged."""
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
    return value


# returns student progress / updates student progress
@student_bp.route("/api/students/<student_id>/progress", methods=["GET", "POST"])
def handle_student_progress(student_id):
    if request.method == "GET":
        student = students_repo.find_one_by({"id": student_id})
        if student is None:
            return Response("Student not found", 404)
        return student.progress

    elif request.method == "POST":
        progress_data = request.get_json()
        if not progress_data:
            return Response("No data provided", 400)
        try:
            progress_data = {
                k: to_boolean(v) for k, v in progress_data.items()
            }  # k ist exercise_id, v ist true/false
            Student.__pydantic_validator__.validate_assignment(
                Student.model_construct(), "progress", progress_data
            )
        except ValidationError as e:
            return Response(str(e), 400)
        student = students_repo.find_one_by({"id": student_id})
        if student is None:
            return Response("Student not found", 404)
        course_data = course_repo.find_one_by({"id": student.course})

        exercise_ids = {exercise.id for exercise in course_data.exercises}
        if not all(ex_id in exercise_ids for ex_id in progress_data.keys()):
            return Response("Exercise not found in the course", 400)

        students_repo.get_collection().update_one(
            {"_id": student_id}, {"$set": {"progress": progress_data}}
        )
        result_data = {"id": student_id, "progress": progress_data}
        socketio.emit("progress", {"data": result_data}, namespace="/student")
        return Response("Progress updated successfully", 200)


# returns student help status / updates student help status
@student_bp.route("/api/students/<student_id>/help", methods=["GET", "POST"])
def handle_help(student_id):
    if request.method == "GET":
        student = students_repo.find_one_by({"id": student_id})
        if student is None:
            return Response("Student not found", 404)
        return jsonify(student.help_requested, student.table)
    elif request.method == "POST":
        student = students_repo.find_one_by({"id": student_id})
        if student is None:
            return Response("Student not found", 404)
        students_repo.get_collection().update_one(
            {"_id": student_id},
            {"$set": {"help_requested": not student.help_requested}},
        )
        socketio.emit(
            "help",
            {"data": {"id": student_id, "help_requested": not student.help_requested}},
            namespace="/student",
        )
        return Response("Help status updated successfully", 200)
