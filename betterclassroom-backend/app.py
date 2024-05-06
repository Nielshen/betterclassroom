import logging

from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
# username = "admin"
# password = "admin"

# Verbindungszeichenfolge erstellen
# connection = f"mongodb://{username}:{password}@mongodb.betterclassroom.svc.cluster.local:27017/"
connection = f"mongodb://mongodb.betterclassroom.svc.cluster.local:27017/"

print("MongoDB connection string:", connection)
client = MongoClient(connection)

try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

db = client["betterclassroom"]

# Define the schema for classrooms and students
classroom_schema = {
    "name": "String",
    "tables_per_row": "Number",
    "rows_per_room": "Number",
    "tables": []
}

student_schema = {
    "name": "String",
    "chosen_seat": {
        "classroom_id": "ObjectId",
        "table_id": "ObjectId",
        "seat_id": "ObjectId"
    }
}

# Create collections
classrooms_collection = db['classrooms']
students_collection = db['students']

# Insert one table into the classrooms collection
classrooms_collection.insert_one({
    "name": "Classroom A",
    "tables_per_row": 1,
    "rows_per_room": 1,
    "tables": [
        {
            "table_number": 1,
            "row": 1,
            "col": 1,
            "seats": [
                {"seat_number": 1, "occupied": False},
                {"seat_number": 2, "occupied": False}
            ]
        }
    ]
})

# Insert one student into the students collection
student_data = {
    "name": "Alice",
    "chosen_seat": {
        "classroom_id": classrooms_collection.find_one({})["_id"],
        "table_id": classrooms_collection.find_one({})["tables"][0]["_id"],
        "seat_id": classrooms_collection.find_one({})["tables"][0]["seats"][0]["_id"]
    }
}
students_collection.insert_one(student_data)

# Update the chosen seat in the classrooms collection to mark it as occupied
chosen_seat = student_data["chosen_seat"]
classrooms_collection.update_one(
    {
        "_id": chosen_seat["classroom_id"],
        "tables._id": chosen_seat["table_id"],
        "tables.seats._id": chosen_seat["seat_id"]
    },
    {"$set": {"tables.$.seats.$[seat].occupied": True}},
    array_filters=[{"seat._id": chosen_seat["seat_id"]}]
)


@app.route("/api")
def hello():
    return "Hello, World!"


# Test API and MongoDB
@app.route("/api/students")
def get_students():
    all_students = list(students_collection.find({}, {"_id": 0}))
    return jsonify(all_students)


@app.route("/api/class_rooms")
def get_classroom():
    all_class_rooms = list(classrooms_collection.find({}, {"_id": 0}))
    return jsonify(all_class_rooms)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
