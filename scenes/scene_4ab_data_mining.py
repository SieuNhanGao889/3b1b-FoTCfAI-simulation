"""
scenes/scene_4ab_data_mining.py
SCENE 4A + 4B: Data mining with tensor factorization.
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


class DataMiningAB(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Tensor Factorization for Data Mining}")
        self.play(FadeIn(title), run_time=T_FAST)

        # 4A cocktail-party separation
        sub_4a = make_sub(r"\text{Source separation}")
        self.play(FadeIn(sub_4a), run_time=T_FAST)

        sources = VGroup(
            Dot(at(X_LEFT - 1.1, Y_BODY + 0.8), color=RED_C, radius=0.12),
            Dot(at(X_LEFT - 1.7, Y_BODY + 0.0), color=GREEN_C, radius=0.12),
            Dot(at(X_LEFT - 0.8, Y_BODY - 0.7), color=BLUE_C, radius=0.12),
        )
        waves = VGroup()
        for k, col in enumerate([RED_C, GREEN_C, BLUE_C]):
            w = VMobject(color=col, stroke_width=2)
            pts = [at(X_LEFT - 0.1 + 0.15 * t, Y_BODY + 0.25 * np.sin(0.6 * t + k) + 0.02 * k) for t in range(26)]
            w.set_points_as_corners(pts)
            waves.add(w)

        tensor_mix = Tensor3D(nx=5, ny=4, nz=4, cell_size=0.22, face_color=BLUE_E, edge_color=TENSOR_EDGE_COLOR)
        tensor_mix.move_to(at(X_RIGHT - 1.0, Y_BODY + 0.1))

        prism = Triangle(fill_color="#9fd8ff", fill_opacity=0.30, stroke_color="#9fd8ff", stroke_width=2).scale(0.55)
        prism.move_to(at(X_RIGHT + 1.1, Y_BODY + 0.2))

        in_ray = Line(tensor_mix.get_right(), prism.get_left(), color=WHITE, stroke_width=2)
        out_rays = VGroup(
            Line(prism.get_right(), at(X_RIGHT + 2.7, Y_BODY + 0.8), color=RED_C, stroke_width=2.4),
            Line(prism.get_right(), at(X_RIGHT + 2.7, Y_BODY + 0.2), color=GREEN_C, stroke_width=2.4),
            Line(prism.get_right(), at(X_RIGHT + 2.7, Y_BODY - 0.4), color=BLUE_C, stroke_width=2.4),
        )

        lbl_mix = MathTex(r"\text{Frequency}\times\text{Time}\times\text{Sensor}", font_size=16, color=SUBTITLE_COLOR).next_to(tensor_mix, DOWN, buff=0.12)
        lbl_sep = MathTex(r"\text{A}\quad\text{B}\quad\text{Background}", font_size=16, color=HIGHLIGHT_COLOR).next_to(out_rays, RIGHT, buff=0.10)

        self.play(LaggedStart(*[GrowFromCenter(s) for s in sources], lag_ratio=0.2), run_time=T_MEDIUM)
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.2), run_time=T_MEDIUM)
        self.play(FadeIn(tensor_mix, scale=0.8), FadeIn(lbl_mix), run_time=T_MEDIUM)
        self.play(Create(in_ray), FadeIn(prism), run_time=T_FAST)
        self.play(LaggedStart(*[Create(r) for r in out_rays], lag_ratio=0.2), FadeIn(lbl_sep), run_time=T_MEDIUM)

        note_4a = make_note(r"\text{Blind Source Separation}")
        self.play(FadeIn(note_4a), run_time=T_MEDIUM)
        self.wait(0.7)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in [title]])))

        # 4B nonnegative factorization and completion
        sub_4b = make_sub(r"\text{Nonnegative factors}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(sub_4b), run_time=T_FAST)

        data_block = Tensor3D(nx=5, ny=4, nz=5, cell_size=0.22, face_color="#223344", edge_color=TENSOR_EDGE_COLOR)
        data_block.move_to(at(X_LEFT, Y_BODY + 0.1))
        axes_lbl = MathTex(r"\text{User}\times\text{Product}\times\text{Time}", font_size=16, color=SUBTITLE_COLOR).next_to(data_block, DOWN, buff=0.12)

        missing = VGroup(*[
            Square(side_length=0.22, fill_color="#444444", fill_opacity=0.95, stroke_width=0).move_to(data_block.get_center() + RIGHT * dx + UP * dy)
            for dx, dy in [(0.35, 0.20), (-0.3, -0.1), (0.1, -0.3), (-0.4, 0.25)]
        ])

        self.play(FadeIn(data_block, scale=0.8), FadeIn(axes_lbl), run_time=T_MEDIUM)
        self.play(FadeIn(missing), run_time=T_FAST)

        factors = VGroup(
            Rectangle(width=2.1, height=0.32, fill_color=RED_C, fill_opacity=0.70, stroke_width=0).move_to(at(X_RIGHT, Y_BODY + 0.7)),
            Rectangle(width=2.1, height=0.32, fill_color=BLUE_C, fill_opacity=0.70, stroke_width=0).move_to(at(X_RIGHT, Y_BODY + 0.1)),
            Rectangle(width=2.1, height=0.32, fill_color=YELLOW_C, fill_opacity=0.70, stroke_width=0).move_to(at(X_RIGHT, Y_BODY - 0.5)),
        )
        f_lbls = VGroup(
            MathTex(r"\text{Weekends}", font_size=15, color=RED_C).next_to(factors[0], RIGHT, buff=0.10),
            MathTex(r"\text{Morning}", font_size=15, color=BLUE_C).next_to(factors[1], RIGHT, buff=0.10),
            MathTex(r"\text{Promo}", font_size=15, color=YELLOW_C).next_to(factors[2], RIGHT, buff=0.10),
        )
        nn = MathTex(r"\ge 0", font_size=20, color=HIGHLIGHT_COLOR).move_to(at(X_RIGHT, Y_BODY - 1.1))

        self.play(data_block.animate.set_opacity(0.22), LaggedStart(*[FadeIn(f, shift=LEFT * 0.1) for f in factors], lag_ratio=0.2), run_time=T_MEDIUM)
        self.play(FadeIn(f_lbls), FadeIn(nn), run_time=T_FAST)

        filled = VGroup(*[
            Square(side_length=0.22, fill_color=TENSOR_COLOR, fill_opacity=0.9, stroke_width=0).move_to(m.get_center())
            for m in missing
        ])
        comp = make_note(r"\textbf{Tensor Completion}", color=HIGHLIGHT_COLOR)

        self.play(FadeOut(VGroup(factors, f_lbls, nn)), data_block.animate.set_opacity(0.85), run_time=T_FAST)
        self.play(ReplacementTransform(missing, filled), run_time=T_MEDIUM)
        self.play(FadeIn(comp), run_time=T_MEDIUM)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MEDIUM)
