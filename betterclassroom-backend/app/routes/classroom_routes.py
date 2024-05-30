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
