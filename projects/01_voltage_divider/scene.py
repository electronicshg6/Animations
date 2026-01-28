"""
Scene definition for the voltage divider animation.

This script constructs a short Manim animation illustrating how a simple two‑resistor
voltage divider works.  It uses the reusable helpers defined in the `electroanim`
package to load the circuit diagram, apply consistent styles, and build common
animation effects.
"""

from __future__ import annotations

from manim import (
    VGroup,
    MathTex,
    ValueTracker,
    DecimalNumber,
    always_redraw,
    Axes,
    Line,
    FadeIn,
    FadeOut,
    Create,
    Transform,
    RoundedRectangle,
    config,
    UP,
    RIGHT,
    DOWN,
    LEFT,
    ORIGIN,
)

import numpy as np

from electroanim.scene_base import ElectroScene
from electroanim.circuitikz import circuitikz_from_file
from electroanim.aesthetics import FG, ACCENT_1, ACCENT_2, WARN
from electroanim.helpers import ring, pop


def _format_example(axes, r1_value: float, r2_value: float, vout: float, scale: float):
    example = MathTex(
        r"\text{Example: }",
        r"R_1=%.0fk,\ R_2=%.0fk \Rightarrow V_{out}=%.1f\mathrm{V}"
        % (r1_value / 1000.0, r2_value / 1000.0, vout),
    ).set_color(FG)
    example.scale(scale)
    if example.width > axes.width:
        example.scale_to_fit_width(axes.width)
    example.next_to(axes, DOWN, buff=0.25).align_to(axes, LEFT)
    return example


