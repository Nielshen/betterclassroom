from flask_socketio import emit
from flask_socketio.namespace import Namespace
import logging


class StudentNamespace(Namespace):
    def on_connect(self):
        emit("response", {"data": "Connection established"})

    def on_disconnect(self):
        logging.info("Client disconnected")

    def on_message(self, message):
        response_message = f"Received your message: {message}"
        emit("response", {"data": response_message})


student_ns = StudentNamespace("/student")
