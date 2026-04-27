"""
scenes/scene_3ab_circuits.py
SCENE 3A + 3B: Tensor Circuits and SPN.
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


def sum_node(pos, radius=0.24):
    c = Circle(radius=radius, fill_color=SUM_NODE_COLOR, fill_opacity=0.9, stroke_width=0)
    t = MathTex(r"+", font_size=24, color=BLACK)
    return VGroup(c, t).move_to(pos)


def prod_node(pos, radius=0.24):
    c = Circle(radius=radius, fill_color=PRODUCT_NODE_COLOR, fill_opacity=0.9, stroke_width=0)
    t = MathTex(r"\times", font_size=18, color=BLACK)
    return VGroup(c, t).move_to(pos)


def leaf_node(pos, label):
    c = Circle(radius=0.20, fill_color=VECTOR_COLOR, fill_opacity=0.7, stroke_width=0)
    t = MathTex(label, font_size=16, color=WHITE)
    return VGroup(c, t).move_to(pos)


def connect(a, b):
    return Line(a.get_center(), b.get_center(), color=SUBTITLE_COLOR, stroke_width=1.5, stroke_opacity=0.75)


class CircuitsAndSPN(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Tensor Factorization as Computational Circuits}")
        self.play(FadeIn(title), run_time=T_FAST)

        # 3A
        sub_3a = make_sub(r"\text{Decomposition becomes a circuit}")
        self.play(FadeIn(sub_3a), run_time=T_FAST)

        block = Tensor3D(nx=4, ny=3, nz=5, cell_size=0.24, face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block.move_to(at(X_LEFT, Y_BODY))

        inputs = VGroup(
            leaf_node(at(X_RIGHT - 2.0, Y_BODY - 1.0), r"x_1"),
            leaf_node(at(X_RIGHT - 2.0, Y_BODY - 0.2), r"x_2"),
            leaf_node(at(X_RIGHT - 2.0, Y_BODY + 0.6), r"x_3"),
        )
        p1 = prod_node(at(X_RIGHT - 0.9, Y_BODY - 0.5))
        p2 = prod_node(at(X_RIGHT - 0.9, Y_BODY + 0.3))
        s1 = sum_node(at(X_RIGHT + 0.3, Y_BODY - 0.1))
        out = Dot(at(X_RIGHT + 1.4, Y_BODY - 0.1), color=HIGHLIGHT_COLOR, radius=0.12)
        out_lbl = MathTex(r"y", font_size=22, color=HIGHLIGHT_COLOR).next_to(out, RIGHT, buff=0.06)

        edges = VGroup(
            connect(inputs[0], p1), connect(inputs[1], p1),
            connect(inputs[1], p2), connect(inputs[2], p2),
            connect(p1, s1), connect(p2, s1), connect(s1, out),
        )

        self.play(FadeIn(block), run_time=T_MEDIUM)
        self.play(block.animate.set_opacity(0.18), run_time=T_FAST)
        self.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08),
            LaggedStart(*[GrowFromCenter(n) for n in inputs], lag_ratio=0.12),
            GrowFromCenter(p1), GrowFromCenter(p2), GrowFromCenter(s1),
            GrowFromCenter(out), FadeIn(out_lbl),
            FadeOut(block),
            run_time=T_MEDIUM,
        )

        note_logic = make_note(r"\times\ \text{combine}\quad +\ \text{mix}")
        self.play(FadeIn(note_logic), run_time=T_FAST)
        self.wait(0.8)

        # clear 3A content except title
        to_remove = [m for m in self.mobjects if m is not title]
        self.play(*[FadeOut(m) for m in to_remove], run_time=T_FAST)
        # 3B
        sub_3b = make_sub(r"\text{Depth increases expressivity}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(sub_3b), run_time=T_FAST)

        leaves = VGroup(*[
            leaf_node(at(X_LEFT - 0.6 + i * 0.9, Y_BODY - 1.0), rf"x_{i+1}")
            for i in range(5)
        ])
        prod_l = VGroup(prod_node(at(X_LEFT + 0.2, Y_BODY - 0.2)), prod_node(at(X_LEFT + 1.8, Y_BODY - 0.2)))
        sum_l = VGroup(sum_node(at(X_LEFT + 1.0, Y_BODY + 0.5)))
        prod_top = prod_node(at(X_LEFT + 1.0, Y_BODY + 1.2))
        root = sum_node(at(X_LEFT + 1.0, Y_BODY + 1.9))

        spn_edges = VGroup(
            connect(leaves[0], prod_l[0]), connect(leaves[1], prod_l[0]),
            connect(leaves[2], prod_l[1]), connect(leaves[3], prod_l[1]),
            connect(prod_l[0], sum_l[0]), connect(prod_l[1], sum_l[0]),
            connect(sum_l[0], prod_top), connect(prod_top, root),
        )

        shallow_leaves = VGroup(*[
            leaf_node(at(X_RIGHT - 1.2 + i * 0.55, Y_BODY - 0.8), rf"x_{i+1}")
            for i in range(5)
        ])
        shallow_root = sum_node(at(X_RIGHT, Y_BODY + 0.2))
        shallow_edges = VGroup(*[connect(l, shallow_root) for l in shallow_leaves])

        self.play(
            LaggedStart(*[Create(e) for e in spn_edges], lag_ratio=0.06),
            LaggedStart(*[GrowFromCenter(n) for n in list(leaves) + list(prod_l) + list(sum_l) + [prod_top, root]], lag_ratio=0.08),
            run_time=T_MEDIUM,
        )
        self.play(
            LaggedStart(*[Create(e) for e in shallow_edges], lag_ratio=0.06),
            LaggedStart(*[GrowFromCenter(n) for n in list(shallow_leaves) + [shallow_root]], lag_ratio=0.08),
            run_time=T_MEDIUM,
        )

        deep_lbl = MathTex(r"\text{Deep: compact}", font_size=18, color=HIGHLIGHT_COLOR).move_to(at(X_LEFT + 1.0, Y_NOTE + 0.55))
        shallow_lbl = MathTex(r"\text{Shallow: wide}", font_size=18, color=SUBTITLE_COLOR).move_to(at(X_RIGHT, Y_NOTE + 0.55))
        self.play(FadeIn(deep_lbl), FadeIn(shallow_lbl), run_time=T_FAST)
        self.wait(1.1)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MEDIUM)
