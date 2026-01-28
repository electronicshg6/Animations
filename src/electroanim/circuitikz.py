r"""
Utilities for loading CircuitikZ diagrams into Manim.

This module exposes a helper function that reads a `.tikz` file containing
CircuitikZ `\\draw` commands and returns a Manim `Tex` object.  The object is
constructed using a custom template that imports the `circuitikz` package and
draws within the `circuitikz` environment.  By default the resulting
diagram has no fill and uses the global stroke width defined in
``src/electroanim/aesthetics.py``.

Usage:

    from electroanim.circuitikz import circuitikz_from_file
    circuit = circuitikz_from_file("path/to/diagram.tikz")
    circuit.set_color(FG)
    scene.add(circuit)

Alternatively, if you wish to precompile your CircuitikZ diagrams into SVG
files, you can call `\usepackage[convert]{circuitikz}` in a LaTeX document
and compile it using `dvisvgm`.  Then load the resulting SVG with
``SVGMobject`` instead.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

from manim import Tex

from .aesthetics import STROKE_W
from .tex import circuitikz_template


def circuitikz_from_file(tikz_path: Union[str, Path]) -> Tex:
    """
    Load a CircuitikZ diagram from a `.tikz` file and return a `Tex` mobject.

    Parameters
    ----------
    tikz_path:
        Path to the `.tikz` file containing only the `\\draw` commands for the
        circuit.  The file should not include `\\begin{circuitikz}` or
        `\\end{circuitikz}`; those are added automatically.

    Returns
    -------
    Tex
        A Manim `Tex` object representing the rendered circuit.  The diagram is
        created within a `circuitikz` environment and uses a template that
        imports the `circuitikz` package.  The `stroke_width` and
        `fill_opacity` are set to sensible defaults for line drawings.
    """
    path = Path(tikz_path)
    code = path.read_text(encoding="utf-8")

    return Tex(
        code,
        tex_environment="circuitikz",
        tex_template=circuitikz_template(),
        stroke_width=STROKE_W,
        # We disable fill so that the interior of components is transparent.
        fill_opacity=0,
        stroke_opacity=1,
    )