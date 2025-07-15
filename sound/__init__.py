"""
Sound Processing Library

A Cython-accelerated library for audio effects, filters, and format handling.
"""

__version__ = "0.1.0"

# Import all submodules
from . import effects
from . import filters  
from . import formats

__all__ = ["effects", "filters", "formats"]
