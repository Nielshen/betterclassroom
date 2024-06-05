from flask import Blueprint, Response
from app import classroom_repo


classroom_bp = Blueprint("classroom", __name__)


# returns all classrooms
@classroom_bp.route("/api/classroom", methods=["GET"])
def get_classroom():
    all_classrooms = list(classroom_repo.get_collection().find({}))
    if not all_classrooms:
        return Response("No classrooms found", 404)
    return all_classrooms


@classroom_bp.route("/api/classroom/<classroom_id>", methods=["GET"])
def get_classroom_by_id(classroom_id):
    classroom = classroom_repo.get_collection().find_one({"_id": classroom_id})
    if not classroom:
        return Response("Classroom not found", 404)
    return classroom