class VoltageDivider(ElectroScene):
    """Animation illustrating the behaviour of a simple resistor voltage divider."""

    def construct(self) -> None:
        """Build and play the animation."""
        gap = 0.5
        margin = 0.6
        bottom_margin = 0.45
        row_gap = 0.18
        col_gap = 0.3
        section_gap = 0.3
        note_gap = 0.18
        card_pad_x = 0.5
        card_pad_y = 0.4

        title_scale = 0.9
        subtitle_scale = 0.55
        body_scale = 0.55

        # Load the circuit diagram from the TikZ file.
        circuit = circuitikz_from_file(
            "projects/01_voltage_divider/assets/circuit/divider.tikz"
        )
        circuit.set_color(FG).scale(1.0)

        load_circuit = circuitikz_from_file(
            "projects/01_voltage_divider/assets/circuit/divider_load.tikz"
        )
        load_circuit.set_color(FG).scale(1.0).move_to(circuit)

        title = MathTex(r"\text{Voltage Divider}").set_color(FG).scale(title_scale)
        subtitle = (
            MathTex(r"\text{Two resistors set a fraction of }V_{in}")
            .set_color(FG)
            .scale(subtitle_scale)
            .set_opacity(0.7)
        )
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.12)

        eq = (
            MathTex(r"V_{out} = V_{in}\frac{R_2}{R_1 + R_2}")
            .set_color(FG)
            .scale(body_scale)
        )

        vin = ValueTracker(9.0)
        r1 = ValueTracker(10_000.0)
        r2 = ValueTracker(10_000.0)
        rl = ValueTracker(1_000_000.0)

        def r2_effective() -> float:
            r2_val = r2.get_value()
            rl_val = rl.get_value()
            return (r2_val * rl_val) / (r2_val + rl_val)

        def vout_value() -> float:
            r2_eff = r2_effective()
            return vin.get_value() * r2_eff / (r1.get_value() + r2_eff)

        label_vin = MathTex(r"V_{in}").set_color(FG).scale(body_scale)
        label_r1 = MathTex(r"R_1").set_color(FG).scale(body_scale)
        label_r2 = MathTex(r"R_2").set_color(FG).scale(body_scale)
        label_vout = MathTex(r"V_{out}").set_color(FG).scale(body_scale)

        value_vin = DecimalNumber(
            vin.get_value(), num_decimal_places=1, edge_to_fix=LEFT
        ).set_color(ACCENT_2)
        value_r1 = DecimalNumber(
            r1.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT
        ).set_color(ACCENT_1)
        value_r2 = DecimalNumber(
            r2.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT
        ).set_color(ACCENT_1)
        value_vout = DecimalNumber(
            vout_value(), num_decimal_places=2, edge_to_fix=LEFT
        ).set_color(ACCENT_1)

        for value in (value_vin, value_r1, value_r2, value_vout):
            value.scale(body_scale)

        value_vin.add_updater(lambda m: m.set_value(vin.get_value()))
        value_r1.add_updater(lambda m: m.set_value(r1.get_value() / 1000.0))
        value_r2.add_updater(lambda m: m.set_value(r2.get_value() / 1000.0))
        value_vout.add_updater(lambda m: m.set_value(vout_value()))

        unit_v = MathTex(r"\mathrm{V}").set_color(FG).scale(body_scale)
        unit_kohm = MathTex(r"\mathrm{k}\Omega").set_color(FG).scale(body_scale)

        label_col = VGroup(label_vin, label_r1, label_r2, label_vout).arrange(
            DOWN, aligned_edge=LEFT, buff=row_gap
        )
        value_col = VGroup(value_vin, value_r1, value_r2, value_vout).arrange(
            DOWN, aligned_edge=LEFT, buff=row_gap
        )
        unit_col = VGroup(unit_v, unit_kohm, unit_kohm.copy(), unit_v.copy()).arrange(
            DOWN, aligned_edge=LEFT, buff=row_gap
        )

        value_col.next_to(label_col, RIGHT, buff=col_gap, aligned_edge=UP)
        unit_col.next_to(value_col, RIGHT, buff=col_gap, aligned_edge=UP)

        for value, label, unit in zip(value_col, label_col, unit_col):
            value.align_to(label, DOWN)
            unit.align_to(label, DOWN)

        info_table = VGroup(label_col, value_col, unit_col)

        load_label = MathTex(r"R_L").set_color(FG).scale(body_scale)
        load_value = DecimalNumber(
            rl.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT
        ).set_color(WARN)
        load_value.scale(body_scale)
        load_value.add_updater(lambda m: m.set_value(rl.get_value() / 1000.0))
        load_unit = MathTex(r"\mathrm{k}\Omega").set_color(FG).scale(body_scale)
        load_line = VGroup(load_label, load_value, load_unit).arrange(
            RIGHT, buff=col_gap
        )

        load_note = (
            MathTex(r"\text{Heavier load lowers }V_{out}\text{ (}R_2 \parallel R_L\text{)}")
            .set_color(WARN)
            .scale(subtitle_scale)
        )

        reg_note = (
            MathTex(r"\text{Not a regulator: }V_{out}\text{ follows }V_{in}")
            .set_color(WARN)
            .scale(subtitle_scale)
        )

        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-15, 15, 5],
            x_length=7.0,
            y_length=4.1,
            axis_config={"color": FG},
            tips=False,
        )
        y_label = MathTex(r"V\ (\mathrm{V})").set_color(FG).scale(subtitle_scale)
        y_label.move_to(axes.c2p(0.05, 14))

        legend_in = VGroup(
            Line(ORIGIN, RIGHT * 0.6).set_color(ACCENT_2),
            MathTex(r"V_{in}").set_color(FG).scale(body_scale),
        ).arrange(RIGHT, buff=0.1)
        legend_out = VGroup(
            Line(ORIGIN, RIGHT * 0.6).set_color(ACCENT_1),
            MathTex(r"V_{out}").set_color(FG).scale(body_scale),
        ).arrange(RIGHT, buff=0.1)
        legend = VGroup(legend_in, legend_out).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.next_to(axes, UP, buff=0.15).align_to(axes, RIGHT)

        example_placeholder = _format_example(
            axes,
            r1.get_value(),
            r2.get_value(),
            vout_value(),
            body_scale,
        )
        example_placeholder.set_opacity(0)
        note_stack = VGroup(load_line, load_note, reg_note).arrange(
            DOWN, aligned_edge=LEFT, buff=note_gap
        )

        mid_stack = VGroup(eq, info_table, note_stack).arrange(
            DOWN, aligned_edge=LEFT, buff=section_gap
        )
        mid_content = VGroup(title_group, mid_stack).arrange(
            DOWN, aligned_edge=LEFT, buff=section_gap
        )
        title_group.set_x(mid_stack.get_x())

        mid_card = RoundedRectangle(corner_radius=0.2)
        mid_card.set_fill(FG, opacity=0.08).set_stroke(width=0)

        right_panel = VGroup(axes, y_label, legend, example_placeholder)
        top_row = VGroup(circuit, right_panel).arrange(
            RIGHT, buff=gap, aligned_edge=UP
        )

        mid_card.set_width(max(mid_content.width + card_pad_x, top_row.width))
        mid_card.set_height(mid_content.height + card_pad_y)
        mid_card.move_to(mid_content).set_z_index(-1)
        mid_panel = VGroup(mid_card, mid_content)

        layout = VGroup(top_row, mid_panel).arrange(
            DOWN, buff=gap, aligned_edge=LEFT
        )
        layout_scale = min(
            (config.frame_width - 2 * margin) / layout.width,
            (config.frame_height - 2 * margin) / layout.height,
            1.0,
        )
        layout.scale(layout_scale)
        layout.move_to(ORIGIN)
        layout.to_edge(DOWN, buff=bottom_margin)
        load_circuit.scale(layout_scale)
        load_circuit.move_to(circuit)

        example = always_redraw(
            lambda: _format_example(
                axes,
                r1.get_value(),
                r2.get_value(),
                vout_value(),
                body_scale * layout_scale,
            )
        )
        input_wave = always_redraw(
            lambda: axes.plot(
                lambda x: vin.get_value() * np.sin(2 * np.pi * 2 * x),
                x_range=[0, 1],
                color=ACCENT_2,
            )
        )
        output_wave = always_redraw(
            lambda: axes.plot(
                lambda x: vout_value() * np.sin(2 * np.pi * 2 * x),
                x_range=[0, 1],
                color=ACCENT_1,
            )
        )

        self.play(FadeIn(circuit), FadeIn(mid_card), FadeIn(title_group), run_time=1.2)
        self.play(FadeIn(eq), run_time=0.8)
        self.play(ring(circuit), run_time=0.6)
        self.play(pop(eq), run_time=0.6)
        self.wait(0.8)

        self.play(FadeIn(info_table), run_time=0.8)
        self.play(Create(axes), run_time=1.0)
        self.play(FadeIn(y_label), run_time=0.4)
        self.play(Create(input_wave), Create(output_wave), run_time=1.5)
        self.play(FadeIn(legend), run_time=0.5)
        self.play(FadeIn(example), run_time=0.8)
        self.wait(0.8)

        self.play(r2.animate.set_value(20_000.0), run_time=4.0)
        self.wait(1.2)
        self.play(r2.animate.set_value(5_000.0), run_time=4.0)
        self.wait(1.2)
        self.play(r1.animate.set_value(20_000.0), run_time=3.5)
        self.wait(1.2)

        self.play(FadeOut(example), run_time=0.6)
        self.play(
            Transform(circuit, load_circuit),
            FadeIn(load_line),
            FadeIn(load_note),
            run_time=1.2,
        )
        self.wait(1.0)

        self.play(rl.animate.set_value(2_000.0), run_time=5.0)
        self.wait(1.0)
        self.play(rl.animate.set_value(20_000.0), run_time=4.0)
        self.wait(1.4)

        self.play(FadeOut(load_note), FadeIn(reg_note), run_time=0.8)
        self.play(vin.animate.set_value(12.0), run_time=2.5)
        self.wait(0.4)
        self.play(vin.animate.set_value(7.0), run_time=2.5)
        self.wait(1.2)
