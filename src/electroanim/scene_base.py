"""
Base scene for all electronics animations.

Derive your scenes from `ElectroScene` instead of directly from `Scene`.
This class sets the camera background colour according to the project palette
and allows for further global initialisation in the future.
"""

from __future__ import annotations

from manim import Scene

from .aesthetics import BG


class ElectroScene(Scene):
    """Base scene that sets the default background colour."""

    def setup(self) -> None:
        """Set the camera background colour."""
        self.camera.background_color = BG