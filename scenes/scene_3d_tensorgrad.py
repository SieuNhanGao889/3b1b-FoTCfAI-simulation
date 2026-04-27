"""
scenes/scene_3d_tensorgrad.py
SCENE 3D: TensorGrad memory reduction.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
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


class TensorGrad(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{TensorGrad}")
        self.play(FadeIn(title), run_time=T_FAST)

        sub_1 = make_sub(r"\text{Gradients are heavy}")
        self.play(FadeIn(sub_1), run_time=T_FAST)

        # Simple forward/backward sketch
        layers_x = [-5.2, -3.4, -1.6, 0.2]
        layers_n = [3, 4, 4, 3]
        nodes = []
        for x, n in zip(layers_x, layers_n):
            col = VGroup(*[
                Circle(radius=0.16, fill_color=BLUE_D, fill_opacity=0.8, stroke_width=0).move_to(at(x, Y_BODY + 0.45 * (i - (n - 1) / 2)))
                for i in range(n)
            ])
            nodes.append(col)

        edges = VGroup()
        for i in range(len(nodes) - 1):
            for a in nodes[i]:
                for b in nodes[i + 1]:
                    edges.add(Line(a.get_center(), b.get_center(), stroke_color=BLUE_C, stroke_opacity=0.35, stroke_width=0.6))

        fwd = Arrow(at(-5.9, -1.6), at(-0.3, -1.6), color=BLUE_C, stroke_width=2.2, max_tip_length_to_length_ratio=0.08)
        fwd_lbl = MathTex(r"\text{forward}", font_size=16, color=BLUE_C).next_to(fwd, DOWN, buff=0.08)
        bwd = Arrow(at(-0.3, -2.1), at(-5.9, -2.1), color=RED_C, stroke_width=2.2, max_tip_length_to_length_ratio=0.08)
        bwd_lbl = MathTex(r"\text{backward gradients}", font_size=16, color=RED_C).next_to(bwd, DOWN, buff=0.08)

        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), LaggedStart(*[GrowFromCenter(n) for col in nodes for n in col], lag_ratio=0.03), run_time=T_MEDIUM)
        self.play(GrowArrow(fwd), FadeIn(fwd_lbl), run_time=T_FAST)
        self.play(GrowArrow(bwd), FadeIn(bwd_lbl), run_time=T_FAST)

        grad = Tensor3D(nx=6, ny=5, nz=6, cell_size=0.20, face_color="#553333", edge_color="#ff8888")
        grad.move_to(at(X_RIGHT - 1.4, Y_BODY + 0.1))
        g_lbl = MathTex(r"\nabla W", font_size=24, color=RED_C).next_to(grad, UP, buff=0.10)

        self.play(FadeIn(grad, scale=0.8), FadeIn(g_lbl), run_time=T_MEDIUM)

        sub_2 = make_sub(r"\text{Factorize the gradient}", color=HIGHLIGHT_COLOR)
        self.play(ReplacementTransform(sub_1, sub_2), run_time=T_FAST)

        core = Tensor3D(nx=2, ny=2, nz=2, cell_size=0.28, face_color="#aa3333", edge_color=RED_C)
        core.move_to(at(X_RIGHT + 1.5, Y_BODY + 0.2))
        u = Rectangle(width=0.30, height=1.4, fill_color=VECTOR_COLOR, fill_opacity=0.85, stroke_width=0).move_to(at(X_RIGHT + 2.7, Y_BODY + 0.2))
        v = Rectangle(width=1.4, height=0.30, fill_color=MATRIX_COLOR, fill_opacity=0.85, stroke_width=0).move_to(at(X_RIGHT + 1.5, Y_BODY - 0.8))

        approx = MathTex(r"\approx", font_size=28, color=HIGHLIGHT_COLOR).move_to(at(X_RIGHT + 0.4, Y_BODY + 0.2))
        decomp_lbl = MathTex(r"\text{core + factors}", font_size=16, color=SUBTITLE_COLOR).next_to(core, UP, buff=0.08)

        self.play(grad.animate.set_opacity(0.25), FadeIn(approx), FadeIn(core, scale=0.75), FadeIn(u), FadeIn(v), FadeIn(decomp_lbl), run_time=T_MEDIUM)

        # Memory bars
        bars = VGroup(
            Rectangle(width=4.8, height=0.42, fill_color="#222222", fill_opacity=1, stroke_width=0).move_to(at(X_RIGHT, Y_BODY - 1.5)),
            Rectangle(width=4.8, height=0.42, fill_color="#222222", fill_opacity=1, stroke_width=0).move_to(at(X_RIGHT, Y_BODY - 2.0)),
        )
        old_fill = Rectangle(width=4.8, height=0.42, fill_color=RED_C, fill_opacity=0.9, stroke_width=0).move_to(bars[0])
        new_fill = Rectangle(width=0.96, height=0.42, fill_color=GREEN_C, fill_opacity=0.9, stroke_width=0)
        new_fill.align_to(bars[1], LEFT).move_to(bars[1].get_left() + RIGHT * (new_fill.width / 2))

        old_lbl = MathTex(r"\text{Before}\ 100\%", font_size=16, color=RED_C).next_to(bars[0], RIGHT, buff=0.12)
        new_lbl = MathTex(r"\text{After}\ 20\%", font_size=16, color=GREEN_C).next_to(bars[1], RIGHT, buff=0.12)

        self.play(FadeIn(bars[0]), GrowFromEdge(old_fill, LEFT), FadeIn(old_lbl), run_time=T_MEDIUM)
        self.play(FadeIn(bars[1]), GrowFromEdge(new_fill, LEFT), FadeIn(new_lbl), run_time=T_MEDIUM)

        note = make_note(r"5{\times} \text{ memory reduction}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(note), run_time=T_MEDIUM)
        self.wait(1.1)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MEDIUM)
