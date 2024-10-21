#!/bin/bash

# Define the project directory and virtual environment
PROJECT_DIR="/Users/rolle/Projects/activitywatch-daily-export-to-md"
VENV_DIR="$PROJECT_DIR/venv"

# Activate the virtual environment
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install the required Python packages
python3 -m pip install python-dotenv

# Run the Python script
python3 "$PROJECT_DIR/process.py"

# Deactivate the virtual environment
deactivate
