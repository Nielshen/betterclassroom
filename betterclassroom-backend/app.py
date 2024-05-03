from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Connect to MongoDB
#client = MongoClient("mongodb://mongodb-mongodb.betterclassroom:27017/")
client = MongoClient("mongodb://mongodb.betterclassroom:27017/")
try:
    #client.admin.command('ismaster')
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

db = client["betterclassroom"]
students_collection = db["students"]

@app.route("/api")
def hello():
    return "Hello, World!"

#@app.route("/api/students")
#def get_students():
 #   students = [
  #      {"id": 1, "name": "Alice"},
   #     {"id": 2, "name": "Bob"}
    #]
    #return jsonify(students)

#Test API and MongoDB
@app.route("/api/students")
def get_students():
    students = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    # Clear existing data and insert new students
    students_collection.delete_many({})
    students_collection.insert_many(students)

    # Retrieve all students
    all_students = list(students_collection.find({}, {"_id": 0}))

    return jsonify(all_students)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
