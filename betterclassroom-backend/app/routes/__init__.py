def register_routes(app):
    from .student_routes import student_bp
    from .course_routes import course_bp
    from .professor_routes import professor_bp
    from .classroom_routes import classroom_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(classroom_bp)
