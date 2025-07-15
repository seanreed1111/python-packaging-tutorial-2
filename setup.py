#!/usr/bin/env python
"""Setup script for the sound package with Cython extensions."""

import os
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy

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

# Cythonize the extensions
if extensions:
    extensions = cythonize(
        extensions,
        compiler_directives={
            "boundscheck": False,
            "wraparound": False,
            "nonecheck": False,
            "cdivision": True,
            "language_level": 3,
        },
        annotate=True,  # Generate HTML annotation files
    )

if __name__ == "__main__":
    setup(
        ext_modules=extensions,
        zip_safe=False,
    ) 