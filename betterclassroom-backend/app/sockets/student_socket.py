from flask_socketio import emit
from flask_socketio.namespace import Namespace


class StudentNamespace(Namespace):
    def on_connect(self):
        emit("response", {"data": "Connection established test123"})

    def on_disconnect(self):
        pass


student_ns = StudentNamespace("/student")
