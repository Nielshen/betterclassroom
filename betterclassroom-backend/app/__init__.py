from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
import logging
from app.db_models import (
    ClassroomRepository,
    CourseRepository,
    StudentRepository,
    ProfessorRepository,
)
from app.utils.helpers import createO201, createO301, createProfEigslperger
import os

socketio = SocketIO(
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    async_mode="eventlet",
    path="/api/socket.io",
)


def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio.init_app(app)

    logging.basicConfig(level=logging.DEBUG)

    # fmt: off
    connection = "mongodb://127.0.0.1:27017/" if os.getenv("BETTERCLASSROOM_LOCAL") else "mongodb://mongodb.betterclassroom.svc.cluster.local:27017/"
    # fmt: on
    logging.info("MongoDB connection string: %s", connection)

    client = MongoClient(connection)

    try:
        client.admin.command("ping")
        logging.info("MongoDB connection successful")
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")

    global db
    db = client["betterclassroom"]

    global classroom_repo
    classroom_repo = ClassroomRepository(db)

    global course_repo
    course_repo = CourseRepository(db)

    global students_repo
    students_repo = StudentRepository(db)

    global professor_repo
    professor_repo = ProfessorRepository(db)

    from .routes import register_routes

    register_routes(app)

    from .sockets import register_sockets

    register_sockets(socketio)

    createO201(classroom_repo)
    createO301(classroom_repo)
    createProfEigslperger(professor_repo)

    return app
