"""
scenes/scene_1c_data_explosion.py
─────────────────────────────────────────────────────────────────────────────
SCENE 1C  "The data explosion → Low-Rank Factorization"  (1:10 – 1:30)

Pedagogical goals (from feedback):
  1. Motivate tensor decomposition via the THREE canonical ML problems:
       (a) Models too large
       (b) Inference too slow
       (c) Black-box models (lack of structure / interpretability)
  2. Show memory blow-up as block grows.
  3. Introduce "Low-Rank Factorization" as the answer with a visual teaser.
─────────────────────────────────────────────────────────────────────────────
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D


class DataExplosion(Scene):

    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Three-problem motivation ──────────────────────────────────────
        problems = VGroup(
            DataExplosion._problem_card( 
                "Models too large",
                "Billions of parameters\ndon't fit on one GPU",
                color="#ff5555",
            ),
            DataExplosion._problem_card( 
                "Inference too slow",
                "O(N²) attention over\nlong sequences",
                color="#ffaa33",
            ),
            DataExplosion._problem_card( 
                "Black-box models",
                "No structure ⟹ no\ninterpretability",
                color="#aaaaff",
            )
        ).arrange(RIGHT, buff=0.4)
        problems.move_to(UP * 1.5)

        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in problems],
                        lag_ratio=0.3),
            run_time=T_SLOW,
        )
        self.wait(0.5)

        connector = Text("Why tensor decomposition?", font_size=24,
                         color=HIGHLIGHT_COLOR, weight=BOLD)
        connector.next_to(problems, DOWN, buff=0.35)
        self.play(Write(connector), run_time=T_MEDIUM)
        self.wait(0.6)

        # ── ML systems need multiway structure ────────────────────────────
        multiway = Text(
            "ML data has multiple modes of variation.\n"
            "Tensors preserve this multiway structure naturally.",
            font_size=19, color=SUBTITLE_COLOR,
            line_spacing=0.5,
        ).next_to(connector, DOWN, buff=0.3)
        self.play(FadeIn(multiway, shift=UP * 0.1), run_time=T_MEDIUM)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(problems, connector, multiway)),
            run_time=T_FAST,
        )

        # ── Memory blow-up ────────────────────────────────────────────────
        block = Tensor3D(nx=4, ny=3, nz=5, cell_size=0.30,
                         face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(block, scale=0.7), run_time=T_FAST)

        # Counter
        counter = Integer(4 * 3 * 5, font_size=36, color=VECTOR_COLOR)
        counter_label = Text(" parameters", font_size=22, color=SUBTITLE_COLOR)
        counter_grp = VGroup(counter, counter_label).arrange(RIGHT, buff=0.08)
        counter_grp.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(counter_grp), run_time=T_FAST)

        # Grow the block in 3 steps
        scales = [1.5, 2.0, 2.8]
        param_counts = [1_000, 10_000, 1_000_000]

        for sc, pc in zip(scales, param_counts):
            self.play(
                block.animate.scale(sc / scales[scales.index(sc) - 1]
                                    if scales.index(sc) > 0 else sc),
                ChangeDecimalToValue(counter, pc),
                run_time=T_MEDIUM,
            )

        # Flash warning
        warning = Text("⚠  Memory explosion!", font_size=28,
                       color="#ff4444", weight=BOLD)
        warning.next_to(block, UP, buff=0.3)
        self.play(FadeIn(warning, scale=1.2), run_time=T_FAST)
        self.play(warning.animate.set_color(RED), run_time=0.3,
                  rate_func=there_and_back)
        self.wait(0.4)

        self.play(
            FadeOut(VGroup(block, counter_grp, warning)),
            run_time=T_FAST,
        )

        # ── Low-Rank teaser ───────────────────────────────────────────────
        big_block = Tensor3D(nx=6, ny=5, nz=7, cell_size=0.28,
                             face_color="#334455", edge_color=TENSOR_EDGE_COLOR)
        big_block.shift(LEFT * 2.5)
        self.play(FadeIn(big_block, scale=0.6), run_time=T_FAST)

        # Three thin factor "sticks"
        vec_a = Rectangle(width=0.3, height=1.6,
                          fill_color=VECTOR_COLOR, fill_opacity=0.85,
                          stroke_width=0)
        vec_b = Rectangle(width=1.6, height=0.3,
                          fill_color=MATRIX_COLOR, fill_opacity=0.85,
                          stroke_width=0)
        vec_c = Rectangle(width=0.3, height=0.9,
                          fill_color=TENSOR_EDGE_COLOR, fill_opacity=0.85,
                          stroke_width=0)
        factors = VGroup(vec_a, vec_b, vec_c).arrange(RIGHT, buff=0.3)
        factors.shift(RIGHT * 1.8)

        arrow = Arrow(big_block.get_right(), factors.get_left(),
                      color=HIGHLIGHT_COLOR, stroke_width=3,
                      max_tip_length_to_length_ratio=0.2)
        approx = Text("≈", font_size=34,
                         color=MATH_COLOR).next_to(big_block, RIGHT, buff=0.15)

        self.play(GrowArrow(arrow), FadeIn(approx), run_time=T_FAST)
        self.play(
            LaggedStart(*[GrowFromCenter(f) for f in factors], lag_ratio=0.3),
            run_time=T_MEDIUM,
        )

        # Final reveal text
        answer = Text("LOW-RANK FACTORIZATION", font_size=30,
                      color=HIGHLIGHT_COLOR, weight=BOLD)
        answer.to_edge(DOWN, buff=0.5)
        self.play(Write(answer), run_time=T_MEDIUM)

        sub = Text(
            "Compress the block into a few small factors –\n"
            "preserving the essential structure.",
            font_size=18, color=SUBTITLE_COLOR, line_spacing=0.45,
        ).next_to(answer, UP, buff=0.2)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=T_FAST)
        self.wait(1.8)

        self.play(FadeOut(VGroup(big_block, arrow, approx, factors, answer, sub)),
                  run_time=T_MEDIUM)

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _problem_card(title: str, body: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.15,
            width=3.0, height=2.2,
            fill_color=color, fill_opacity=0.15,
            stroke_color=color, stroke_width=1.5,
        )
        t = Text(title, font_size=17, color=color, weight=BOLD)
        b = Text(body, font_size=14, color=SUBTITLE_COLOR, line_spacing=0.4)
        t.next_to(bg.get_top(), DOWN, buff=0.2)
        b.move_to(bg).shift(DOWN * 0.15)
        return VGroup(bg, t, b)
