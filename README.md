# BetterClassroom Project

BetterClassroom is a comprehensive classroom management system with a Vue.js frontend, Python Flask + SocketIO backend, and MongoDB database.

## Project Structure

```
├── betterclassroom-backend
│   └── app
│       ├── db_models
│       ├── routes
│       ├── sockets
│       └── utils
├── betterclassroom-frontend
│   └── src
│       ├── assets
│       ├── components
│       ├── router
│       ├── stores
│       ├── utils
│       └── views
└── kubernetes
    ├── docs
    └── flux-system
```

## Components

### 1. Frontend

The frontend is built with Vue.js and includes the following key directories:

- `src`: Contains the main source code for the Vue.js application
  - `assets`: Static assets like images and global styles
  - `components`: Reusable Vue components
  - `router`: Vue Router configuration
  - `stores`: Pinia stores for state management
  - `utils`: Utility functions and helpers
  - `views`: Vue components representing different pages or views
- `cypress`: End-to-end testing setup using Cypress
- `public`: Public assets that are copied to the build output directory

### 2. Backend

The backend is built with Python Flask and SocketIO, structured as follows:

- `app`: Main application directory
  - `db_models`: Database models for MongoDB integration
  - `routes`: API route handlers
  - `sockets`: WebSocket functionality using SocketIO
  - `utils`: Utility functions and helpers

### 3. Database

The project uses MongoDB as its database system. The database models are defined in the `db_models` directory of the backend.

### 4. Kubernetes (kubernetes)

The `kubernetes` directory contains configuration files for deploying the application to a Kubernetes cluster:

- `docs`: Documentation related to Kubernetes deployment
- `flux-system`: Configuration files for the Flux CD system

## Getting Started

1. Clone the repository:

   ```
   git clone https://gitlab.in.htwg-konstanz.de/lehre/meiglspe/sose24/betterclassroom.git
   cd betterclassroom
   ```

2. Follow the instructions under the `kubernetes` directory to setup your local kubernetes cluster

3. Set up the backend:

   ```
   cd betterclassroom-backend
   pip install -r requirements.txt
   ```

   To run the backend locally:

   a. Set the environment variable:

   ```
   export BETTERCLASSROOM_LOCAL=true
   ```

   b. Forward the database port:

   ```
   kubectl port-forward svc/mongodb -n betterclassroom 27017:27017
   ```

4. Set up the frontend:

   ```
   cd ../betterclassroom-frontend
   npm install
   npm run dev
   ```

5. Access the frontend at `http://localhost:5173`

## Development

- Backend: The Flask application is located in `betterclassroom-backend/app/main.py`
- Frontend: The Vue.js application entry point is `betterclassroom-frontend/src/main.js`
- Database: Ensure MongoDB is running and properly configured in the backend

## License

BetterClassroom is available under the MIT license. See LICENSE for the full license text.
