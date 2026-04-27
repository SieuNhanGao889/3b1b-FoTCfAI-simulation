"""
scenes/scene_4cd_coupled_cases.py
SCENE 4C + 4D: Coupled factorization and case flashes.
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


class CoupledAndCases(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = make_title(r"\text{Coupled Tensor Factorization}")
        self.play(FadeIn(title), run_time=T_FAST)

        # 4C
        sub_4c = make_sub(r"\text{Shared factors}")
        self.play(FadeIn(sub_4c), run_time=T_FAST)

        t3 = Tensor3D(nx=4, ny=3, nz=4, cell_size=0.24, face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        t3.move_to(at(X_LEFT, Y_BODY + 0.2))
        t_lbl = MathTex(r"\text{User}\times\text{Action}\times\text{Time}", font_size=16, color=SUBTITLE_COLOR).next_to(t3, DOWN, buff=0.10)

        m2 = Rectangle(width=1.9, height=1.3, fill_color=MATRIX_COLOR, fill_opacity=0.45, stroke_color=MATRIX_COLOR, stroke_width=2)
        m2.move_to(at(X_RIGHT, Y_BODY + 0.2))
        m_lbl = MathTex(r"\text{User}\times\text{Demographics}", font_size=16, color=SUBTITLE_COLOR).next_to(m2, DOWN, buff=0.10)

        self.play(FadeIn(t3, scale=0.8), FadeIn(t_lbl), FadeIn(m2), FadeIn(m_lbl), run_time=T_MEDIUM)

        lf_t = Rectangle(width=0.28, height=1.0, fill_color=VECTOR_COLOR, fill_opacity=0.85, stroke_width=0).move_to(at(X_LEFT + 1.4, Y_BODY + 0.4))
        lf_m = Rectangle(width=0.28, height=1.0, fill_color=VECTOR_COLOR, fill_opacity=0.85, stroke_width=0).move_to(at(X_RIGHT - 1.4, Y_BODY + 0.4))
        shared = Line(lf_t.get_right(), lf_m.get_left(), color=HIGHLIGHT_COLOR, stroke_width=3)
        shared_glow = Line(lf_t.get_right(), lf_m.get_left(), color=HIGHLIGHT_COLOR, stroke_width=8, stroke_opacity=0.2)

        self.play(
            ReplacementTransform(t3.copy(), lf_t),
            ReplacementTransform(m2.copy(), lf_m),
            run_time=T_MEDIUM,
        )
        self.play(Create(shared_glow), Create(shared), run_time=T_FAST)

        flow = Dot(lf_t.get_right(), color=HIGHLIGHT_COLOR, radius=0.09)
        self.play(GrowFromCenter(flow), run_time=T_FAST)
        self.play(flow.animate.move_to(lf_m.get_left()), run_time=T_MEDIUM)
        self.play(FadeOut(flow), run_time=T_FAST)

        note_4c = make_note(r"\text{Signal transfers across views}")
        self.play(FadeIn(note_4c), run_time=T_MEDIUM)
        self.wait(0.8)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in [title]])))

        # 4D
        sub_4d = make_sub(r"\text{Case flashes}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(sub_4d), run_time=T_FAST)

        cards = [
            (r"\text{Healthcare}", r"\text{Patient}\times\text{Symptom}\times\text{Time}", r"\text{Hidden disease patterns}", RED_C),
            (r"\text{Social networks}", r"\text{User}\times\text{Hashtag}\times\text{Time}", r"\text{Trends and communities}", BLUE_C),
            (r"\text{Traffic}", r"\text{Location}\times\text{Flow}\times\text{Time}", r"\text{Congestion forecasts}", GREEN_C),
        ]

        for domain, tensor, result, col in cards:
            card = RoundedRectangle(corner_radius=0.18, width=7.6, height=2.4, fill_color="#121224", fill_opacity=1, stroke_color=col, stroke_width=2)
            d = MathTex(domain, font_size=26, color=col).move_to(card.get_center() + UP * 0.55)
            t = MathTex(tensor, font_size=18, color=SUBTITLE_COLOR).move_to(card.get_center() + UP * 0.05)
            r = MathTex(result, font_size=18, color=col).move_to(card.get_center() + DOWN * 0.55)
            grp = VGroup(card, d, t, r).move_to(at(0, Y_BODY - 0.1))

            self.play(FadeIn(grp, shift=UP * 0.10), run_time=T_MEDIUM)
            self.play(Flash(d.get_center(), color=col, flash_radius=0.35, line_length=0.10), run_time=T_FAST)
            self.wait(0.5)
            self.play(FadeOut(grp), run_time=T_FAST)

        close = make_note(r"\textbf{One lens, many domains}", color=HIGHLIGHT_COLOR)
        self.play(FadeIn(close), run_time=T_MEDIUM)
        self.wait(1.0)

        self.play(FadeOut(Group(*[m for m in self.mobjects if m not in [title]])))
