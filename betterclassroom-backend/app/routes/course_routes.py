from flask import Blueprint, request, Response, jsonify
from app.db_models.course import Course, Exercise
from app.utils.helpers import validate_request
from app import course_repo, professor_repo, classroom_repo


course_bp = Blueprint("course", __name__)


# returns all courses / creates new course
@course_bp.route("/api/course", methods=["GET", "POST"])
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


@course_bp.route("/api/course/<course_id>", methods=["GET", "DELETE"])
def handle_course(course_id):
    if request.method == "GET":
        course = course_repo.get_collection().find_one({"_id": course_id})
        if not course:
            return Response("Course not found", 404)
        return course
    elif request.method == "DELETE":
        course = course_repo.get_collection().find_one({"_id": course_id})
        if not course:
            return Response("Course not found", 404)
        course_repo.get_collection().delete_one({"_id": course_id})
        return Response("Course deleted successfully", 200)


# returns all exercises / creates new exercise
@course_bp.route("/api/course/<course_id>/exercise", methods=["GET", "POST"])
@validate_request(Exercise)
def handle_exercises(course_id, data):
    if request.method == "GET":
        course = course_repo.get_collection().find_one(
            {"_id": course_id},
            {"exercises": 1},  # exercises ist hier alle Hauptaufgaben?
        )
        if (
            not course or "exercises" not in course
        ):  # exercises ist hier alle Hauptaufgaben?
            return Response("Course not found or no exercises available", 404)
        return jsonify(course["exercises"])
    elif request.method == "POST":
        course = course_repo.get_collection().find_one(
            {"_id": course_id},
            {"exercises": 1},  # exercises ist hier alle Hauptaufgaben?
        )
        if not course:
            return Response("Course not found", 404)
        if any(ex["id"] == data["id"] for ex in course.get("exercises", [])):
            return Response("An exercise with this ID already exists.", 400)
        course_repo.get_collection().update_one(
            {"_id": course_id}, {"$push": {"exercises": data}}
        )
        return Response("Exercise added successfully", 201)


@course_bp.route("/api/course/<course_id>/exercise/<exercise_id>", methods=["DELETE"])
def delete_exercise(course_id, exercise_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    course_repo.get_collection().update_one(
        {"_id": course_id}, {"$pull": {"exercises": {"id": exercise_id}}}
    )
    return Response("Exercise deleted successfully", 200)
