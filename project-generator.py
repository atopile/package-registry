# Python script to generate the proposed project structure

import os

def create_project_structure(base_path, project_name):
    # Define the directories to be created
    directories = [
        f"{base_path}/{project_name}/app",
        f"{base_path}/{project_name}/app/query_interface",
        f"{base_path}/{project_name}/app/parsing",
        f"{base_path}/{project_name}/app/utilities",
        f"{base_path}/{project_name}/tests",
        f"{base_path}/{project_name}/venv",
    ]

    # Define the files to be created
    files = {
        f"{base_path}/{project_name}/app/__init__.py": "",
        f"{base_path}/{project_name}/app/main.py": "# Main application setup and routes\n",
        f"{base_path}/{project_name}/app/query_interface/__init__.py": "",
        f"{base_path}/{project_name}/app/query_interface/query_handler.py": "# Handles querying the database\n",
        f"{base_path}/{project_name}/app/parsing/__init__.py": "",
        f"{base_path}/{project_name}/app/parsing/parser_type_1.py": "# A specific type of parsing script\n",
        f"{base_path}/{project_name}/app/parsing/parser_type_2.py": "# Another type of parsing script\n",
        f"{base_path}/{project_name}/app/utilities/__init__.py": "",
        f"{base_path}/{project_name}/app/utilities/firebase_setup.py": "# Setup Firebase connection\n",
        f"{base_path}/{project_name}/tests/__init__.py": "",
        f"{base_path}/{project_name}/tests/test_main.py": "# Tests for main application functionality\n",
        f"{base_path}/{project_name}/tests/test_parsers.py": "# Tests for parsing scripts\n",
        f"{base_path}/{project_name}/Dockerfile": "# Dockerfile for containerization\n",
        f"{base_path}/{project_name}/requirements.txt": "# Python dependencies\n",
        f"{base_path}/{project_name}/README.md": "# Project description and instructions\n"
    }

    # Create the directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create the files
    for file_path, file_content in files.items():
        with open(file_path, 'w') as file:
            file.write(file_content)

# Define the base path (top level of the repo) and project name
base_path = "."  # Current directory
project_name = "component-parser"  # Replace with your actual project name

# Create the project structure
create_project_structure(base_path, project_name)
