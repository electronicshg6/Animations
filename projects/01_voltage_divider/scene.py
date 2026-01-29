"""
Voltage divider scene (layout v2):
- Fixes Vout label occlusion by using output stubs in TikZ (see divider*.tikz).
- Makes the bottom information card large and readable (YouTube/phone-friendly).
- Spreads content horizontally across the card (title+equation | table | notes).
"""

from __future__ import annotations

from manim import (
    Axes,
    Create,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    Transform,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    VGroup,
    ValueTracker,
    always_redraw,
    config,
)

import numpy as np

from electroanim.aesthetics import ACCENT_1, ACCENT_2, FG, WARN
from electroanim.circuitikz import circuitikz_from_file
from electroanim.helpers import pop, ring
from electroanim.scene_base import ElectroScene


def _scale_to_fit(mobj, max_w: float, max_h: float):
    """Uniformly scale mobj to fit inside (max_w, max_h)."""
    if mobj.width == 0 or mobj.height == 0:
        return mobj
    s = min(max_w / mobj.width, max_h / mobj.height)
    mobj.scale(s)
    return mobj


def _format_example(axes: Axes, r1_value: float, r2_value: float, vout: float, scale: float):
    example = MathTex(
        r"\text{Example: }",
        r"R_1=%.0fk,\ R_2=%.0fk \Rightarrow V_{out}=%.1f\mathrm{V}"
        % (r1_value / 1000.0, r2_value / 1000.0, vout),
    ).set_color(FG)
    example.scale(scale)
    if example.width > axes.width:
        example.scale_to_fit_width(axes.width)
    return example


