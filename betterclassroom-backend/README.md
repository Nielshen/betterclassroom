# Backend Project Structure and Components

This document provides an overview of the backend project structure and explains the purpose of each component.

## Project Structure

```
├── app
│   ├── db_models
│   ├── routes
│   ├── sockets
│   ├── utils
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── README.md
├── requirements.txt
├── run.py
├── start.sh
└── swagger.yaml
```

## Components

### 1. app/db_models

This directory contains Pydantic models for database entities and their respective repositories.

- `classroom.py`: Defines the `Classroom` and `Table` models
- `course.py`: Contains `Course`, `Exercise`, and `SubExercise` models
- `professor.py`: Defines the `Professor` model
- `student.py`: Contains the `Student` model

These models represent the structure of the data stored in the database and provide methods for interacting with the data.

### 2. app/routes

This directory contains route handlers for different API endpoints.

- `classroom_routes.py`: Handles API routes related to classroom operations
- `course_routes.py`: Manages API routes for course-related operations
- `professor_routes.py`: Handles API routes for professor-related actions
- `student_routes.py`: Manages API routes for student-related operations

These files define the API endpoints and their corresponding logic.

### 3. app/sockets

This directory contains WebSocket-related functionality.

- `student_socket.py`: Implements WebSocket functionality for real-time communication with students

### 4. app/utils

This directory contains utility functions and helpers.

- `helpers.py`: Provides utility functions used across the application, such as `get_hash()`

### 5. app/main.py

The main application file that sets up the FastAPI application, includes routes, and configures any middleware or event handlers.

### 6. run.py

The entry point for running the application.

### 7. swagger.yaml

Contains the OpenAPI (Swagger) specification for the API, documenting all available endpoints, request/response structures, and other API details.

## Key Features

1. **Pydantic Models**: The project uses Pydantic for data validation
2. **MongoDB Integration**: The `pydantic_mongo.AbstractRepository` is used as MongoDB integration, creating collections and validating data on creation.
3. **FastAPI**: FastAPI is used as the web framework
4. **WebSocket Support**: Real-time communication is implemented for student interactions
5. **Dockerization**: The application is be containerized using Docker

## Getting Started

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. To run locally, set the environment variable `BETTERCLASSROOM_LOCAL`
   e.g., in Linux, do:

   ```
   export BETTERCLASSROOM_LOCAL=true
   ```

3. Forward ports in order to access the database (blocks terminal):

   ```
   kubectl port-forward svc/mongodb -n betterclassroom 27017:27017
   ```

4. Run the application:

   ```
   python run.py
   ```

5. Access the API documentation at `http://localhost:5000/api/docs`
