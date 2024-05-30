from flask import Blueprint, request, Response
from app.db_models import Professor
from app.utils.helpers import validate_request, generate_professor_id
from app import professor_repo


professor_bp = Blueprint("professor", __name__)


# returns all professors / creates new professor
@professor_bp.route("/api/professor", methods=["GET", "POST"])
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
