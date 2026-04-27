"""
scenes/scene_4cd_coupled_cases.py
─────────────────────────────────────────────────────────────────────────────
SCENE 4C  "Coupled Tensor Factorization"  (10:00 – 10:45)
SCENE 4D  "Case Studies Flash"            (10:45 – 11:30)
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from config import *
from utils.tensor_objects import Tensor3D


class CoupledAndCases(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ════════════════════════════════════════════════════════════════
        # SCENE 4C – Coupled Factorization
        # ════════════════════════════════════════════════════════════════

        title = Text("Coupled Tensor Factorization",
                     font_size=22, color=HIGHLIGHT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=T_FAST)

        # Two data sources
        tensor_src = Tensor3D(nx=4, ny=3, nz=4, cell_size=0.28,
                              face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        tensor_src.shift(LEFT * 4.0)
        t_lbl = VGroup(
            Text("Tensor (3D)", font_size=15, color=TENSOR_EDGE_COLOR, weight=BOLD),
            Text("User × Action × Time", font_size=13, color=SUBTITLE_COLOR),
        ).arrange(DOWN, buff=0.05).next_to(tensor_src, DOWN, buff=0.12)

        mat_src = Rectangle(width=1.8, height=1.2,
                            fill_color=MATRIX_COLOR, fill_opacity=0.55,
                            stroke_color=MATRIX_COLOR, stroke_width=2)
        mat_src.shift(RIGHT * 4.0)
        m_lbl = VGroup(
            Text("Matrix (2D)", font_size=15, color=MATRIX_COLOR, weight=BOLD),
            Text("User × Demographics", font_size=13, color=SUBTITLE_COLOR),
        ).arrange(DOWN, buff=0.05).next_to(mat_src, DOWN, buff=0.12)

        vo1 = Text("Nhiều nguồn dữ liệu về cùng một đối tượng",
                   font_size=17, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(tensor_src, scale=0.7), FadeIn(t_lbl),
            FadeIn(mat_src, scale=0.7), FadeIn(m_lbl),
            FadeIn(vo1),
            run_time=T_MEDIUM,
        )
        self.wait(0.6)
        self.play(FadeOut(vo1), run_time=T_FAST)

        # Factor vectors from each source
        fac_t1 = Rectangle(width=0.28, height=1.0,
                           fill_color=VECTOR_COLOR, fill_opacity=0.9,
                           stroke_width=0).shift(LEFT * 2.2 + UP * 0.3)
        fac_t2 = Rectangle(width=1.0, height=0.28,
                           fill_color=VECTOR_COLOR, fill_opacity=0.7,
                           stroke_width=0).shift(LEFT * 2.2 + DOWN * 0.4)

        fac_m1 = Rectangle(width=0.28, height=0.9,
                           fill_color=VECTOR_COLOR, fill_opacity=0.9,
                           stroke_width=0).shift(RIGHT * 2.2 + UP * 0.3)
        fac_m2 = Rectangle(width=1.0, height=0.28,
                           fill_color=MATRIX_COLOR, fill_opacity=0.7,
                           stroke_width=0).shift(RIGHT * 2.2 + DOWN * 0.4)

        self.play(
            LaggedStart(
                ReplacementTransform(tensor_src.copy(), fac_t1),
                ReplacementTransform(tensor_src.copy(), fac_t2),
                ReplacementTransform(mat_src.copy(), fac_m1),
                ReplacementTransform(mat_src.copy(), fac_m2),
                lag_ratio=0.2,
            ),
            run_time=T_SLOW,
        )

        # Shared factors connected by glowing line
        shared_line = Line(fac_t1.get_right(), fac_m1.get_left(),
                           color=HIGHLIGHT_COLOR, stroke_width=3)
        shared_glow = Line(fac_t1.get_right(), fac_m1.get_left(),
                           color=HIGHLIGHT_COLOR, stroke_width=7,
                           stroke_opacity=0.25)
        shared_lbl = Text("Shared factor\n(User)", font_size=13,
                          color=HIGHLIGHT_COLOR, line_spacing=0.35)
        shared_lbl.next_to(shared_line, UP, buff=0.08)

        self.play(
            Create(shared_glow), Create(shared_line),
            FadeIn(shared_lbl),
            run_time=T_MEDIUM,
        )

        # Info flow animation
        flow = Dot(fac_t1.get_right(), color=HIGHLIGHT_COLOR, radius=0.1)
        self.play(GrowFromCenter(flow), run_time=T_FAST)
        self.play(flow.animate.move_to(fac_m1.get_left()), run_time=T_MEDIUM,
                  rate_func=smooth)
        self.play(FadeOut(flow), run_time=T_FAST)

        insight = Text(
            "Kết hợp đa nguồn → hiểu người dùng sâu hơn\n"
            "vừa qua hành vi, vừa qua đặc điểm cá nhân",
            font_size=16, color=SUBTITLE_COLOR, line_spacing=0.45,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(insight), run_time=T_FAST)
        self.wait(1.0)

        self.play(FadeOut(VGroup(
            tensor_src, t_lbl, mat_src, m_lbl,
            fac_t1, fac_t2, fac_m1, fac_m2,
            shared_line, shared_glow, shared_lbl,
            insight, title,
        )), run_time=T_MEDIUM)

        # ════════════════════════════════════════════════════════════════
        # SCENE 4D – Case Studies Flash
        # ════════════════════════════════════════════════════════════════

        title2 = Text("Tensor trong thực tế",
                      font_size=22, color=HIGHLIGHT_COLOR, weight=BOLD)
        title2.to_edge(UP, buff=0.3)
        self.play(FadeIn(title2), run_time=T_FAST)

        cases = [
            {
                "icon": "🏥",
                "domain": "Y tế",
                "tensor": "Patient × Symptom × Time",
                "result": "Phát hiện bệnh lý ẩn từ hồ sơ điện tử",
                "color": "#ff8888",
                "dot_color": "#ff4444",
            },
            {
                "icon": "📱",
                "domain": "Mạng xã hội",
                "tensor": "User × Hashtag × Time",
                "result": "Phát hiện xu hướng & cộng đồng",
                "color": "#88aaff",
                "dot_color": "#4466ff",
            },
            {
                "icon": "🚗",
                "domain": "Giao thông",
                "tensor": "Location × Traffic × Time",
                "result": "Dự báo tắc đường thời gian thực",
                "color": "#88ffaa",
                "dot_color": "#22cc66",
            },
        ]

        for case in cases:
            card = self._case_card(case)
            card.move_to(ORIGIN + DOWN * 0.2)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=T_MEDIUM)

            # Animate a "detection" highlight dot on the tensor label
            dot = Dot(color=case["dot_color"], radius=0.12)
            dot.move_to(card.get_center() + UP * 0.15)
            self.play(
                Flash(dot, color=case["dot_color"],
                      flash_radius=0.35, line_length=0.12),
                run_time=T_FAST,
            )
            self.wait(0.9)
            self.play(FadeOut(card), run_time=T_FAST)

        close_txt = Text(
            "Từ y tế, mạng xã hội đến giao thông –\n"
            "Tensor giúp ta hiểu mọi dữ liệu đa chiều!",
            font_size=19, color=HIGHLIGHT_COLOR, weight=BOLD,
            line_spacing=0.5,
        ).move_to(DOWN * 0.2)
        self.play(Write(close_txt), run_time=T_SLOW)
        self.wait(1.2)

        self.play(FadeOut(VGroup(close_txt, title2)), run_time=T_MEDIUM)

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _case_card(data: dict) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.2, width=7.5, height=2.6,
            fill_color="#111122", fill_opacity=1,
            stroke_color=data["color"], stroke_width=2,
        )
        icon = Text(data["icon"], font_size=48).move_to(bg.get_left() + RIGHT * 0.9)
        domain = Text(data["domain"], font_size=22,
                      color=data["color"], weight=BOLD)
        tensor_lbl = Text(data["tensor"], font_size=16, color=SUBTITLE_COLOR)
        result_lbl = Text(data["result"], font_size=17,
                          color=data["color"])
        content = VGroup(domain, tensor_lbl, result_lbl).arrange(DOWN, buff=0.16,
                                                                  aligned_edge=LEFT)
        content.next_to(icon, RIGHT, buff=0.35)
        return VGroup(bg, icon, content)
