"""
scenes/scene_2c_lora.py
SCENE 2C: LoRA in LLMs (3:20 – 4:00)  ≈ 40 seconds

STORY ARC (Show Don't Tell):
  Beat 1  (0–10s)  : PROBLEM — Giant W matrix fills the screen. Tiny GPU icon crushed under it.
                      Viewer FEELS the weight before reading any text.
  Beat 2  (10–25s) : INSIGHT — W "cracks" open. Two thin slabs A, B slide out.
                      The SIZE CONTRAST does the explaining: A and B are visually tiny next to W.
  Beat 3  (25–40s) : PAYOFF — Pixel-count comparison: 16M dots vs 65K dots (actual dot grid),
                      then big "256×" stamp animates in. No bar charts — literal dots.

Design principle:
  - Every number is SHOWN geometrically, not just printed as text.
  - Animation direction carries meaning (crush → crack → relief).
  - Color: W = cold grey (heavy), A = warm blue (light), B = warm amber (light), 
           reduction stamp = green (victory).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *

# ── Layout ────────────────────────────────────────────────────────────────────
Y_TITLE =  3.30
Y_SUB   =  2.65
Y_BODY  =  0.00
Y_NOTE  = -3.00

def at(x, y):
    return np.array([x, y, 0])

def tx(s, size=28, color=WHITE):
    return MathTex(s, font_size=size, color=color)

def words(s, size=26, color=WHITE):
    return Text(s, font_size=size, color=color)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_matrix_rect(w, h, fc, ec, label_tex, label_color, label_size=22):
    """A filled rectangle representing a matrix, with a dimension label below."""
    rect = Rectangle(width=w, height=h,
                     fill_color=fc, fill_opacity=0.82,
                     stroke_color=ec, stroke_width=1.8)
    lbl  = MathTex(label_tex, font_size=label_size, color=label_color)
    lbl.next_to(rect, DOWN, buff=0.13)
    return rect, lbl


def dot_grid(rows, cols, dot_r=0.025, color=WHITE, opacity=0.6, h_gap=0.07, v_gap=0.07):
    """Return a VGroup of dots arranged in a rows×cols grid."""
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=dot_r, color=color, fill_opacity=opacity)
            d.move_to(RIGHT * c * h_gap + DOWN * r * v_gap)
            grid.add(d)
    return grid


# ── Scene ─────────────────────────────────────────────────────────────────────
class LoRAScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ══════════════════════════════════════════════════════════════════════
        # BEAT 1 (0–10s): THE WEIGHT OF W
        # Visual story: W matrix is HUGE → GPU icon is tiny and struggling
        # ══════════════════════════════════════════════════════════════════════

        # --- W matrix: deliberately oversized to feel oppressive ---
        W_rect = Rectangle(
            width=5.2, height=4.8,
            fill_color="#1a2a4a", fill_opacity=0.92,
            stroke_color=GREY_C, stroke_width=2.5
        )
        W_rect.move_to(at(0.5, Y_BODY + 0.2))

        # Grid lines inside W to convey "many parameters"
        grid_lines = VGroup()
        for i in range(1, 8):
            grid_lines.add(
                Line(W_rect.get_left() + RIGHT * i * (5.2 / 8),
                     W_rect.get_left() + RIGHT * i * (5.2 / 8) + UP * 4.8,
                     stroke_color=GREY_D, stroke_width=0.4, stroke_opacity=0.4)
            )
        for j in range(1, 7):
            grid_lines.add(
                Line(W_rect.get_bottom() + UP * j * (4.8 / 7),
                     W_rect.get_bottom() + UP * j * (4.8 / 7) + RIGHT * 5.2,
                     stroke_color=GREY_D, stroke_width=0.4, stroke_opacity=0.4)
            )

        W_label = tx(r"W", 56, GREY_C)
        W_label.move_to(W_rect.get_center() + UP * 0.3)
        W_dim   = tx(r"4096\times 4096", 22, GREY_B)
        W_dim.move_to(W_rect.get_center() + DOWN * 0.6)

        # W flies in from top, lands with "weight" (overshoot)
        W_group = VGroup(W_rect, grid_lines, W_label, W_dim)
        W_group.shift(UP * 8)  # start off-screen top

        self.play(
            W_group.animate.shift(DOWN * 8),
            run_time=1.1,
            rate_func=rate_functions.ease_in_out_cubic
        )

        # GPU icon: a small rectangle representing a GPU, placed bottom-left
        gpu = RoundedRectangle(corner_radius=0.12, width=1.1, height=0.6,
                               fill_color="#004400", fill_opacity=0.9,
                               stroke_color=GREEN_C, stroke_width=1.5)
        gpu_lbl = words("GPU", 16, GREEN_C)
        gpu_lbl.move_to(gpu)
        gpu_group = VGroup(gpu, gpu_lbl)
        gpu_group.move_to(at(-5.2, -2.8))

        self.play(FadeIn(gpu_group), run_time=0.4)

        # GPU tries to "hold up" the matrix — it slides further down, GPU squishes
        self.play(
            gpu_group.animate.shift(DOWN * 0.28).scale(0.82),
            W_group.animate.shift(DOWN * 0.12),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_sine
        )

        # Caption appears: the number, not as text first — as a pixel count hint
        caption_1 = tx(r"16{,}777{,}216\ \text{parameters}", 28, RED_C)
        caption_1.move_to(at(-4.0, Y_TITLE - 0.2))
        self.play(Write(caption_1), run_time=0.8)
        self.wait(2.0)   # let viewer absorb the weight

        # ══════════════════════════════════════════════════════════════════════
        # BEAT 2 (10–25s): THE CRACK — W breaks into A and B
        # Visual story: crack line appears on W, A slides left, B slides right
        # Then SIZE CONTRAST is the argument: A,B are visually tiny vs W
        # ══════════════════════════════════════════════════════════════════════

        sub_insight = tx(r"\text{LoRA: }\Delta W \approx B \cdot A", 30, HIGHLIGHT_COLOR)
        sub_insight.move_to(at(0, Y_TITLE - 0.2))

        # Crack line across W (horizontal, at mid-height)
        crack = Line(
            W_rect.get_left() + UP * 0.0,
            W_rect.get_right() + UP * 0.0,
            stroke_color=YELLOW, stroke_width=2.5
        )

        self.play(
            FadeOut(caption_1),
            Create(crack),
            run_time=0.7
        )

        # Flash effect on crack
        self.play(
            crack.animate.set_stroke(color=WHITE, width=5),
            run_time=0.25,
            rate_func=there_and_back
        )

        # W dims (becomes ghost), A and B emerge from the crack
        # A: thin vertical slab (r × 4096)  — r=8 so very thin
        # B: thin horizontal slab (4096 × r) — very thin
        # We make them PROPORTIONALLY accurate to feel the thinness:
        # Full W is 5.2 wide × 4.8 tall. r=8, n=4096 → r/n = 8/4096 ≈ 0.002
        # If we show 1/20th of W width for r dimension it still looks thin: 0.28 wide

        A_rect, A_lbl = make_matrix_rect(
            w=0.28, h=4.0,
            fc=BLUE_C, ec=BLUE_B,
            label_tex=r"A\;(8\times 4096)", label_color=BLUE_B, label_size=20
        )
        B_rect, B_lbl = make_matrix_rect(
            w=4.0, h=0.28,
            fc=GOLD, ec=GOLD_A,
            label_tex=r"B\;(4096\times 8)", label_color=GOLD_A, label_size=20
        )

        A_group = VGroup(A_rect, A_lbl)
        B_group = VGroup(B_rect, B_lbl)

        # Start A and B at the center (crack location), then slide apart
        A_group.move_to(W_rect.get_center())
        B_group.move_to(W_rect.get_center())

        self.play(
            W_group.animate.set_opacity(0.12),
            FadeOut(crack),
            FadeIn(sub_insight, shift=DOWN * 0.2),
            run_time=0.7
        )

        self.play(
            A_group.animate.move_to(at(-2.8, Y_BODY + 0.8)),
            B_group.animate.move_to(at( 1.8, Y_BODY - 0.5)),
            run_time=1.4,
            rate_func=rate_functions.ease_out_cubic
        )

        # Times symbol between A and B
        times_sym = tx(r"\times", 34, PRODUCT_NODE_COLOR)
        times_sym.move_to(at(-0.6, Y_BODY + 0.2))
        self.play(FadeIn(times_sym), run_time=0.4)

        # r=8 badge — emphasize how small r is vs 4096
        r_badge = VGroup(
            tx(r"r = 8", 36, HIGHLIGHT_COLOR),
            tx(r"\ll 4096", 24, SUBTITLE_COLOR)
        ).arrange(RIGHT, buff=0.18)
        r_badge.move_to(at(0, Y_NOTE + 0.8))
        self.play(FadeIn(r_badge, scale=1.15), run_time=0.6)

        # Arrow from W ghost to A×B to show equivalence
        arrow_equiv = Arrow(
            W_rect.get_center() + LEFT * 0.3,
            times_sym.get_center() + UP * 0.6,
            buff=0.15, stroke_color=GREY_C, stroke_width=1.5,
            tip_length=0.18
        )
        equiv_lbl = tx(r"\Delta W \approx", 22, GREY_C)
        equiv_lbl.next_to(arrow_equiv, UP, buff=0.05)
        self.play(Create(arrow_equiv), FadeIn(equiv_lbl), run_time=0.7)
        self.wait(2.5)   # let the SIZE CONTRAST speak

        # ══════════════════════════════════════════════════════════════════════
        # BEAT 3 (25–40s): THE PAYOFF — Dot comparison + 256× stamp
        # Visual story: left side = thousands of red dots (W params),
        #               right side = tiny cluster of blue dots (LoRA params)
        # The DOT GRID is the argument — no bar charts needed.
        # ══════════════════════════════════════════════════════════════════════

        # Clear previous visuals except title area
        self.play(
            FadeOut(VGroup(
                W_group, A_group, B_group, times_sym, A_lbl, B_lbl,
                arrow_equiv, equiv_lbl, sub_insight, r_badge,
                gpu_group
            )),
            run_time=0.7
        )

        # ── Left panel: W = 4096×4096, represented as dense dot grid ──────
        # We can't draw 16M dots, so we draw a SCALED sample: 40×40 = 1600 dots
        # Label explains it's a sample
        panel_left_bg = Rectangle(
            width=4.2, height=4.2,
            fill_color="#1a0000", fill_opacity=0.6,
            stroke_color=RED_C, stroke_width=1.5
        ).move_to(at(-3.0, Y_BODY))

        dots_full = dot_grid(rows=28, cols=28, dot_r=0.028,
                             color=RED_C, opacity=0.75,
                             h_gap=0.13, v_gap=0.13)
        dots_full.move_to(panel_left_bg.get_center())

        lbl_full_top = tx(r"W\text{ : }4096\times4096", 22, RED_C)
        lbl_full_top.next_to(panel_left_bg, UP, buff=0.18)
        lbl_full_count = tx(r"16{,}777{,}216\ \text{parameters}", 20, RED_C)
        lbl_full_count.next_to(panel_left_bg, DOWN, buff=0.14)

        # ── Right panel: LoRA A+B = 2×r×4096 = 65,536 params ─────────────
        # Represented as sparse dot grid: 6×6 = 36 dots (vs 784 on left — ratio ~22×)
        panel_right_bg = Rectangle(
            width=4.2, height=4.2,
            fill_color="#001a00", fill_opacity=0.6,
            stroke_color=GREEN_C, stroke_width=1.5
        ).move_to(at(3.0, Y_BODY))

        # LoRA is 65536/16777216 ≈ 1/256 of W
        # If left has 28×28=784 dots, right should have ~784/256 ≈ 3 dots
        # Let's use 3×3=9 dots, placed in corner to show sparsity
        dots_lora = dot_grid(rows=4, cols=4, dot_r=0.07,
                             color=GREEN_C, opacity=0.9,
                             h_gap=0.22, v_gap=0.22)
        dots_lora.move_to(panel_right_bg.get_center())

        lbl_lora_top = tx(r"A+B\text{ (LoRA)}", 22, GREEN_C)
        lbl_lora_top.next_to(panel_right_bg, UP, buff=0.18)
        lbl_lora_count = tx(r"65{,}536\ \text{parameters}", 20, GREEN_C)
        lbl_lora_count.next_to(panel_right_bg, DOWN, buff=0.14)

        # Animate panels appearing
        self.play(
            FadeIn(panel_left_bg), FadeIn(panel_right_bg),
            FadeIn(lbl_full_top), FadeIn(lbl_lora_top),
            run_time=0.6
        )

        # Flood the left panel with dots (dramatic, LaggedStart)
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in dots_full],
                lag_ratio=0.006
            ),
            run_time=1.8
        )
        self.play(FadeIn(lbl_full_count), run_time=0.4)

        # Right panel: only a few dots appear — the EMPTINESS is the point
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in dots_lora],
                lag_ratio=0.08
            ),
            run_time=0.7
        )
        self.play(FadeIn(lbl_lora_count), run_time=0.4)

        # Pause — let the visual contrast land (this IS the argument)
        self.wait(1.2)

        # ── 256× REDUCTION STAMP ──────────────────────────────────────────
        # Big, bold, animated like a rubber stamp
        stamp_circle = Circle(radius=1.35,
                              stroke_color=HIGHLIGHT_COLOR, stroke_width=4,
                              fill_color=BG_COLOR, fill_opacity=0.92)
        stamp_text_1 = tx(r"256\times", 46, HIGHLIGHT_COLOR)
        stamp_text_2 = words("less parameters!", 22, HIGHLIGHT_COLOR)
        stamp_text_2.next_to(stamp_text_1, DOWN, buff=0.12)
        stamp = VGroup(stamp_circle, stamp_text_1, stamp_text_2)
        stamp.move_to(at(0, Y_BODY))

        # Stamp: scale from huge → normal with slight overshoot
        stamp.scale(2.5)
        self.play(
            stamp.animate.scale(1 / 2.5),
            run_time=0.55,
            rate_func=rate_functions.ease_out_bounce
        )

        # Final caption
        final_note = words("Fine-tune only with a regular laptop!", 24, GREEN_C)
        final_note.move_to(at(0, Y_NOTE + 0.5))
        self.play(Write(final_note), run_time=0.8)
        self.wait(2.5)

        # ── Outro ─────────────────────────────────────────────────────────
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)