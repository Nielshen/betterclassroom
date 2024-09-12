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
        professor = professor_repo.find_one_by_id(data["email"])
        if professor:
            return Response("Professor with that ID already exists", status=400)

        professor_repo.save(
            Professor(
                id=data["id"],
                email=data["email"],
                password=data["password"],
                firstName=data["firstName"],
                lastName=data["lastName"],
            )
        )
        return Response("Inserted professor successfully", status=201)


j
@professor_bp.route("/api/professor/login", methods=["POST"])
def login_professor():
    """
    Loggt einen Professor ein.

    Argumente:
    - request.json: Ein JSON-Objekt, das die E-Mail und das Passwort des Professors enthält.
        - email (str): Die E-Mail-Adresse des Professors.
        - password (str): Das Passwort des Professors.

    Rückgabe:
    - Response: Eine HTTP-Antwort, entweder mit dem Professor-Objekt und dem Statuscode 200, oder mit dem Statuscode 401, falls die Anmeldeinformationen ungültig sind.
    """
    data = request.json
    professor = professor_repo.get_collection().find_one({"email": data["email"]})  
    if professor and professor["password"] == data["password"]:
        return jsonify(professor), 200
    return Response("Invalid credentials*", status=401)

    
    
    


@professor_bp.route("/api/professor/reset_password", methods=["POST"])
def reset_password():
    """
    Setzt das Passwort eines Professors zurück.

    Argumente:
    - request.json: Ein JSON-Objekt, das die E-Mail des Professors und das neue Passwort enthält.
        - email (str): Die E-Mail-Adresse des Professors.
        - new_password (str): Das neue Passwort des Professors.

    Rückgabe:
    - Response: Eine HTTP-Antwort, die den Erfolg oder Misserfolg des Zurücksetzens des Passworts anzeigt.
    """
    data = request.json
    professor = professor_repo.get_collection().find_one({"email": data["email"]})  
    if not professor:
        return Response("Professor not found", status=404)

    professor["password"] = data["password"]
    professor_repo.get_collection().update_one({"email": data["email"]}, {"$set": {"password": data["new_password"]}})
    return Response("Password updated successfully", status=200)



"""
def login_professor(data): pass

def get_professor_form_id(data): pass

def registerr_professor(data): pass
"""
