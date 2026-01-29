"""
Voltage divider scene (layout v2):
- Fixes Vout label occlusion by using output stubs in TikZ (see divider*.tikz).
- Makes the bottom information card large and readable (YouTube/phone-friendly).
- Spreads content horizontally across the card (title+equation | table | notes).
"""

from __future__ import annotations

from manim import (
    Axes,
    Circle,
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


def fit_to_rect(mobj, rect, pad_x: float = 0.15, pad_y: float = 0.15):
    """Scale *mobj* to fit inside *rect* with padding, then centre it."""
    avail_w = rect.width - 2 * pad_x
    avail_h = rect.height - 2 * pad_y
    _scale_to_fit(mobj, avail_w, avail_h)
    mobj.move_to(rect.get_center())
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

        # Match load circuit scale + position to base circuit, then scale up 81%
        # (load circuit is wider due to RL, so needs extra scaling to match visual size)
        # Shift right so Vin label stays on screen
        load_circuit.scale(circuit.width / load_circuit.width * 1.81)
        load_circuit.move_to(circuit).shift(RIGHT * 0.45)

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

        # === SECTION 1: Introduction - Voltage divider and equation (~15s) ===
        self.play(FadeIn(circuit), run_time=2.0)
        self.wait(1.0)
        self.play(Create(axes), FadeIn(bottom_panel), run_time=2.5)
        self.play(FadeIn(y_label), run_time=0.8)
        self.wait(1.5)

        self.play(ring(circuit), run_time=1.2)
        self.wait(0.8)
        self.play(pop(eq), run_time=1.0)
        self.wait(2.0)

        self.play(Create(input_wave), Create(output_wave), run_time=2.5)
        self.wait(1.0)
        self.play(FadeIn(legend), run_time=1.0)
        self.play(FadeIn(example), run_time=1.2)
        self.wait(2.5)

        # === SECTION 2: Changing R values with dynamic voltage plot (~20s) ===
        self.play(r2.animate.set_value(20_000.0), run_time=5.0)
        self.wait(1.5)
        self.play(r2.animate.set_value(5_000.0), run_time=5.0)
        self.wait(1.5)
        self.play(r1.animate.set_value(20_000.0), run_time=5.0)
        self.wait(2.0)

        # === SECTION 3: Load resistor section (~20s) ===
        self.play(
            Transform(circuit, load_circuit),
            load_line.animate.set_opacity(1),
            load_note.animate.set_opacity(1),
            run_time=2.5,
        )
        self.wait(2.0)

        self.play(rl.animate.set_value(2_000.0), run_time=6.0)
        self.wait(1.5)
        self.play(rl.animate.set_value(20_000.0), run_time=5.0)
        self.wait(2.0)

        self.play(load_note.animate.set_opacity(0), reg_note.animate.set_opacity(1), run_time=1.5)
        self.wait(1.0)
        self.play(vin.animate.set_value(12.0), run_time=4.0)
        self.wait(1.0)
        self.play(vin.animate.set_value(7.0), run_time=4.0)
        self.wait(2.0)


class DividerVsRegulatorScene(ElectroScene):
    """
    Split-screen comparison: voltage divider (unregulated) vs regulator (regulated).
    Uses real CircuitikZ diagrams for both halves.
    2-row × 2-column grid: left = circuits, right = VDD plot.
    """

    def construct(self) -> None:
        # =========================================================
        # §1  Electrical model (fixed teaching values)
        # =========================================================
        V_IN = 5.0
        R1 = 91.0
        R2 = 180.0
        V_TH = V_IN * R2 / (R1 + R2)          # ≈ 3.321 V
        R_TH = (R1 * R2) / (R1 + R2)           # ≈ 60.4 Ω
        I_BASE = 0.0012                         # 1.2 mA
        V_F = 2.0
        R_LED = 680.0
        V_BOR = 3.0
        V_REG = 3.30

        def calc_vdd_div(n: int) -> float:
            if n == 0:
                return V_TH - R_TH * I_BASE
            num = V_TH - R_TH * I_BASE + n * R_TH * V_F / R_LED
            den = 1 + n * R_TH / R_LED
            return num / den

        # Pre-compute for sanity (N=0→3.249, N=1→3.147, N=2→3.060, N=3→2.986)
        vdd_pts = [calc_vdd_div(i) for i in range(4)]

        # =========================================================
        # §2  Strict grid layout  (2 rows × 2 cols)
        #
        #  ┌─────────────────────┬───────────────┐
        #  │ TITLE TOP           │               │
        #  │ [circuit: divider]  │               │
        #  │ VDD readout         │   VDD plot    │
        #  ├─────────────────────┤  (spans both  │
        #  │ TITLE BOT           │   rows)       │
        #  │ [circuit: regulator]│               │
        #  │ VDD readout         │               │
        #  ├─────────────────────┤               │
        #  │ [callouts strip]    │               │
        #  └─────────────────────┴───────────────┘
        # =========================================================
        margin = 0.25
        gap_x = 0.25
        gap_y = 0.12
        title_h = 0.40
        callout_h = 1.05          # dedicated strip below bottom circuit

        frame_w = config.frame_width - 2 * margin
        frame_h = config.frame_height - 2 * margin

        left_col_w = frame_w * 0.58
        right_col_w = frame_w - left_col_w - gap_x

        # Rows: 2 titles + 2 circuit rows + gap + callout strip
        circuit_row_h = (frame_h - 2 * title_h - gap_y - callout_h) / 2

        # Anchor: top-left of usable area
        grid_left = -config.frame_width / 2 + margin
        grid_top = config.frame_height / 2 - margin

        # Y coordinates (top-down)
        top_title_cy = grid_top - title_h / 2
        top_circ_cy = grid_top - title_h - circuit_row_h / 2
        sep_y = grid_top - title_h - circuit_row_h - gap_y / 2
        bot_title_cy = grid_top - title_h - circuit_row_h - gap_y - title_h / 2
        bot_circ_cy = grid_top - title_h - circuit_row_h - gap_y - title_h - circuit_row_h / 2
        callout_cy = grid_top - 2 * title_h - 2 * circuit_row_h - gap_y - callout_h / 2

        # X centres
        lc_cx = grid_left + left_col_w / 2
        rc_cx = grid_left + left_col_w + gap_x + right_col_w / 2

        # Build invisible bounding rectangles for placement
        top_circ_rect = Rectangle(width=left_col_w, height=circuit_row_h)
        top_circ_rect.move_to([lc_cx, top_circ_cy, 0])

        bot_circ_rect = Rectangle(width=left_col_w, height=circuit_row_h)
        bot_circ_rect.move_to([lc_cx, bot_circ_cy, 0])

        callout_rect = Rectangle(width=left_col_w, height=callout_h)
        callout_rect.move_to([lc_cx, callout_cy, 0])

        plot_rect = Rectangle(
            width=right_col_w,
            height=2 * circuit_row_h + 2 * title_h + gap_y + callout_h,
        )
        plot_rect.move_to([rc_cx, (grid_top + grid_top - frame_h) / 2, 0])

        # =========================================================
        # §3  Section labels (in title rows – never over circuits)
        # =========================================================
        top_label = MathTex(r"\text{UNREGULATED (Divider)}").set_color(WARN).scale(0.60)
        top_label.move_to([lc_cx, top_title_cy, 0])

        bot_label = MathTex(r"\text{REGULATED (3.3\,V Regulator)}").set_color(ACCENT_1).scale(0.60)
        bot_label.move_to([lc_cx, bot_title_cy, 0])

        separator = Line(
            start=[grid_left, sep_y, 0],
            end=[grid_left + left_col_w, sep_y, 0],
        ).set_color(FG).set_opacity(0.25)

        # =========================================================
        # §4  CircuitikZ diagrams (left column, fitted to rects)
        # =========================================================
        circ_top = circuitikz_from_file(
            "projects/01_voltage_divider/assets/circuit/divider_mcu_leds.tikz"
        )
        circ_top.set_color(FG)
        fit_to_rect(circ_top, top_circ_rect, pad_x=0.10, pad_y=0.10)

        circ_bot = circuitikz_from_file(
            "projects/01_voltage_divider/assets/circuit/reg_mcu_leds.tikz"
        )
        circ_bot.set_color(FG)
        fit_to_rect(circ_bot, bot_circ_rect, pad_x=0.10, pad_y=0.10)

        # =========================================================
        # §5  Value trackers
        # =========================================================
        n_leds = ValueTracker(0)

        def get_n() -> int:
            return int(round(n_leds.get_value()))

        def vdd_top_val() -> float:
            return calc_vdd_div(get_n())

        # =========================================================
        # §6  VDD readouts (anchored in title rows, right-aligned)
        # =========================================================
        vdd_ro_top_pos = [grid_left + left_col_w - 0.10, top_title_cy, 0]
        vdd_ro_bot_pos = [grid_left + left_col_w - 0.10, bot_title_cy, 0]

        vdd_readout_top = always_redraw(
            lambda: MathTex(
                r"V_{DD}\!=\!%.2f\,\text{V}" % vdd_top_val()
            ).set_color(
                WARN if vdd_top_val() < V_BOR else ACCENT_1
            ).scale(0.55).move_to(vdd_ro_top_pos).align_to(
                [vdd_ro_top_pos[0], 0, 0], RIGHT
            )
        )

        vdd_readout_bot = (
            MathTex(r"V_{DD}\!=\!3.30\,\text{V}")
            .set_color(ACCENT_1).scale(0.55)
            .move_to(vdd_ro_bot_pos)
        )
        vdd_readout_bot.align_to([vdd_ro_bot_pos[0], 0, 0], RIGHT)

        # =========================================================
        # §7  Callout strip (Thévenin card + Power waste meter)
        #     Positioned inside callout_rect – below both circuits
        # =========================================================
        thevenin_card_bg = RoundedRectangle(
            corner_radius=0.08, width=2.80, height=0.88,
        ).set_fill(FG, opacity=0.06).set_stroke(WARN, width=1.2)

        thevenin_title = MathTex(r"\text{Thévenin Model}").set_color(WARN).scale(0.42)
        thevenin_vth = MathTex(
            r"V_{th} = V_{in}\frac{R_2}{R_1+R_2} \approx 3.32\,\text{V}"
        ).set_color(FG).scale(0.35)
        thevenin_rth = MathTex(
            r"R_{th} = R_1 \parallel R_2 \approx 60.4\,\Omega"
        ).set_color(WARN).scale(0.35)

        thevenin_content = VGroup(thevenin_title, thevenin_vth, thevenin_rth).arrange(
            DOWN, buff=0.07, aligned_edge=LEFT
        )
        thevenin_content.move_to(thevenin_card_bg.get_center())
        thevenin_card = VGroup(thevenin_card_bg, thevenin_content)

        power_bg = RoundedRectangle(
            corner_radius=0.06, width=2.00, height=0.88,
        ).set_fill(WARN, opacity=0.08).set_stroke(WARN, width=1)

        power_title = MathTex(r"\text{Divider Waste}").set_color(WARN).scale(0.38)
        power_i = MathTex(r"I_{div} \approx 18.5\,\text{mA}").set_color(WARN).scale(0.34)
        power_p = MathTex(r"P_{div} \approx 92\,\text{mW}").set_color(WARN).scale(0.34)

        power_content = VGroup(power_title, power_i, power_p).arrange(
            DOWN, buff=0.05, aligned_edge=LEFT
        )
        power_content.move_to(power_bg.get_center())
        power_meter = VGroup(power_bg, power_content)

        callout_group = VGroup(thevenin_card, power_meter).arrange(RIGHT, buff=0.20)
        fit_to_rect(callout_group, callout_rect, pad_x=0.10, pad_y=0.06)

        # =========================================================
        # §8  VDD plot (right column, full height)
        # =========================================================
        plot_pad = 0.35
        plot_w = plot_rect.width - 2 * plot_pad
        plot_h = plot_rect.height - 2 * plot_pad - 0.30  # room for labels

        axes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[2.85, 3.45, 0.1],
            x_length=plot_w,
            y_length=plot_h,
            axis_config={"color": FG, "include_numbers": False},
            tips=False,
        )
        axes.move_to(plot_rect.get_center() + UP * 0.10)

        x_label = MathTex(r"\text{LEDs on}").set_color(FG).scale(0.40)
        x_label.next_to(axes, DOWN, buff=0.12)
        y_label = MathTex(r"V_{DD}\;(\text{V})").set_color(FG).scale(0.38)
        y_label.next_to(axes, LEFT, buff=0.08)

        # Tick labels
        x_ticks = VGroup()
        for i in range(4):
            t = MathTex(str(i)).set_color(FG).scale(0.34)
            t.next_to(axes.c2p(i, 2.85), DOWN, buff=0.10)
            x_ticks.add(t)

        y_ticks = VGroup()
        for v in [2.9, 3.0, 3.1, 3.2, 3.3, 3.4]:
            t = MathTex("%.1f" % v).set_color(FG).scale(0.28)
            t.next_to(axes.c2p(0, v), LEFT, buff=0.10)
            y_ticks.add(t)

        # Brown-out threshold line
        bor_line = axes.plot(lambda x: V_BOR, x_range=[0, 3.5], color=WARN)
        bor_line.set_stroke(width=2, opacity=0.6)
        bor_label = MathTex(r"V_{BOR}\!=\!3.0\text{V}").set_color(WARN).scale(0.30)
        bor_label.next_to(axes.c2p(3.5, V_BOR), RIGHT, buff=0.06)

        # Regulator flat line
        reg_line = axes.plot(lambda x: V_REG, x_range=[0, 3.5], color=ACCENT_1)
        reg_line.set_stroke(width=2.5, opacity=0.6)

        # ---- Divider staircase trace (always_redraw) ----
        def make_div_trace():
            n = get_n()
            grp = VGroup()
            # Draw horizontal shelves and vertical drops
            for i in range(n + 1):
                v = vdd_pts[i]
                clr = ACCENT_2 if v >= V_BOR else WARN
                # Horizontal shelf from i to i+1 (or i to i for last step)
                x_end = i + 1 if i < n else i + 0.4
                hseg = Line(
                    axes.c2p(i, v), axes.c2p(min(x_end, 3.5), v),
                    color=clr, stroke_width=3,
                )
                grp.add(hseg)
                # Vertical drop to next step
                if i < n:
                    v_next = vdd_pts[i + 1]
                    vseg = Line(
                        axes.c2p(i + 1, v), axes.c2p(i + 1, v_next),
                        color=ACCENT_2 if v_next >= V_BOR else WARN,
                        stroke_width=3,
                    )
                    grp.add(vseg)
            # Dot at current position
            v_now = vdd_pts[n]
            dot = Circle(radius=0.07).set_fill(
                ACCENT_2 if v_now >= V_BOR else WARN, opacity=1
            ).set_stroke(width=0)
            dot.move_to(axes.c2p(n, v_now))
            grp.add(dot)
            return grp

        div_trace = always_redraw(make_div_trace)

        # Regulator dot (follows x only)
        def make_reg_dot():
            n = get_n()
            dot = Circle(radius=0.07).set_fill(ACCENT_1, opacity=1).set_stroke(width=0)
            dot.move_to(axes.c2p(n, V_REG))
            return dot

        reg_dot = always_redraw(make_reg_dot)

        # Plot legend (anchored inside plot, top-right)
        legend_div = VGroup(
            Line(ORIGIN, RIGHT * 0.35).set_color(ACCENT_2),
            MathTex(r"\text{Divider}").set_color(FG).scale(0.32),
        ).arrange(RIGHT, buff=0.08)
        legend_reg = VGroup(
            Line(ORIGIN, RIGHT * 0.35).set_color(ACCENT_1),
            MathTex(r"\text{Regulator}").set_color(FG).scale(0.32),
        ).arrange(RIGHT, buff=0.08)
        plot_legend = VGroup(legend_div, legend_reg).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        plot_legend.move_to(axes.c2p(2.6, 3.42))

        # =========================================================
        # §9  Brown-out overlay
        # =========================================================
        brownout_text = MathTex(r"\text{BROWN-OUT RESET!}").set_color(WARN).scale(0.85)
        brownout_text.move_to(top_circ_rect.get_center())

        # =========================================================
        # §10  Final summary captions
        # =========================================================
        summary_top = MathTex(
            r"\text{Divider: good for sensing, bad for power}"
        ).set_color(WARN).scale(0.50)
        summary_top.next_to(top_circ_rect, DOWN, buff=0.04).align_to(top_circ_rect, LEFT)

        summary_bot = MathTex(
            r"\text{Regulator: stable supply}"
        ).set_color(ACCENT_1).scale(0.50)
        summary_bot.next_to(bot_circ_rect, DOWN, buff=0.04).align_to(bot_circ_rect, LEFT)

        # =========================================================
        # §11  Animation sequence
        # =========================================================

        # --- INTRO: labels + separator ---
        self.play(
            FadeIn(top_label), FadeIn(bot_label), FadeIn(separator),
            run_time=1.5,
        )
        self.wait(0.5)

        # --- Circuits ---
        self.play(FadeIn(circ_top), FadeIn(circ_bot), run_time=2.0)
        self.wait(0.5)

        # --- VDD readouts ---
        self.play(FadeIn(vdd_readout_top), FadeIn(vdd_readout_bot), run_time=1.0)
        self.wait(1.0)

        # --- Callouts (Thévenin + waste) ---
        self.play(FadeIn(thevenin_card), run_time=1.5)
        self.play(pop(thevenin_rth), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(power_meter), run_time=1.2)
        self.wait(1.0)

        # --- Plot ---
        self.play(
            Create(axes), FadeIn(x_label), FadeIn(y_label),
            FadeIn(x_ticks), FadeIn(y_ticks),
            Create(bor_line), FadeIn(bor_label),
            Create(reg_line),
            FadeIn(plot_legend),
            run_time=2.0,
        )
        self.play(FadeIn(div_trace), FadeIn(reg_dot), run_time=1.0)
        self.wait(2.0)

        # --- LED1 ON ---
        self.play(n_leds.animate.set_value(1), run_time=2.5)
        self.wait(2.0)

        # --- LED2 ON ---
        self.play(n_leds.animate.set_value(2), run_time=2.5)
        self.wait(2.0)

        # --- LED3 ON → brown-out ---
        self.play(n_leds.animate.set_value(3), run_time=2.5)
        self.wait(1.0)

        # Brown-out effects
        self.play(circ_top.animate.set_opacity(0.35), run_time=0.5)
        self.play(FadeIn(brownout_text, scale=1.3), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(brownout_text), run_time=0.5)
        self.wait(0.5)
        self.play(circ_top.animate.set_opacity(1.0), run_time=0.6)
        self.wait(1.0)

        # --- Final summary ---
        self.play(FadeIn(summary_top), FadeIn(summary_bot), run_time=2.0)
        self.wait(4.0)
