from flask import Blueprint, request, Response, jsonify
from app.db_models import Student
from app import students_repo, course_repo
from app.utils.helpers import validate_request
import logging


student_bp = Blueprint("students", __name__)


@student_bp.route("/api/students", methods=["GET", "POST", "DELETE"])
@validate_request(Student)
def handle_students(data):
    if request.method == "GET":
        all_students = list(students_repo.get_collection().find({}))
        return all_students
    elif request.method == "POST":
        course = course_repo.find_one_by_id(data["course"])
        if not course:
            return Response("Course not found", 404)

        exercise = next(
            (ex for ex in course.exercises if ex.id == data["exercise"]), None
        )
        if not exercise:
            return Response("Exercise not found", 404)

        student = students_repo.find_one_by_id(data["id"])
        if student:
            return Response("Student with this ID already exists.", 400)

        students_repo.save(
            Student(
                id=data["id"],
                table=data["table"],
                course=data["course"],
                exercise=data["exercise"],
            )
        )

        course_repo.get_collection().update_one(
            {"_id": data["course"], "exercises.id": data["exercise"]},
            {"$addToSet": {"exercises.$.participants": data["id"]}},
        )

        data["_id"] = data.pop("id")
        data["action"] = "add"
        return Response("Student added successfully", status=201)
    elif request.method == "DELETE":
        students_repo.get_collection().delete_many({})
        course_repo.get_collection().update_many(
            {}, {"$set": {"exercises.$[].participants": []}}
        )
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
        course_repo.get_collection().update_one(
            {"_id": student.course, "exercises.id": student.exercise},
            {"$pull": {"exercises.$.participants": student.id}},
        )
        students_repo.delete_by_id(student.id)
        return Response("Student deleted successfully", 200)


@student_bp.route("/api/students/<student_id>/progress", methods=["GET", "POST"])
def handle_student_progress(student_id):
    student = students_repo.find_one_by({"id": student_id})
    logging.info(student)
    if student is None:
        return Response("Student not found", 404)

    if request.method == "GET":
        return student.current_exercise

    elif request.method == "POST":
        progress_data = request.get_json()
        if not progress_data:
            return Response("No data provided", 400)

        if progress_data.get("current_exercise") is None:
            return Response("current_exercise is required", 400)

        if not isinstance(progress_data.get("current_exercise"), int):
            return Response("current_exercise must be an integer", 400)

        students_repo.get_collection().update_one(
            {"_id": student_id},
            {"$set": {"current_exercise": progress_data.get("current_exercise")}},
        )
        return Response("Current exercise updated successfully", 200)


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
        return Response("Help requested updated successfully", 200)
