from flask_socketio import emit
from flask_socketio.namespace import Namespace
from flask import request
import logging
from app import students_repo, course_repo
from app.db_models import Student
from app.utils.helpers import validate_socket_request


class StudentNamespace(Namespace):
    dashboard_sids = {}
    student_sids = {}

    def on_connect(self):
        logging.info("Client connected")
        emit("response", {"data": "Connection established"})

    def on_disconnect(self):
        try:
            self.dashboard_sids = {
                key: value
                for key, value in self.dashboard_sids.items()
                if value != request.sid
            }
            self.student_sids = {
                key: value
                for key, value in self.student_sids.items()
                if value != request.sid
            }
        except Exception as e:
            logging.error(f"Error removing from dict: {e}")
        logging.info("Client disconnected")

    def on_dashboard_register(self, data):
        dashboard = data.get("course") + "." + data.get("exercise")
        self.dashboard_sids[dashboard] = request.sid
        logging.info("Dashboard registered %s", request.sid)
        return {"success": "Dashboard socket registered successfully"}

    def on_student_register(self, data):
        student = (
            data.get("course") + "." + data.get("exercise") + "." + data.get("student")
        )
        self.student_sids[student] = request.sid
        logging.info("Student %s registered", request.sid)
        return {"success": "Student socket registered successfully"}

    @validate_socket_request(Student)
    def on_new_student(self, student_data):
        course = course_repo.find_one_by_id(student_data.course)
        if not course:
            return {"error": "Course not found"}

        exercise = next(
            (ex for ex in course.exercises if ex.id == student_data.exercise), None
        )
        if not exercise:
            return {"error": "Exercise not found"}

        student = students_repo.find_one_by_id(student_data.id)
        if student:
            return {"error": "Student with this ID already exists."}

        students_repo.save(
            Student(
                id=student_data.id,
                table=student_data.table,
                course=student_data.course,
                exercise=student_data.exercise,
            )
        )
        course_repo.get_collection().update_one(
            {"_id": student_data.course, "exercises.id": student_data.exercise},
            {"$addToSet": {"exercises.$.participants": student_data.id}},
        )

        student_data = dict(student_data)
        student_data["_id"] = student_data["id"]
        student_data["action"] = "add"

        emit(
            "student",
            {"data": student_data},
            to=self.dashboard_sids.get(
                student_data["course"] + "." + student_data["exercise"]
            ),
        )
        return {"success": "Student added successfully"}

    def on_delete_student(self, student_data):
        student = students_repo.find_one_by_id(student_data.get("id"))
        if not student:
            return {"error": "Student not found"}
        course_repo.get_collection().update_one(
            {"_id": student.course, "exercises.id": student.exercise},
            {"$pull": {"exercises.$.participants": student.id}},
        )
        students_repo.delete_by_id(student.id)

        emit(
            "student",
            {"data": {"action": "delete", "_id": student.id, "table": student.table}},
            to=self.dashboard_sids.get(student.course + "." + student.exercise),
        )
        return {"success": "Student deleted successfully"}

    def on_update_progress(self, student_data):
        student = students_repo.find_one_by({"id": student_data.get("id")})
        if student is None:
            return {"error": "Student not found"}

        if not student_data:
            return {"error": "No data provided"}

        if student_data.get("current_exercise") is None:
            return {"error": "current_exercise is required"}

        if not isinstance(student_data.get("current_exercise"), int):
            return {"error": "current_exercise must be an integer"}

        students_repo.get_collection().update_one(
            {"_id": student_data.get("id")},
            {"$set": {"current_exercise": student_data.get("current_exercise")}},
        )
        emit(
            "progress",
            {
                "data": {
                    "_id": student_data.get("id"),
                    "current_exercise": student_data.get("current_exercise"),
                    "table": student.table,
                }
            },
            to=self.dashboard_sids.get(student.course + "." + student.exercise),
        )

        return {"success": "Current exercise updated successfully"}

    def on_help(self, student_data):
        student = students_repo.find_one_by_id(student_data.get("id"))
        if student is None:
            return {"error": "Student not found"}
        changed_help = not student.help_requested
        students_repo.get_collection().update_one(
            {"_id": student.id},
            {"$set": {"help_requested": changed_help}},
        )

        emit(
            "help",
            {
                "data": {
                    "_id": student_data.get("id"),
                    "help_requested": changed_help,
                    "table": student.table,
                }
            },
            to=self.dashboard_sids.get(student.course + "." + student.exercise),
        )

        emit(
            "help",
            {
                "data": {
                    "_id": student_data.get("id"),
                    "help_requested": changed_help,
                    "table": student.table,
                }
            },
            to=self.student_sids.get(
                student.course + "." + student.exercise + "." + student.id
            ),
        )
        return {"success": "Help requested updated successfully"}

    def on_subexercise_description(self, course_data):
        course = course_repo.find_one_by_id(course_data.get("course"))
        if not course:
            return {"error": "Course not found"}

        exercise = next(
            (ex for ex in course.exercises if ex.id == course_data.get("exercise")),
            None,
        )
        if not exercise:
            return {"error": "Exercise not found"}

        course_repo.get_collection().update_one(
            {
                "_id": course_data.get("course"),
                "exercises.id": course_data.get("exercise"),
            },
            {"$set": {"exercises.$[exercise].description": course_data.get("description")}},
            array_filters=[{"exercise.id": course_data.get("exercise")}],
        )


student_ns = StudentNamespace("/student")
