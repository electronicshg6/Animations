"""
Shared aesthetic constants for electronics animations.

Define colours, backgrounds, and drawing parameters in one place so that all
scenes maintain a consistent look and feel.  Colours are specified using
hexadecimal notation compatible with Manim's `ManimColor` class.
"""

from __future__ import annotations

from manim import ManimColor

# Background and foreground colours
BG = ManimColor("#0B0F1A")  # Dark navy background
FG = ManimColor("#E6EAF2")  # Light foreground for text and strokes

# Accent colours for highlights
ACCENT_1 = ManimColor("#6EE7FF")   # Cyan accent
ACCENT_2 = ManimColor("#A78BFA")   # Purple accent

# Warning colour (e.g. to highlight "gotchas")
WARN = ManimColor("#FBBF24")       # Amber/yellow

# Default stroke width for circuit drawings
STROKE_W = 3