"""
    Add this script to your maya scripts folder and populate with paths
    containing your custom scripts

    manually add sys paths to maya on startup to access user scripts

    add paths to project_paths
    walk the dir of each path adding to sys path if valid
    only adds python directories (contains __init__.py)
    prevents duplicates being added to sys path (can arrive at same dir from different starting points)
"""

import sys
import os

project_paths = [
    r"C:\Users\rober\OneDrive\Documents\maya\2025\scripts\Maya Technical Art"
]

def is_python_package(path):
    return os.path.exists(os.path.join(path, '__init__.py'))

# Add all subdirectories to sys.path
for project_path in set(project_paths):
    for root, dirs, files in os.walk(project_path):
        # Skip .idea and __pycache__ folders
        dirs[:] = [d for d in dirs if d not in ['.idea', '__pycache__']]
        if is_python_package(root) and root not in sys.path:
            sys.path.append(root)