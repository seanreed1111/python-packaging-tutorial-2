#!/usr/bin/env python
"""Setup script for the sound package with Cython extensions."""

import os
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy

# Define build directories for generated files
BUILD_DIR = "build"
CYTHON_BUILD_DIR = os.path.join(BUILD_DIR, "cython")
ANNOTATION_DIR = os.path.join(BUILD_DIR, "annotations")

# Create build directories if they don't exist
os.makedirs(CYTHON_BUILD_DIR, exist_ok=True)
os.makedirs(ANNOTATION_DIR, exist_ok=True)

# Define which modules should be compiled as Cython extensions
cython_modules = [
    "sound.effects.echo",
    "sound.effects.reverse", 
    "sound.effects.surround",
    "sound.filters.karaoke",
    "sound.filters.synth",
    "sound.filters.vocoder",
    "sound.formats.waveread",
    "sound.formats.wavewrite",
]

# Create Extension objects for each Cython module
extensions = []
for module_name in cython_modules:
    # Convert module name to file path
    pyx_file = module_name.replace(".", "/") + ".py"
    if os.path.exists(pyx_file):
        extensions.append(
            Extension(
                module_name,
                [pyx_file],
                include_dirs=[numpy.get_include()],
                extra_compile_args=["-O3", "-ffast-math"],
                extra_link_args=["-O3"],
            )
        )

# Cythonize the extensions with organized output directories
if extensions:
    extensions = cythonize(
        extensions,
        build_dir=CYTHON_BUILD_DIR,  # Put generated C files here
        compiler_directives={
            "boundscheck": False,
            "wraparound": False,
            "nonecheck": False,
            "cdivision": True,
            "language_level": 3,
        },
        annotate=True,  # Generate HTML annotation files
        annotate_coverage_xml=os.path.join(ANNOTATION_DIR, "coverage.xml"),
    )
    
    # Move annotation files to the annotations directory
    import shutil
    import glob
    
    # Find and move .html annotation files
    for html_file in glob.glob("*.html"):
        if any(module.replace(".", "_") in html_file for module in cython_modules):
            dest_path = os.path.join(ANNOTATION_DIR, html_file)
            shutil.move(html_file, dest_path)
            print(f"Moved annotation file: {html_file} -> {dest_path}")

if __name__ == "__main__":
    setup(
        ext_modules=extensions,
        zip_safe=False,
    ) 