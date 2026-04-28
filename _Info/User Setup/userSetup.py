"""
    Add this script to your maya scripts folder and populate with paths
    containing your custom scripts. Helpful for projects containing numerous sub dirs

    manually add sys paths to maya on startup to access user scripts

    add paths to project_paths
    walk the dir of each path adding to sys path if valid
    only adds python directories (contains __init__.py)
    prevents duplicates being added to sys path (can arrive at same dir from different starting points)

    NOTE that output for this file will not fire on startup, reimport this module to see if paths are failing
"""

import sys
import os

project_paths = [
    "C:/Users/rober/Files/Pycharm/Maya Technical Art"
]

def is_python_package(path):
    return os.path.exists(os.path.join(path, '__init__.py'))

# Add all subdirectories to sys.path
for project_path in set(project_paths):
    if not os.path.exists(project_path):
        print(f"WARNING: Path does not exist: {project_path}")
        continue
    for root, dirs, files in os.walk(project_path):
        # Skip .idea and __pycache__ folders
        dirs[:] = [d for d in dirs if d not in ['.idea', '__pycache__']]
        if is_python_package(root) and root not in sys.path:
            # because of maya reload pattern, ensure your paths are first
            sys.path.insert(0, root)