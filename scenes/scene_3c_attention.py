"""
scenes/scene_3c_attention.py
SCENE 3C: Attention complexity from O(N^2) to O(N).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *


Y_TITLE = 3.40
Y_SUB = 2.72
Y_BODY = 0.10
Y_NOTE = -3.30
X_LEFT = -3.70
X_RIGHT = 3.10


def at(x, y):
    return np.array([x, y, 0])


def make_title(s):
    return MathTex(s, font_size=32, color=HIGHLIGHT_COLOR).move_to(at(0, Y_TITLE))


def make_sub(s, color=SUBTITLE_COLOR):
    return MathTex(s, font_size=26, color=color).move_to(at(0, Y_SUB))


def make_note(s, color=SUBTITLE_COLOR):
    return MathTex(s, font_size=22, color=color).move_to(at(0, Y_NOTE))


class PolynomialAttention(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Attention Cost}")
        self.play(FadeIn(title), run_time=T_FAST)

        sub_1 = make_sub(r"\text{Full }N\times N\text{ map}")
        self.play(FadeIn(sub_1), run_time=T_FAST)

        n = 7
        cell = 0.38
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(
                    side_length=cell,
                    fill_color=TENSOR_COLOR,
                    fill_opacity=0.25 + 0.5 * abs(i - j) / n,
                    stroke_color=TENSOR_EDGE_COLOR,
                    stroke_width=0.6,
                )
                sq.move_to(at(X_LEFT + (j - n / 2 + 0.5) * cell, Y_BODY + (n / 2 - i - 0.5) * cell))
                grid.add(sq)

        qkt = MathTex(r"QK^\top\in\mathbb{R}^{N\times N}", font_size=22, color=WHITE).move_to(at(X_LEFT, Y_BODY - 1.8))
        old_c = MathTex(r"O(N^2)", font_size=34, color=RED_C).move_to(at(X_RIGHT, Y_BODY + 0.7))
        old_note = MathTex(r"\text{All-to-all}", font_size=18, color=SUBTITLE_COLOR).next_to(old_c, DOWN, buff=0.18)

        self.play(LaggedStart(*[FadeIn(s, scale=0.85) for s in grid], lag_ratio=0.01), run_time=T_MEDIUM)
        self.play(FadeIn(qkt), FadeIn(old_c), FadeIn(old_note), run_time=T_FAST)

        std_formula = MathTex(r"QK^\top", font_size=28, color=WHITE).move_to(at(0, Y_NOTE + 0.55))
        self.play(Write(std_formula), run_time=T_MEDIUM)
        self.wait(0.6)

        sub_2 = make_sub(r"\text{Reordered computation}", color=HIGHLIGHT_COLOR)
        self.play(ReplacementTransform(sub_1, sub_2), run_time=T_FAST)

        line_vec = VGroup(*[
            Square(side_length=cell, fill_color=MATRIX_COLOR, fill_opacity=0.85, stroke_color=MATRIX_COLOR, stroke_width=0.6)
            for _ in range(n)
        ]).arrange(RIGHT, buff=0.02).move_to(at(X_LEFT, Y_BODY))

        self.play(ReplacementTransform(grid, line_vec), FadeOut(qkt), run_time=T_MEDIUM)

        new_c = MathTex(r"O(N)", font_size=34, color=GREEN_C).move_to(old_c)
        poly_formula = MathTex(r"\phi(Q)\big(\phi(K)^\top V\big)", font_size=24, color=WHITE).move_to(std_formula)
        idea = MathTex(r"\text{No explicit }N\times N", font_size=18, color=HIGHLIGHT_COLOR).next_to(poly_formula, UP, buff=0.18)

        self.play(ReplacementTransform(old_c, new_c), FadeOut(old_note), run_time=T_FAST)
        self.play(ReplacementTransform(std_formula, poly_formula), FadeIn(idea), run_time=T_MEDIUM)

        self.play(FadeOut(VGroup(line_vec, poly_formula, idea)), run_time=T_FAST)

        maze = VMobject(color=RED_C, stroke_width=3)
        maze.set_points_as_corners([
            at(X_LEFT - 1.0, Y_BODY + 0.8), at(X_LEFT - 1.0, Y_BODY - 0.2), at(X_LEFT + 0.2, Y_BODY - 0.2),
            at(X_LEFT + 0.2, Y_BODY + 0.6), at(X_LEFT + 1.3, Y_BODY + 0.6), at(X_LEFT + 1.3, Y_BODY - 0.7),
            at(X_LEFT + 2.1, Y_BODY - 0.7),
        ])
        straight = Line(at(X_RIGHT - 1.8, Y_BODY), at(X_RIGHT + 1.8, Y_BODY), color=GREEN_C, stroke_width=3)
        maze_lbl = MathTex(r"O(N^2)", font_size=22, color=RED_C).next_to(maze, DOWN, buff=0.12)
        straight_lbl = MathTex(r"O(N)", font_size=22, color=GREEN_C).next_to(straight, DOWN, buff=0.12)

        self.play(Create(maze), FadeIn(maze_lbl), run_time=T_MEDIUM)
        self.play(Create(straight), FadeIn(straight_lbl), run_time=T_MEDIUM)

        note = make_note(r"\textbf{From }O(N^2)\textbf{ to }O(N)", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(note), run_time=T_MEDIUM)
        self.wait(1.1)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MEDIUM)
