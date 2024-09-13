from flask import Blueprint, Response, jsonify
from app import classroom_repo

classroom_bp = Blueprint("classroom", __name__)


@classroom_bp.route("/api/classroom", methods=["GET"])
def get_classroom():
    all_classrooms = list(classroom_repo.get_collection().find({}))
    if not all_classrooms:
        return Response("No classrooms found", 404)
    return jsonify(all_classrooms)

@classroom_bp.route("/api/classroom/<classroom_id>", methods=["GET"])
def get_classroom_by_id(classroom_id):
    classroom = classroom_repo.get_collection().find_one({"_id": classroom_id})
    if not classroom:
        return Response("Classroom not found", 404)
    return classroom


@classroom_bp.route("/api/classroom/<classroom_id>/table/<table_id>/<seat_side>/occupied", methods=["GET"])
def is_seat_occupied(classroom_id, table_id, seat_side):
    if seat_side == 'L':
        seat_side = 'left'
    elif seat_side == 'R':
        seat_side = 'right'
    else:
        return Response("Invalid seat side provided", 400)

    # Find the classroom
    classroom = classroom_repo.get_collection().find_one({"_id": classroom_id})
    if not classroom:
        return Response("Classroom not found", 404)

    table_id = int(table_id)
    table = next((t for t in classroom['tables'] if t['id'] == table_id), None)
    if not table:
        return Response("Table not found", 404)

    # Check seat occupation status and return True/False
    if seat_side == 'left':
        return jsonify({"occupied": table['occupied_left']})
    elif seat_side == 'right':
        pass
    return jsonify({"occupied": table['occupied_right']})


@classroom_bp.route("/api/classroom/<classroom_id>/table/<table_id>/<seat_side>", methods=["POST"])
def update_seat_occupation(classroom_id, table_id, seat_side):
    # Validate seat side
    if seat_side == 'L':
        seat_side_field = 'occupied_left'
    elif seat_side == 'R':
        seat_side_field = 'occupied_right'
    else:
        return Response("Invalid seat side provided", 400)

    # Find the classroom
    classroom = classroom_repo.get_collection().find_one({"_id": classroom_id})
    if not classroom:
        return Response("Classroom not found", 404)

    # Convert table_id to an integer
    table_id = int(table_id)

    # Find the requested table
    table = next((t for t in classroom['tables'] if t['id'] == table_id), None)
    if not table:
        return Response("Table not found", 404)

    # Check if seat is already occupied
    if table[seat_side_field]:
        return Response(f"Seat on {seat_side} side of table {table_id} is already occupied", 400)

    # Update seat occupation status to True
    update_query = {f"tables.$.{seat_side_field}": True}

    # Update the seat occupation in the database
    classroom_repo.get_collection().update_one(
        {"_id": classroom_id, "tables.id": table_id},
        {"$set": update_query}
    )

    return Response(f"Seat on {seat_side} side of table {table_id} successfully occupied", 200)
