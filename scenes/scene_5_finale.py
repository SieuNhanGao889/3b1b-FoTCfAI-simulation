"""
scenes/scene_5_finale.py
SCENE 5: Convergence and closing message.
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


class Finale(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Everything Converges}")
        sub = make_sub(r"\text{One low-rank principle}")
        self.play(FadeIn(title), FadeIn(sub), run_time=T_FAST)

        icon_tensor = Tensor3D(nx=3, ny=3, nz=3, cell_size=0.20, face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        icon_tensor.move_to(at(X_LEFT - 1.2, Y_BODY + 1.2))

        icon_cp = VGroup(
            Rectangle(width=0.20, height=0.85, fill_color=VECTOR_COLOR, fill_opacity=0.85, stroke_width=0),
            Rectangle(width=0.85, height=0.20, fill_color=MATRIX_COLOR, fill_opacity=0.85, stroke_width=0),
            Rectangle(width=0.20, height=0.65, fill_color=BLUE_C, fill_opacity=0.85, stroke_width=0),
        ).arrange(RIGHT, buff=0.10).move_to(at(X_RIGHT + 1.0, Y_BODY + 1.1))

        icon_circuit = VGroup(
            Circle(radius=0.18, fill_color=SUM_NODE_COLOR, fill_opacity=0.9, stroke_width=0),
            Circle(radius=0.18, fill_color=PRODUCT_NODE_COLOR, fill_opacity=0.9, stroke_width=0).shift(RIGHT * 0.7),
            Line(LEFT * 0.15, RIGHT * 0.55, color=SUBTITLE_COLOR, stroke_width=1.5),
        ).move_to(at(X_LEFT - 1.3, Y_BODY - 1.4))

        prism = Triangle(fill_color="#9fd8ff", fill_opacity=0.30, stroke_color="#9fd8ff", stroke_width=2).scale(0.45).move_to(at(X_RIGHT + 1.0, Y_BODY - 1.5))

        icons = VGroup(icon_tensor, icon_cp, icon_circuit, prism)
        self.play(LaggedStart(*[FadeIn(i, scale=0.7) for i in icons], lag_ratio=0.2), run_time=T_MEDIUM)

        self.play(*[i.animate.move_to(at(0, Y_BODY)).scale(0.12) for i in icons], run_time=T_SLOW)
        self.play(FadeOut(icons), run_time=T_FAST)

        formula = MathTex(r"\mathcal{X}\approx\sum_{r=1}^{R} a_r\circ b_r\circ c_r", font_size=54, color=HIGHLIGHT_COLOR).move_to(at(0, Y_BODY + 0.1))
        self.play(Write(formula), run_time=T_SLOW)

        glow = formula.copy().set_stroke(HIGHLIGHT_COLOR, width=9, opacity=0.25)
        self.play(FadeIn(glow), run_time=0.4)
        self.play(FadeOut(glow), run_time=0.4)

        essence = make_note(r"\text{Complexity from simple parts}")
        self.play(FadeIn(essence), run_time=T_MEDIUM)
        self.wait(1.0)

        self.play(FadeOut(VGroup(sub, formula, essence)), run_time=T_MEDIUM)

        sub_close = make_sub(r"\text{Closing}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(sub_close), run_time=T_FAST)

        lines = [
            MathTex(r"\text{AI is not magic.}", font_size=34, color=WHITE),
            MathTex(r"\text{It is geometry.}", font_size=34, color=TENSOR_EDGE_COLOR),
            MathTex(r"\text{Tensors structure reality.}", font_size=30, color=VECTOR_COLOR),
            MathTex(r"\text{Low-rank reveals essence.}", font_size=30, color=HIGHLIGHT_COLOR),
        ]

        for i, line in enumerate(lines):
            line.move_to(at(0, 1.4 - i * 0.8))
            self.play(FadeIn(line, shift=UP * 0.08), run_time=T_MEDIUM)
            self.wait(0.25)

        # soft gradient ambience
        grad = VGroup(*[
            Rectangle(width=16, height=0.55, fill_color=interpolate_color(ManimColor(BG_COLOR), ManimColor("#001933"), i / 16), fill_opacity=0.08, stroke_width=0).shift(DOWN * (4.2 - i * 0.55))
            for i in range(16)
        ])
        self.play(FadeIn(grad), run_time=T_SLOW)

        rng = np.random.default_rng(123)
        particles = VGroup(*[
            Dot(at(rng.uniform(-6, 6), rng.uniform(-3.6, 3.2)), radius=rng.uniform(0.02, 0.05), color=HIGHLIGHT_COLOR, fill_opacity=rng.uniform(0.25, 0.55))
            for _ in range(28)
        ])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in particles], lag_ratio=0.03), run_time=T_MEDIUM)

        thanks_box = RoundedRectangle(corner_radius=0.22, width=8.8, height=2.5, fill_color="#090916", fill_opacity=0.94, stroke_color=HIGHLIGHT_COLOR, stroke_width=1.6)
        thanks_box.move_to(at(0, -1.7))
        thanks = MathTex(r"\text{Thank you for watching.}", font_size=30, color=WHITE).move_to(thanks_box.get_center() + UP * 0.3)
        team = MathTex(r"\text{Tensors in AI}", font_size=20, color=HIGHLIGHT_COLOR).next_to(thanks, DOWN, buff=0.22)

        self.play(FadeIn(thanks_box, scale=0.9), run_time=T_MEDIUM)
        self.play(FadeIn(thanks), FadeIn(team), run_time=T_MEDIUM)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_SLOW)
