from flask import Blueprint, request, Response, jsonify
from app.db_models.course import Course, Exercise, SubExercise
from app.utils.helpers import validate_request
from app import course_repo, professor_repo, classroom_repo, students_repo


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


@course_bp.route("/api/course/<course_id>/students", methods=["GET"])
def get_students(course_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    students = list(students_repo.get_collection().find({"course": course_id}))
    return students


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


@course_bp.route("/api/course/<course_id>/start", methods=["POST"])
def start_course(course_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    # Setze den Kursstatus auf 'aktiv'
    course_repo.get_collection().update_one(
        {"_id": course_id}, {"$set": {"is_active": True}}
    )
    return Response("Course started successfully", 200)


# Endpunkt zum Beenden des Kurses
@course_bp.route("/api/course/<course_id>/close", methods=["POST"])
def close_course(course_id):
    course = course_repo.get_collection().find_one({"_id": course_id})
    if not course:
        return Response("Course not found", 404)
    # Setze den Kursstatus auf 'inaktiv'
    course_repo.get_collection().update_one(
        {"_id": course_id}, {"$set": {"is_active": False}}
    )
    return Response("Course closed successfully", 200)


# add subexercise / delete exercise
@course_bp.route(
    "/api/course/<course_id>/exercise/<exercise_id>",
    methods=["POST", "GET", "DELETE", "PUT"],
)
@validate_request(SubExercise)
def handle_exercises_two(course_id, exercise_id, data):
    course = course_repo.find_one_by_id(course_id)
    if not course:
        return Response("Course not found", 404)

    exercise = next((ex for ex in course.exercises if ex.id == exercise_id), None)
    if not exercise:
        return Response("Exercise not found", 404)

    if request.method == "GET":
        sub_exercises = [sub.to_dict() for sub in exercise.exercises]
        return sub_exercises

    elif request.method == "POST":
        course_repo.get_collection().update_one(
            {"_id": course_id, "exercises.id": exercise_id},
            {"$push": {"exercises.$.exercises": data}},
        )
        return Response("Exercise added successfully", 201)
    elif request.method == "DELETE":
        course_repo.get_collection().update_one(
            {"_id": course_id}, {"$pull": {"exercises": {"id": exercise_id}}}
        )
        return Response("Exercise deleted successfully", 200)
    elif request.method == "PUT":
        data = request.get_json()
        if len(data) > 1:
            return Response("Only description can be modified", 400)

        if data.get("description") is None:
            return Response("No description field provided", 400)

        course_repo.get_collection().update_one(
            {
                "_id": course_id,
                "exercises.id": exercise_id,
            },
            {"$set": {"exercises.$[exercise].description": data["description"]}},
            array_filters=[{"exercise.id": exercise_id}],
        )
        return Response("Exercise updated successfully", 200)


@course_bp.route(
    "/api/course/<course_id>/exercise/<exercise_id>/<subexercise_id>",
    methods=["DELETE", "PUT"],
)
def alter_subexercise(course_id, exercise_id, subexercise_id):
    course = course_repo.find_one_by_id(course_id)
    if not course:
        return Response("Course not found", 404)

    exercise = next((ex for ex in course.exercises if ex.id == exercise_id), None)
    if not exercise:
        return Response("Exercise not found", 404)

    subexercise = next(
        (subex for subex in exercise.exercises if subex.id == subexercise_id), None
    )
    if not subexercise:
        return Response("Subexercise not found", 404)

    if request.method == "DELETE":
        course_repo.get_collection().update_one(
            {"_id": course_id, "exercises.id": exercise_id},
            {"$pull": {"exercises.$.exercises": {"id": subexercise_id}}},
        )
        return Response("SubExercise deleted successfully", 200)
    elif request.method == "PUT":
        data = request.get_json()

        if len(data) > 1:
            return Response("Only description can be modified", 400)

        if data.get("description") is None:
            return Response("No description field provided", 400)

        course_repo.get_collection().update_one(
            {
                "_id": course_id,
                "exercises.id": exercise_id,
                "exercises.exercises.id": subexercise_id,
            },
            {
                "$set": {
                    "exercises.$[exercise].exercises.$[subexercise].description": data[
                        "description"
                    ]
                }
            },
            array_filters=[
                {"exercise.id": exercise_id},
                {"subexercise.id": subexercise_id},
            ],
        )
        return Response("SubExercise updated successfully", 200)
