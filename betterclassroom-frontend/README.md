# Frontend Project Structure and Components

This document provides an overview of the frontend project structure and explains the purpose of each component.

## Project Structure

```
betterclassroom-frontend/
├── public/                 # Static assets
├── src/                    # Source code
│   ├── assets/             # Project assets (images, styles, etc.)
│   ├── components/         # Vue components
│   ├── router/             # Vue Router configuration
│   ├── stores/             # Files for dataStores
│   ├── utils/              # Utility functions
│   ├── views/              # Vue views (pages)
│   ├── App.vue             # Root Vue component
│   ├── index.css           # Importing daisyUI
│   └── main.js             # Entry point for the application 
├── .gitignore              # Git ignore file
├── index.html              # Main HTML file
├── package.json            # Project dependencies and scripts
├── README.md               # Project documentation
└── vite.config.js          # Vite configuration file
```

## Components

### 1. DashboardPerson

This component is used to display the progress of a single student that can be reused.

### 2. DashboardTable

This component is used to display a table in the classroom and shows students if the seat is occupied.

### 3. NavBar

This component is used to display the main navigationbar of the project.

## Router

### index.js

This file is used to create the routes of the project.

## Stores

### dataStore.js

- `initStudent`: Initializes a new student object with default values.
- `saveStudentLocally`: Saves the student data to local storage.
- `saveProfessorLocally`: Saves the professor data to local storage.
- `checkUser`: Verifies if a user exists in the local storage.
- `checkProfessor`: Verifies if a professor exists in the local storage.
- `updateUserField`: Updates a specific field of the user object in local storage.
- `readUser`: Retrieves the user data from local storage.
- `readProfessor`: Retrieves the professor data from local storage.
- `deleteStudentLocally`: Removes the student data from local storage.
- `deleteProfessorLocally`: Removes the professor data from local storage.
- `updateTasks`: Updates the list of tasks in the local storage.
- `alterTask`: Modifies a specific task in the local storage.
- `addNewSubexercise`: Adds a new subexercise to a task in the local storage.
- `deleteSubexercise`: Removes a subexercise from a task in the local storage.

## Utils

### common.js

- `getApiUrl`: Constructs and returns the base URL for the API, typically based on the environment or configuration settings.

## views

### CourseView

This view is used to display courses that a professor has created.

### CreateCourseView

This view is used to create a course. 

- `loadCourse`: Fetches course data from the API using the course ID and populates the component's data properties.
- `pushCourse`: Sends course data to the API to create a new course or update an existing one based on the presence of a course ID.
- `deleteCourse`: Sends a request to the server to delete the course identified by the course ID in the route parameters and navigates back to the courses list upon success.
- `createTask`: Redirects the user to a page where they can create a new task for the current course.
- `editTask`: Redirects the user to a page where they can edit the task identified by the provided task ID within the current course.
- `startTask`: Sends a request to the server to start the task identified by the task ID, displays a course link for students, and navigates to the task's dashboard upon success.

### CreateTaskView

This view is used to create or edit tasks or subtasks from a course.

- `loadExercises`: Fetches the list of exercises from the API and populates the component's data properties.
- `createExercise`: Sends a request to the API to create a new exercise and updates the exercises list upon success.
- `deleteTask`: Sends a request to the API to delete a task identified by its ID and removes it from the local list of tasks.
- `addSubTask`: Adds a new sub-task to the current task's list of sub-tasks.
- `saveSubTask`: Sends a request to the API to save a new sub-task and updates the task's sub-tasks list upon success.
- `selectSubTaskToEdit`: Selects a sub-task for editing by populating the edit form with the sub-task's details.
- `saveEditedSubTask`: Sends a request to the API to save the edited sub-task and updates the task's sub-tasks list upon success.
- `deleteSubTask`: Sends a request to the API to delete a sub-task identified by its ID and removes it from the local list of sub-tasks.

### DashboardView

This view is used to display the dashboard for the professor.

- `fetchExercisesCount`: Retrieves the count of exercises from the API and updates the component's data properties.
- `loadCourse`: Fetches course details from the API using the course ID and populates the component's data properties.
- `handleStudentUpdate`: Handles updates to student information and sends the updated data to the API.
- `updateStudentProperty`: Updates a specific property of a student object in the component's data.
- `generateQRCode`: Generates a QR code for the course or task and displays it in the component.
- `copyToClipboard`: Copies a specified text (such as a course link) to the clipboard.
- `closeCourse`: Sends a request to the API to close the course and updates the course status in the component.

### ProfessorChangePasswordView

This view is used for the recoveryprocess of the password if forgotten.

- `saveLocally`: Saves the current state or data locally within the component.
- `requestChangePassword`: Sends a request to the API to initiate a password change process for the professor.
- `resetPassword`: Sends a request to the API to reset the professor's password and updates the component's state accordingly.

### ProfessorLoginView

This view is used as a login page for the professor. 

- `requestLogin`: Sends a request to the API to initiate the login process for the professor.
- `login`: Authenticates the professor by sending their credentials to the API and handles the login response.
- `changePassword`: Sends a request to the API to change the professor's password and updates the component's state based on the response.

### ProfessorRegisterView

This view is used as a register page for the professor.
 
- `requestRegister`: Sends a request to the API to initiate the registration process for a new professor.
- `register`: Completes the registration process by sending the professor's details to the API and handles the response.

### StudentTaskView

This view is used for students to join a course and choose a seat.

- `loadTasks`: Fetches the list of tasks from the API and populates the component's data properties.
- `changeIndex`: Changes the index of the current task or student in the component's data.
- `raisedHand`: Handles the event when a student raises their hand and updates the component's state accordingly.
- `submitStudent`: Submits the student's task or information to the API and updates the component's data.
- `deleteStudent`: Sends a request to the API to delete a student and removes them from the local list of students.
- `loadUser`: Fetches user details from the API and populates the component's data properties.
- `loadClassroom`: Fetches classroom details from the API and populates the component's data properties.
- `clickOnSeat`: Handles the event when a seat is clicked and updates the component's state or data accordingly.
- `getSeat`: Retrieves the details of a specific seat from the component's data.
- `isOccupied`: Checks if a specific seat is occupied by a student and returns a boolean value.

### TaskView

This view is used for students to view the tasks given to them.

- `nextTask`: Advances to the next task in the list and updates the component's state accordingly.
- `previousTask`: Moves to the previous task in the list and updates the component's state accordingly.
- `finishExercise`: Marks the current exercise as finished and updates the component's state or sends a request to the API.
- `toggleQuestion`: Toggles the visibility or state of a specific question in the component.


## Getting Started

1. Install the required dependencies:

   ```
   npm install
   ```

2. To run locally:

   ```
   npm run dev
   ```
