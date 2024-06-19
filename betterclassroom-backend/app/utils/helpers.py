from pydantic import BaseModel, ValidationError
from flask import request, Response
from app.db_models import Classroom, Table, Professor


def validate_request(model: BaseModel):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if request.method == "POST":
                try:
                    data = request.get_json()
                    model(**data)
                except ValidationError as e:
                    return Response(str(e), 400)
                except TypeError:
                    return Response("No data provided", 400)
                return func(*args, **kwargs, data=data)
            else:
                return func(*args, **kwargs, data=None)

        wrapper.__name__ = f"validate_{func.__name__}"
        return wrapper

    return decorator


def validate_socket_request(model: BaseModel):
    def decorator(func):
        def wrapper(self, json):
            try:
                validated_data = model(**json)
            except ValidationError as e:
                return {"error": str(e)}
            except TypeError:
                return {"error": "No valid data provided"}
            return func(self, validated_data)

        wrapper.__name__ = f"validate_{func.__name__}"
        return wrapper

    return decorator


def to_boolean(value):
    """Converts a string that is 'true' or 'false' to a boolean value, otherwise returns the value unchanged."""
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
    return value


def createO201(classroom_repo):
    # TODO fill with test data?

    tablesPerRow = 4
    rows = 5

    classroom_repo.save(
        Classroom(
            id="O-201",
            tablesPerRow=tablesPerRow,
            rows=rows,
            tables=[Table(id=i, occupied=False) for i in range(0, tablesPerRow * rows)],
        )
    )


def createO301(classroom_repo):
    tablesPerRow = 4
    rows = 5
    classroom_repo.save(
        Classroom(
            id="O-301",
            tablesPerRow=tablesPerRow,
            rows=rows,
            tables=[Table(id=i, occupied=False) for i in range(0, tablesPerRow * rows)],
        )
    )


def createProfEigslperger(professor_repo):
    professor_repo.save(Professor(id="Prof. Dr. Markus Eiglsperger"))
