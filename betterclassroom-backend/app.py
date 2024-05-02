from flask import Flask, jsonify
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route("/api")
def hello():
    return "Hello, World!"

@app.route("/api/students")
def get_students():
    students = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    return jsonify(students)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
