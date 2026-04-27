"""
scenes/scene_2b_cp_decomposition.py
─────────────────────────────────────────────────────────────────────────────
SCENE 2B  "CP Decomposition – Phép phân tách"  (2:10 – 3:20)

- Tensor W tan thành sợi (vectors a, b, c)
- Outer product animation a ∘ b ∘ c → rank-1 block
- R bộ vectors → R rank-1 terms → cộng lại ≈ W
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D


class CPDecomposition(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Original tensor ───────────────────────────────────────────────
        W = Tensor3D(nx=5, ny=4, nz=6, cell_size=0.28,
                     face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        W.shift(LEFT * 3.5)
        W_label = Text("W", font_size=30, color=TENSOR_EDGE_COLOR)
        W_label.next_to(W, UP, buff=0.15)

        self.play(FadeIn(W, scale=0.8), FadeIn(W_label), run_time=T_MEDIUM)

        question = Text("Có cách nào lưu ít hơn không?",
                        font_size=20, color=HIGHLIGHT_COLOR)
        question.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(question), run_time=T_FAST)
        self.wait(0.5)
        self.play(FadeOut(question), run_time=T_FAST)

        # ── Three factor vectors ──────────────────────────────────────────
        vec_height = 1.4
        vec_a = Rectangle(width=0.32, height=vec_height,
                          fill_color=VECTOR_COLOR, fill_opacity=0.9,
                          stroke_color=VECTOR_COLOR, stroke_width=1)
        vec_b = Rectangle(width=vec_height, height=0.32,
                          fill_color=MATRIX_COLOR, fill_opacity=0.9,
                          stroke_color=MATRIX_COLOR, stroke_width=1)
        vec_c = Rectangle(width=0.32, height=0.9,
                          fill_color=TENSOR_EDGE_COLOR, fill_opacity=0.9,
                          stroke_color=TENSOR_EDGE_COLOR, stroke_width=1)

        la = Text("a", font_size=24, color=VECTOR_COLOR)
        lb = Text("b", font_size=24, color=MATRIX_COLOR)
        lc = Text("c", font_size=24, color=TENSOR_EDGE_COLOR)

        vec_a.move_to(RIGHT * 0.3)
        vec_b.move_to(RIGHT * 1.5)
        vec_c.move_to(RIGHT * 2.7)
        for v, l in zip([vec_a, vec_b, vec_c], [la, lb, lc]):
            l.next_to(v, DOWN, buff=0.12)

        factors_grp = VGroup(vec_a, vec_b, vec_c, la, lb, lc)

        vo = Text("Thay vì lưu cả khối, ta chỉ lưu 3 vectors",
                  font_size=18, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.3)

        # W "dissolves" into the factor vectors
        self.play(
            W.animate.set_opacity(0.3),
            run_time=T_MEDIUM,
        )
        self.play(
            LaggedStart(
                ReplacementTransform(W.copy(), vec_a),
                ReplacementTransform(W.copy(), vec_b),
                ReplacementTransform(W.copy(), vec_c),
                lag_ratio=0.3,
            ),
            FadeIn(la), FadeIn(lb), FadeIn(lc),
            FadeIn(vo),
            run_time=T_SLOW,
        )
        self.play(FadeOut(W), FadeOut(W_label), run_time=T_FAST)
        self.wait(0.5)
        self.play(FadeOut(vo), run_time=T_FAST)

        # ── Outer product: a ∘ b → matrix ────────────────────────────────
        op_title = Text("Outer Product: a ∘ b ∘ c", font_size=20,
                        color=HIGHLIGHT_COLOR, weight=BOLD)
        op_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(op_title), run_time=T_FAST)

        # Position vectors for outer product demo
        a_demo = vec_a.copy().set_height(1.6).move_to(LEFT * 3.5 + UP * 0.0)
        b_demo = vec_b.copy().set_width(2.0).move_to(LEFT * 2.0 + UP * 1.2)
        la2 = Text("a", font_size=22, color=VECTOR_COLOR).next_to(a_demo, LEFT, buff=0.1)
        lb2 = Text("b", font_size=22, color=MATRIX_COLOR).next_to(b_demo, UP, buff=0.1)

        self.play(
            factors_grp.animate.shift(RIGHT * 2),
            FadeIn(a_demo), FadeIn(b_demo), FadeIn(la2), FadeIn(lb2),
            run_time=T_MEDIUM,
        )

        # a ∘ b → 2D matrix
        mat_ab = Rectangle(width=2.0, height=1.6,
                           fill_color=BLUE_D, fill_opacity=0.6,
                           stroke_color=BLUE_B, stroke_width=2)
        mat_ab.move_to(LEFT * 2.0 + UP * 0.0)

        self.play(
            a_demo.animate.set_opacity(0.4),
            b_demo.animate.set_opacity(0.4),
            FadeIn(mat_ab, scale=0.8),
            run_time=T_MEDIUM,
        )
        mat_lbl = Text("a ⊗ b", font_size=20,
                          color=BLUE_B).next_to(mat_ab, LEFT, buff=0.1)
        self.play(FadeIn(mat_lbl), run_time=T_FAST)

        # (a∘b) ∘ c → rank-1 3D block
        rank1 = Tensor3D(nx=4, ny=5, nz=3, cell_size=0.22,
                         face_color="#2255aa", edge_color=BLUE_B)
        rank1.move_to(LEFT * 2.0 + DOWN * 0.2)
        c_demo = vec_c.copy().move_to(LEFT * 0.3 + DOWN * 0.0)
        lc2 = Text("c", font_size=22, color=TENSOR_EDGE_COLOR).next_to(c_demo, RIGHT, buff=0.1)

        self.play(FadeIn(c_demo), FadeIn(lc2), run_time=T_FAST)
        self.play(
            ReplacementTransform(VGroup(mat_ab, c_demo), rank1),
            FadeOut(VGroup(mat_lbl, a_demo, b_demo, la2, lb2, lc2)),
            run_time=T_MEDIUM,
        )
        r1_lbl = Text("a ∘ b ∘ c",
                         font_size=20, color=BLUE_B).next_to(rank1, DOWN, buff=0.1)
        self.play(FadeIn(r1_lbl), run_time=T_FAST)
        self.wait(0.5)

        # ── R rank-1 terms ────────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(rank1, r1_lbl, factors_grp, op_title)),
            run_time=T_FAST,
        )

        rank1_colors = [
            ("#1a3a6a", "#4488cc"),
            ("#2a4a1a", "#66aa44"),
            ("#4a2a1a", "#cc6633"),
            ("#3a1a4a", "#9944cc"),
            ("#4a3a1a", "#ccaa22"),
        ]
        R = 5
        rank1_blocks = VGroup()
        for i, (fc, ec) in enumerate(rank1_colors):
            b = Tensor3D(nx=3, ny=4, nz=4, cell_size=0.18,
                         face_color=fc, edge_color=ec)
            b.move_to(LEFT * 3.5 + RIGHT * i * 1.55 + UP * 0.3)
            rank1_blocks.add(b)

        plus_signs = VGroup()
        for i in range(R - 1):
            p = Text("+", font_size=28, color=SUM_NODE_COLOR)
            p.move_to(LEFT * 2.75 + RIGHT * i * 1.55 + UP * 0.3)
            plus_signs.add(p)

        vo2 = Text("Tạo R bộ vectors, mỗi bộ cho một rank-1 block",
                   font_size=18, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.4)

        self.play(
            LaggedStart(*[FadeIn(b, scale=0.7) for b in rank1_blocks], lag_ratio=0.2),
            LaggedStart(*[FadeIn(p) for p in plus_signs], lag_ratio=0.2),
            FadeIn(vo2),
            run_time=T_SLOW,
        )
        self.wait(0.5)

        # ── Sum → approximates W ──────────────────────────────────────────
        self.play(FadeOut(VGroup(rank1_blocks, plus_signs, vo2)), run_time=T_FAST)

        W_approx = Tensor3D(nx=5, ny=4, nz=6, cell_size=0.28,
                            face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        W_approx.move_to(RIGHT * 2.5)

        formula = Text("W ≈ Σ(r=1..R)  aᵣ ∘ bᵣ ∘ cᵣ",
            font_size=28, color=MATH_COLOR,
        ).to_edge(DOWN, buff=0.5)

        approx_sign = Text("≈", font_size=34, color=HIGHLIGHT_COLOR)
        approx_sign.move_to(ORIGIN)

        self.play(
            FadeIn(W_approx, scale=0.8),
            FadeIn(approx_sign),
            Write(formula),
            run_time=T_SLOW,
        )

        cp_label = Text("CP Decomposition", font_size=24,
                        color=HIGHLIGHT_COLOR, weight=BOLD)
        cp_label.to_edge(UP, buff=0.3)
        self.play(FadeIn(cp_label), run_time=T_FAST)
        self.wait(1.2)

        self.play(FadeOut(VGroup(W_approx, approx_sign, formula, cp_label)),
                  run_time=T_MEDIUM)
