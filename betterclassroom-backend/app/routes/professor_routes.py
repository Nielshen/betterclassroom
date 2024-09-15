from flask import Blueprint, request, Response, jsonify
from app.db_models import Professor
from app.utils.helpers import validate_request
from app import professor_repo

professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/api/professor", methods=["GET", "POST"])
@validate_request(Professor)
def handle_professors(data):
    if request.method == "GET":
        all_professors = list(professor_repo.get_collection().find({}))
        return jsonify(all_professors)

    elif request.method == "POST":
        professor = professor_repo.find_one_by_id(data["id"])
        if professor:
            return Response("Professor with that ID already exists", status=400)

        professor_repo.save(
            Professor(
                id=data["id"],  # email
                password=data["password"],
                firstName=data["firstName"],
                lastName=data["lastName"],
            )
        )
        return Response("Inserted professor successfully", status=201)


@professor_bp.route("/api/professor/login", methods=["POST"])
def login_professor():
    """
    Logs in a professor.

    Arguments:
    - request.json: A JSON object containing the professor's email and password.
        - email (str): The professor's email address.
        - password (str): The professor's password.

    Returns:
    - Response: An HTTP response, either with the professor object and status code 200, or with status code 401 if the credentials are invalid.
    """
    data = request.json
    professor = professor_repo.get_collection().find_one({"_id": data["email"]})
    if professor and professor["password"] == data["password"]:
        return jsonify(professor), 200
    return Response("Invalid credentials*", status=401)


@professor_bp.route("/api/professor/reset_password", methods=["POST"])
def reset_password():
    """
    Resets a professor's password.

    Arguments:
    - request.json: A JSON object containing the professor's email and the new password.
        - email (str): The professor's email address.
        - new_password (str): The new password of the professor.

    Returns:
    - Response: An HTTP response indicating the success or failure of the password reset.
    """
    data = request.json
    professor = professor_repo.get_collection().find_one({"email": data["email"]})
    if not professor:
        return Response("Professor not found", status=404)

    professor["password"] = data["password"]
    professor_repo.get_collection().update_one(
        {"email": data["email"]}, {"$set": {"password": data["new_password"]}}
    )
    return Response("Password updated successfully", status=200)