class VoltageDivider(ElectroScene):
    def construct(self) -> None:
        # -------------------------
        # Global layout parameters
        # -------------------------
        margin = 0.45
        gap_x = 0.70
        gap_y = 0.30
        inner_pad_x = 0.28
        inner_pad_y = 0.20

        # Give the bottom card *more* real estate.
        top_h = config.frame_height * 0.50
        bot_h = config.frame_height - top_h - (2 * margin) - gap_y

        top_rect = Rectangle(
            width=config.frame_width - 2 * margin,
            height=top_h,
        ).to_edge(UP, buff=margin)

        bot_rect = Rectangle(
            width=top_rect.width,
            height=bot_h,
        ).to_edge(DOWN, buff=margin)

        left_w = top_rect.width * 0.33
        right_w = top_rect.width - left_w - gap_x

        # -------------------------
        # Circuit diagrams (TikZ)
        # -------------------------
        circuit = circuitikz_from_file("projects/01_voltage_divider/assets/circuit/divider.tikz")
        circuit.set_color(FG)

        load_circuit = circuitikz_from_file("projects/01_voltage_divider/assets/circuit/divider_load.tikz")
        load_circuit.set_color(FG)

        # Fit circuit to left area
        _scale_to_fit(circuit, left_w - 2 * inner_pad_x, top_rect.height - 2 * inner_pad_y)
        circuit.align_to(top_rect, LEFT).shift(RIGHT * inner_pad_x)
        circuit.align_to(top_rect, UP).shift(DOWN * inner_pad_y)

        # Match load circuit scale + position to base circuit
        load_circuit.scale(circuit.width / load_circuit.width)
        load_circuit.move_to(circuit)

        # -------------------------
        # Plot (right side)
        # -------------------------
        axes_h = top_rect.height * 0.78
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-15, 15, 5],
            x_length=right_w - 2 * inner_pad_x,
            y_length=axes_h - inner_pad_y,
            axis_config={"color": FG},
            tips=False,
        )
        axes.align_to(top_rect, RIGHT).shift(LEFT * inner_pad_x)
        axes.align_to(top_rect, UP).shift(DOWN * inner_pad_y)

        # Small y-unit label inside plot area (can't collide with circuit/card)
        y_label = MathTex(r"V\ (\mathrm{V})").set_color(FG).scale(0.52)
        y_label.move_to(axes.c2p(0.10, 13.5))

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

        legend_in = VGroup(
            Line(ORIGIN, RIGHT * 0.55).set_color(ACCENT_2),
            MathTex(r"V_{in}").set_color(FG).scale(0.55),
        ).arrange(RIGHT, buff=0.12)
        legend_out = VGroup(
            Line(ORIGIN, RIGHT * 0.55).set_color(ACCENT_1),
            MathTex(r"V_{out}").set_color(FG).scale(0.55),
        ).arrange(RIGHT, buff=0.12)
        legend = VGroup(legend_in, legend_out).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        legend.move_to(axes.get_corner(UP + RIGHT) + LEFT * 0.95 + DOWN * 0.35)

        example = always_redraw(
            lambda: _format_example(
                axes,
                r1.get_value(),
                r2.get_value(),
                vout_value(),
                scale=0.62,
            )
            .next_to(axes, DOWN, buff=0.18)
            .align_to(axes, LEFT)
        )

        # -------------------------
        # Bottom info card (bigger, horizontally spread)
        # -------------------------
        title = MathTex(r"\text{Voltage Divider}").set_color(FG).scale(1.05)
        subtitle = (
            MathTex(r"\text{Two resistors set a fraction of }V_{in}")
            .set_color(FG)
            .scale(0.70)
            .set_opacity(0.72)
        )
        title_group = VGroup(title, subtitle).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        eq = MathTex(r"V_{out} = V_{in}\frac{R_2}{R_1 + R_2}").set_color(FG).scale(0.78)

        # Table: larger and stable (no jitter)
        body_scale = 0.74
        row_gap = 0.20
        col_gap = 0.32

        label_vin = MathTex(r"V_{in}").set_color(FG).scale(body_scale)
        label_r1 = MathTex(r"R_1").set_color(FG).scale(body_scale)
        label_r2 = MathTex(r"R_2").set_color(FG).scale(body_scale)
        label_vout = MathTex(r"V_{out}").set_color(FG).scale(body_scale)

        value_vin = DecimalNumber(vin.get_value(), num_decimal_places=1, edge_to_fix=LEFT).set_color(ACCENT_2).scale(body_scale)
        value_r1 = DecimalNumber(r1.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT).set_color(ACCENT_1).scale(body_scale)
        value_r2 = DecimalNumber(r2.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT).set_color(ACCENT_1).scale(body_scale)
        value_vout = DecimalNumber(vout_value(), num_decimal_places=2, edge_to_fix=LEFT).set_color(ACCENT_1).scale(body_scale)

        value_vin.add_updater(lambda m: m.set_value(vin.get_value()))
        value_r1.add_updater(lambda m: m.set_value(r1.get_value() / 1000.0))
        value_r2.add_updater(lambda m: m.set_value(r2.get_value() / 1000.0))
        value_vout.add_updater(lambda m: m.set_value(vout_value()))

        unit_v = MathTex(r"\mathrm{V}").set_color(FG).scale(body_scale)
        unit_kohm = MathTex(r"\mathrm{k}\Omega").set_color(FG).scale(body_scale)

        label_col = VGroup(label_vin, label_r1, label_r2, label_vout).arrange(DOWN, aligned_edge=LEFT, buff=row_gap)
        value_col = VGroup(value_vin, value_r1, value_r2, value_vout).arrange(DOWN, aligned_edge=LEFT, buff=row_gap)
        unit_col = VGroup(unit_v, unit_kohm, unit_kohm.copy(), unit_v.copy()).arrange(DOWN, aligned_edge=LEFT, buff=row_gap)

        value_col.next_to(label_col, RIGHT, buff=col_gap, aligned_edge=UP)
        unit_col.next_to(value_col, RIGHT, buff=col_gap, aligned_edge=UP)

        for vv, ll, uu in zip(value_col, label_col, unit_col):
            vv.align_to(ll, DOWN)
            uu.align_to(ll, DOWN)

        info_table = VGroup(label_col, value_col, unit_col)

        # Load row + notes
        load_label = MathTex(r"R_L").set_color(FG).scale(body_scale)
        load_value = DecimalNumber(rl.get_value() / 1000.0, num_decimal_places=1, edge_to_fix=LEFT).set_color(WARN).scale(body_scale)
        load_value.add_updater(lambda m: m.set_value(rl.get_value() / 1000.0))
        load_unit = MathTex(r"\mathrm{k}\Omega").set_color(FG).scale(body_scale)
        load_line = VGroup(load_label, load_value, load_unit).arrange(RIGHT, buff=col_gap)

        load_note = MathTex(r"\text{Heavier load lowers }V_{out}\text{ (}R_2 \parallel R_L\text{)}").set_color(WARN).scale(0.66)
        reg_note = MathTex(r"\text{Not a regulator: }V_{out}\text{ follows }V_{in}").set_color(WARN).scale(0.66)

        # Start hidden, fade in later
        load_line.set_opacity(0)
        load_note.set_opacity(0)
        reg_note.set_opacity(0)

        left_block = VGroup(title_group, eq).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        table_block = VGroup(info_table, load_line).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        notes_block = VGroup(load_note, reg_note).arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        card_content = VGroup(left_block, table_block, notes_block).arrange(
            RIGHT, aligned_edge=UP, buff=1.10
        )

        # Card background
        card = RoundedRectangle(corner_radius=0.22, width=bot_rect.width, height=bot_rect.height)
        card.set_fill(FG, opacity=0.08).set_stroke(FG, opacity=0.12, width=1)

        # Fit content inside card, then gently scale UP if we have room (so it doesn't look tiny)
        target_w = card.width - 0.95
        target_h = card.height - 0.55
        _scale_to_fit(card_content, target_w, target_h)

        # Scale up (bounded) to use space if there's extra room
        if card_content.width < 0.82 * target_w and card_content.height < 0.82 * target_h:
            s_up = min(target_w / card_content.width, target_h / card_content.height, 1.28)
            if s_up > 1.0:
                card_content.scale(s_up)

        card_content.move_to(card.get_center())
        bottom_panel = VGroup(card, card_content).move_to(bot_rect.get_center())

        # -------------------------
        # Animation sequence
        # -------------------------
        self.play(FadeIn(circuit), Create(axes), FadeIn(bottom_panel), run_time=1.2)
        self.play(FadeIn(y_label), run_time=0.4)

        self.play(ring(circuit), run_time=0.6)
        self.play(pop(eq), run_time=0.6)
        self.wait(0.4)

        self.play(Create(input_wave), Create(output_wave), run_time=1.2)
        self.play(FadeIn(legend), run_time=0.5)
        self.play(FadeIn(example), run_time=0.7)
        self.wait(0.6)

        self.play(r2.animate.set_value(20_000.0), run_time=3.2)
        self.wait(0.4)
        self.play(r2.animate.set_value(5_000.0), run_time=3.2)
        self.wait(0.4)
        self.play(r1.animate.set_value(20_000.0), run_time=2.8)
        self.wait(0.4)

        self.play(
            Transform(circuit, load_circuit),
            load_line.animate.set_opacity(1),
            load_note.animate.set_opacity(1),
            run_time=1.2,
        )
        self.wait(0.3)

        self.play(rl.animate.set_value(2_000.0), run_time=3.6)
        self.wait(0.2)
        self.play(rl.animate.set_value(20_000.0), run_time=2.8)
        self.wait(0.5)

        self.play(load_note.animate.set_opacity(0), reg_note.animate.set_opacity(1), run_time=0.8)
        self.play(vin.animate.set_value(12.0), run_time=2.0)
        self.play(vin.animate.set_value(7.0), run_time=2.0)
        self.wait(0.8)
