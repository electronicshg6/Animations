"""
Helpers for creating TeX templates configured for CircuitikZ.

Circuit diagrams are drawn using CircuitikZ, which is a LaTeX package built
on top of TikZ.  In Manim, Tex templates allow you to add additional
LaTeX packages to the preamble.  The function defined here returns a
TexTemplate configured to import `tikz` and `circuitikz`.
"""

from __future__ import annotations

from manim import TexTemplate


def circuitikz_template() -> TexTemplate:
    """
    Return a TexTemplate preconfigured with CircuitikZ support.

    The returned template includes the necessary packages in the LaTeX
    preamble.  You can further customise the template by adding or removing
    packages or changing the default font.  See the Manim documentation for
    details.
    """
    template = TexTemplate()
    # Add packages needed for circuit drawings.  The [american] option sets the
    # default symbol style to the American standard (rectangular resistors etc.).
    template.add_to_preamble(
        r"\usepackage{tikz}"
        r"\usepackage[american]{circuitikz}"
    )
    return template