"""ElectroAnim package.

This package contains reusable helpers for building electronics animations
using Manim and CircuitikZ.  See the individual modules for details.
"""

from .aesthetics import BG, FG, ACCENT_1, ACCENT_2, WARN, STROKE_W
from .tex import circuitikz_template
from .circuitikz import circuitikz_from_file
from .helpers import pop, ring, beat, combo
from .scene_base import ElectroScene

__all__ = [
    "BG",
    "FG",
    "ACCENT_1",
    "ACCENT_2",
    "WARN",
    "STROKE_W",
    "circuitikz_template",
    "circuitikz_from_file",
    "pop",
    "ring",
    "beat",
    "combo",
    "ElectroScene",
]