"""
scenes/scene_2d_polynomial_networks.py
SCENE 2D: Polynomial Networks (4:00 - 5:00)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from config import *
from utils.tensor_objects import Tensor3D


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


class PolynomialNetworks(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Polynomial Networks as Tensor Models}")
        self.play(FadeIn(title), run_time=T_FAST)

        sub_1 = make_sub(r"\text{Self-interaction builds higher order features}")
        self.play(FadeIn(sub_1), run_time=T_FAST)

        x_vec = VGroup(*[
            MathTex(rf"x_{i+1}", font_size=24, color=VECTOR_COLOR)
            for i in range(4)
        ]).arrange(DOWN, buff=0.20)
        b_l = MathTex(r"[", font_size=60, color=VECTOR_COLOR)
        b_r = MathTex(r"]", font_size=60, color=VECTOR_COLOR)
        x_group = VGroup(b_l, x_vec, b_r).arrange(RIGHT, buff=0.08).move_to(at(X_LEFT - 1.0, Y_BODY))
        x_lbl = MathTex(r"\mathbf{x}", font_size=28, color=VECTOR_COLOR).next_to(x_group, UP, buff=0.12)

        mat_xx = Square(side_length=1.35, fill_color=MATRIX_COLOR, fill_opacity=0.5, stroke_color=MATRIX_COLOR, stroke_width=2)
        mat_xx.move_to(at(X_LEFT + 1.0, Y_BODY))
        mat_lbl = MathTex(r"\mathbf{x}\circ\mathbf{x}", font_size=20, color=MATRIX_COLOR).next_to(mat_xx, UP, buff=0.10)

        arrow_1 = Arrow(x_group.get_right(), mat_xx.get_left(), buff=0.12, color=SUBTITLE_COLOR, stroke_width=2)
        op_lbl_1 = MathTex(r"\circ", font_size=26, color=PRODUCT_NODE_COLOR).next_to(arrow_1, UP, buff=0.04)

        self.play(FadeIn(x_group), FadeIn(x_lbl), run_time=T_MEDIUM)
        self.play(GrowArrow(arrow_1), FadeIn(op_lbl_1), run_time=T_FAST)
        self.play(FadeIn(mat_xx, scale=0.75), FadeIn(mat_lbl), run_time=T_MEDIUM)

        block3 = Tensor3D(nx=3, ny=3, nz=3, cell_size=0.26, face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block3.move_to(at(X_LEFT + 3.1, Y_BODY))
        b3_lbl = MathTex(r"\mathbf{x}^{\circ 3}", font_size=22, color=TENSOR_EDGE_COLOR).next_to(block3, UP, buff=0.10)

        arrow_2 = Arrow(mat_xx.get_right(), block3.get_left(), buff=0.10, color=SUBTITLE_COLOR, stroke_width=2)
        op_lbl_2 = MathTex(r"\circ\mathbf{x}", font_size=18, color=PRODUCT_NODE_COLOR).next_to(arrow_2, UP, buff=0.04)

        self.play(GrowArrow(arrow_2), FadeIn(op_lbl_2), run_time=T_FAST)
        self.play(FadeIn(block3, scale=0.8), FadeIn(b3_lbl), run_time=T_MEDIUM)

        block4 = VGroup()
        for i in range(3):
            b = Tensor3D(nx=3, ny=3, nz=3, cell_size=0.20, face_color=BLUE_E, edge_color=BLUE_B)
            b.shift(at(X_RIGHT - 1.4 + 0.18 * i, Y_BODY + 0.12 * i))
            block4.add(b)
        b4_lbl = MathTex(r"\mathbf{x}^{\circ 4}", font_size=22, color=BLUE_B).next_to(block4, UP, buff=0.10)

        arrow_3 = Arrow(block3.get_right(), block4.get_left(), buff=0.10, color=SUBTITLE_COLOR, stroke_width=2)
        self.play(GrowArrow(arrow_3), run_time=T_FAST)
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in block4], lag_ratio=0.15), FadeIn(b4_lbl), run_time=T_MEDIUM)

        w_box = Rectangle(width=1.0, height=0.9, fill_color=PRODUCT_NODE_COLOR, fill_opacity=0.35, stroke_color=PRODUCT_NODE_COLOR, stroke_width=2)
        w_box.move_to(at(X_RIGHT + 1.8, Y_BODY + 0.1))
        w_lbl = MathTex(r"\mathcal{W}", font_size=24, color=PRODUCT_NODE_COLOR).next_to(w_box, UP, buff=0.08)

        con_arr = Arrow(block4.get_right(), w_box.get_left(), buff=0.10, color=HIGHLIGHT_COLOR, stroke_width=2)
        y_dot = Dot(w_box.get_right() + RIGHT * 0.65, color=HIGHLIGHT_COLOR, radius=0.14)
        y_lbl = MathTex(r"y", font_size=26, color=HIGHLIGHT_COLOR).next_to(y_dot, UP, buff=0.06)

        eq = MathTex(r"y=\langle\mathcal{W},\mathbf{x}^{\circ 4}\rangle", font_size=26, color=WHITE).move_to(at(X_RIGHT, Y_NOTE + 0.55))
        note = make_note(r"\text{Higher-order interactions}")

        self.play(GrowArrow(con_arr), FadeIn(w_box), FadeIn(w_lbl), run_time=T_FAST)
        self.play(GrowFromCenter(y_dot), FadeIn(y_lbl), run_time=T_FAST)
        self.play(Write(eq), FadeIn(note), run_time=T_MEDIUM)
        self.wait(0.7)

        keep = VGroup(title)
        self.play(FadeOut(VGroup(*[m for m in self.mobjects if m not in keep])), run_time=T_FAST)

        sub_2 = make_sub(r"\text{Nonlinear boundaries emerge}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(sub_2), run_time=T_FAST)

        ax_l = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=3.5, y_length=3.5, axis_config={"stroke_color": SUBTITLE_COLOR, "include_tip": False})
        ax_l.move_to(at(X_LEFT + 0.8, Y_BODY - 0.2))
        ax_r = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=3.5, y_length=3.5, axis_config={"stroke_color": SUBTITLE_COLOR, "include_tip": False})
        ax_r.move_to(at(X_RIGHT, Y_BODY - 0.2))

        line = ax_l.plot(lambda x: 0.7 * x - 0.2, color=VECTOR_COLOR, stroke_width=2.5)
        curve = ax_r.plot_parametric_curve(lambda t: np.array([2.1 * np.cos(t), 1.4 * np.sin(t) + 0.1, 0]), t_range=[0, TAU], color=TENSOR_EDGE_COLOR, stroke_width=2.5)

        l_lbl = MathTex(r"\text{Linear}", font_size=18, color=VECTOR_COLOR).next_to(ax_l, DOWN, buff=0.12)
        r_lbl = MathTex(r"\text{Nonlinear}", font_size=18, color=TENSOR_EDGE_COLOR).next_to(ax_r, DOWN, buff=0.12)

        self.play(Create(ax_l), Create(ax_r), run_time=T_FAST)
        self.play(Create(line), Create(curve), FadeIn(l_lbl), FadeIn(r_lbl), run_time=T_MEDIUM)

        close = make_note(r"\text{Richer boundaries from higher-order structure}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(close), run_time=T_MEDIUM)
        self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MEDIUM)
