def register_sockets(socketio):
    from .student_socket import student_ns

    socketio.on_namespace(student_ns)
