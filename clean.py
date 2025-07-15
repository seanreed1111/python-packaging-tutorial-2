#!/usr/bin/env python
"""Clean up generated build files and directories."""

import os
import shutil
import glob


def clean_build_files():
    """Remove all generated build files and directories."""
    
    # Directories to remove
    dirs_to_remove = [
        "build",
        "dist", 
        "sound.egg-info",
        "__pycache__",
    ]
    
    # File patterns to remove
    files_to_remove = [
        "*.c",           # Generated C files
        "*.html",        # Cython annotation files  
        "*.so",          # Compiled shared libraries
        "*.pyd",         # Windows compiled extensions
        "*.pyc",         # Compiled Python files
        "**/__pycache__", # Cache directories
    ]
    
    print("Cleaning up generated files...")
    
    # Remove directories
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"Removing directory: {dir_name}")
            shutil.rmtree(dir_name)
    
    # Remove files by pattern
    for pattern in files_to_remove:
        for filepath in glob.glob(pattern, recursive=True):
            if os.path.isfile(filepath):
                print(f"Removing file: {filepath}")
                os.remove(filepath)
            elif os.path.isdir(filepath):
                print(f"Removing directory: {filepath}")
                shutil.rmtree(filepath)
    
    # Remove any remaining annotation files in sound subdirectories
    for root, dirs, files in os.walk("sound"):
        for file in files:
            if file.endswith(('.c', '.html', '.so', '.pyd')):
                filepath = os.path.join(root, file)
                print(f"Removing: {filepath}")
                os.remove(filepath)
    
    print("Cleanup complete!")


if __name__ == "__main__":
    clean_build_files() 