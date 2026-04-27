"""
scenes/scene_2c_lora.py
─────────────────────────────────────────────────────────────────────────────
SCENE 2C  "LoRA – Low-Rank Adaptation"  (3:20 – 4:00)

- Ma trận W 4096×4096 = 16M params
- Phân tách thành A (r×4096) và B (4096×r) với r=8
- So sánh: 16M vs 65K → giảm 256 lần
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *


class LoRAScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── LLM icon + big W ──────────────────────────────────────────────
        llm_box = RoundedRectangle(corner_radius=0.25, width=1.8, height=1.8,
                                   fill_color="#1a1a3a", fill_opacity=1,
                                   stroke_color="#8888ff", stroke_width=2)
        llm_txt = Text("LLM", font_size=22, color="#8888ff", weight=BOLD)
        llm_grp = VGroup(llm_box, llm_txt).shift(LEFT * 5.0)

        W_big = Rectangle(width=2.6, height=2.6,
                          fill_color="#223355", fill_opacity=0.8,
                          stroke_color=TENSOR_EDGE_COLOR, stroke_width=2)
        W_big.shift(LEFT * 2.0)
        W_label = Text("W", font_size=28,
                          color=TENSOR_EDGE_COLOR).next_to(W_big, UP, buff=0.12)
        W_size  = Text("4096 × 4096", font_size=15,
                       color=SUBTITLE_COLOR).next_to(W_big, DOWN, buff=0.1)
        W_params = Text("= 16,777,216 params", font_size=14,
                        color="#ff5555").next_to(W_size, DOWN, buff=0.06)

        self.play(FadeIn(llm_grp, scale=0.8), run_time=T_FAST)
        self.play(FadeIn(W_big), FadeIn(W_label), FadeIn(W_size), run_time=T_MEDIUM)
        self.play(FadeIn(W_params), run_time=T_FAST)
        self.wait(0.5)

        # ── Shatter W into A and B ────────────────────────────────────────
        mat_A = Rectangle(width=0.3, height=2.6,
                          fill_color=VECTOR_COLOR, fill_opacity=0.85,
                          stroke_color=VECTOR_COLOR, stroke_width=1)
        mat_B = Rectangle(width=2.6, height=0.3,
                          fill_color=MATRIX_COLOR, fill_opacity=0.85,
                          stroke_color=MATRIX_COLOR, stroke_width=1)

        mat_A.move_to(RIGHT * 1.5)
        mat_B.move_to(RIGHT * 3.5)

        lA = Text("A", font_size=24, color=VECTOR_COLOR)
        lB = Text("B", font_size=24, color=MATRIX_COLOR)
        lA.next_to(mat_A, UP, buff=0.1)
        lB.next_to(mat_B, UP, buff=0.1)

        sA = Text("r × 4096", font_size=13, color=SUBTITLE_COLOR).next_to(mat_A, DOWN, buff=0.08)
        sB = Text("4096 × r", font_size=13, color=SUBTITLE_COLOR).next_to(mat_B, DOWN, buff=0.08)

        times = Text("×", font_size=28, color=PRODUCT_NODE_COLOR)
        times.move_to(RIGHT * 2.5)

        r_label = Text("r = 8  (rank)", font_size=16,
                       color=HIGHLIGHT_COLOR).to_edge(UP, buff=0.3)

        self.play(
            W_big.animate.set_opacity(0.2),
            FadeOut(W_label), FadeOut(W_size), FadeOut(W_params),
            run_time=T_FAST,
        )
        self.play(
            ReplacementTransform(W_big, mat_A),
            run_time=T_MEDIUM,
        )
        self.play(
            FadeIn(mat_B), FadeIn(times),
            FadeIn(lA), FadeIn(lB),
            FadeIn(sA), FadeIn(sB),
            FadeIn(r_label),
            run_time=T_MEDIUM,
        )
        self.wait(0.4)

        # ── Param comparison bar chart ────────────────────────────────────
        bar_old = Rectangle(width=4.5, height=0.5,
                            fill_color="#ff4444", fill_opacity=0.85,
                            stroke_width=0)
        bar_new = Rectangle(width=4.5 / 256, height=0.5,
                            fill_color="#44cc44", fill_opacity=0.85,
                            stroke_width=0)
        bar_old.to_edge(DOWN, buff=1.1).align_to(LEFT * 0.2, LEFT)
        bar_new.next_to(bar_old, DOWN, buff=0.18).align_to(bar_old, LEFT)

        lold = Text("16,777,216  (cũ)", font_size=14,
                    color="#ff4444").next_to(bar_old, RIGHT, buff=0.12)
        lnew = Text("65,536  (LoRA)", font_size=14,
                    color="#44cc44").next_to(bar_new, RIGHT, buff=0.12)

        self.play(
            GrowFromEdge(bar_old, LEFT),
            FadeIn(lold),
            run_time=T_MEDIUM,
        )
        self.play(
            GrowFromEdge(bar_new, LEFT),
            FadeIn(lnew),
            run_time=T_MEDIUM,
        )

        reduction = Text("Giảm 256 lần! 🎉", font_size=26,
                         color=HIGHLIGHT_COLOR, weight=BOLD)
        reduction.next_to(bar_new, DOWN, buff=0.22)
        self.play(Write(reduction), run_time=T_MEDIUM)

        note = Text("Fine-tune mô hình chỉ bằng laptop thường",
                    font_size=17, color=SUBTITLE_COLOR)
        note.next_to(reduction, DOWN, buff=0.15)
        self.play(FadeIn(note), run_time=T_FAST)
        self.wait(1.2)

        self.play(FadeOut(VGroup(
            llm_grp, mat_A, mat_B, lA, lB, sA, sB, times, r_label,
            bar_old, bar_new, lold, lnew, reduction, note,
        )), run_time=T_MEDIUM)
