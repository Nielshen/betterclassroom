from flask import Blueprint, request, Response
from app.db_models import Professor
from app.utils.helpers import validate_request
from app import professor_repo


professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/api/professor", methods=["GET", "POST"])
@validate_request(Professor)
def handle_professors(data):
    if request.method == "GET":
        all_professors = list(professor_repo.get_collection().find({}))
        return all_professors
    elif request.method == "POST":
        professor = professor_repo.find_one_by_id(data["id"])
        if professor:
            return Response("Professor with that ID already exists", status=400)

        professor_repo.save(
            Professor(
                id=data["id"],
            )
        )
        return Response("Added professor successfully", status=201)


@professor_bp.route("/api/professor/<professor_id>", methods=["DELETE"])
def delete_professor(professor_id):
    professor = professor_repo.find_one_by_id(professor_id)
    if not professor:
        return Response("Professor not found", status=404)

    professor_repo.get_collection().delete_one({"_id": professor_id})
    return Response("Professor deleted successfully", status=200)
