"""
Reusable animation helper functions.

These small helpers encapsulate common animation patterns—highlighting,
circling, waiting, grouping animations together, etc.  Using them helps keep
your scene code concise and consistent across projects.
"""

from __future__ import annotations

from typing import Iterable

from manim import Animation, AnimationGroup, Circumscribe, Indicate, Wait


def pop(mobj, run_time: float = 0.5) -> Animation:
    """
    Create a simple "pop" animation using Manim's Indicate effect.

    Parameters
    ----------
    mobj :
        The mobject to highlight.
    run_time :
        Duration of the animation in seconds.

    Returns
    -------
    Animation
        An `Indicate` animation that briefly emphasizes the mobject.
    """
    return Indicate(mobj, run_time=run_time)


def ring(mobj, run_time: float = 0.6) -> Animation:
    """
    Draw a ring around the given mobject.

    Parameters
    ----------
    mobj :
        The mobject to circumscribe.
    run_time :
        Duration of the animation in seconds.

    Returns
    -------
    Animation
        A `Circumscribe` animation that outlines the mobject.
    """
    return Circumscribe(mobj, run_time=run_time)


def beat(t: float = 0.2) -> Animation:
    """
    Pause for a beat.

    Returns a `Wait` animation that delays the timeline by the given number
    of seconds.  Using small waits between animations can improve pacing.
    """
    return Wait(t)


def combo(*anims: Iterable[Animation], lag_ratio: float = 0.12) -> Animation:
    """
    Group multiple animations into an `AnimationGroup` with a default lag ratio.

    Parameters
    ----------
    *anims :
        Any number of animations to run in sequence.
    lag_ratio :
        Staggering amount between animations.  A small positive value yields a
        pleasing overlap between consecutive effects.

    Returns
    -------
    Animation
        An `AnimationGroup` that sequences the provided animations.
    """
    return AnimationGroup(*anims, lag_ratio=lag_ratio)