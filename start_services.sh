#!/bin/bash

# Function to run kubectl port-forward with automatic restart
run_kubectl_port_forward() {
    while true; do
        echo "Starting kubectl port-forward..."
        kubectl port-forward svc/mongodb -n betterclassroom 27017:27017
        echo "kubectl port-forward stopped. Restarting in 5 seconds..."
        sleep 5
    done
}

# Function to change directory, activate venv if present, and run a command
cd_and_run() {
    echo "Changing to directory: $1"
    cd "$1" || exit
    
    # Activate virtual environment if it exists
    if [ -d ".venv" ]; then
        echo "Activating virtual environment"
        source .venv/bin/activate
    fi
    
    echo "Running: $2"
    $2
}

# Start MongoDB port forwarding in a separate process
run_kubectl_port_forward &
KUBECTL_PID=$!

# Change to backend directory, activate venv, and start the Python script
cd_and_run "betterclassroom-backend" "python run.py" &
BACKEND_PID=$!

# Change to frontend directory and start npm
cd_and_run "betterclassroom-frontend" "npm run dev" &
FRONTEND_PID=$!

echo "All processes have been started. Press Ctrl+C to stop all processes."

# Function to kill all started processes
cleanup() {
    echo "Stopping all processes..."
    kill $KUBECTL_PID $BACKEND_PID $FRONTEND_PID
    exit 0
}

# Set up trap to call cleanup function on script exit
trap cleanup EXIT

# Wait for all background processes
wait