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
        return Response("Inserted professor successfully", status=201)



def login_professor(data): pass

def get_professor_form_id(data): pass

def registerr_professor(data): pass
