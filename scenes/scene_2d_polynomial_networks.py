"""
scenes/scene_2d_polynomial_networks.py
─────────────────────────────────────────────────────────────────────────────
SCENE 2D  "Polynomial Networks"  (4:00 – 5:00)

- x → x⊗x (outer product → matrix) → x⊗x⊗x (rank-3) → rank-4
- Contraction với W → output y
- Decision boundary: linear vs nonlinear
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from config import *
from utils.tensor_objects import Tensor3D


class PolynomialNetworks(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Input vector x ────────────────────────────────────────────────
        x_vec = VGroup(
            *[Text(f"x{i+1}", font="Monospace", font_size=20, color=VECTOR_COLOR)
              for i in range(3)]
        ).arrange(DOWN, buff=0.25)
        bracket_l = Text("[", font_size=60, color=VECTOR_COLOR)
        bracket_r = Text("]", font_size=60, color=VECTOR_COLOR)
        bracket_l.next_to(x_vec, LEFT, buff=0.1)
        bracket_r.next_to(x_vec, RIGHT, buff=0.1)
        x_vec = VGroup(bracket_l, x_vec, bracket_r)
        x_vec.shift(LEFT * 5.5)
        x_lbl = Text("x", font_size=26, color=VECTOR_COLOR)
        x_lbl.next_to(x_vec, UP, buff=0.1)

        self.play(FadeIn(x_vec, scale=0.8), FadeIn(x_lbl), run_time=T_MEDIUM)

        vo = Text("Trong mạng đa thức, input tương tác với chính nó",
                  font_size=18, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(vo), run_time=T_FAST)
        self.wait(0.5)
        self.play(FadeOut(vo), run_time=T_FAST)

        # ── x ⊗ x → matrix ───────────────────────────────────────────────
        mat_xx = Square(side_length=1.2,
                        fill_color=MATRIX_COLOR, fill_opacity=0.55,
                        stroke_color=MATRIX_COLOR, stroke_width=2)
        mat_xx.shift(LEFT * 3.0)
        mat_lbl = Text("x ⊗ x",
                          font_size=22, color=MATRIX_COLOR)
        mat_lbl.next_to(mat_xx, UP, buff=0.1)
        mat_dim = Text("(n × n)", font_size=14,
                       color=SUBTITLE_COLOR).next_to(mat_xx, DOWN, buff=0.08)

        arrow1 = Arrow(x_vec.get_right(), mat_xx.get_left(),
                       color=SUBTITLE_COLOR, stroke_width=2,
                       max_tip_length_to_length_ratio=0.2)
        op1 = Text("⊗", font_size=20,
                      color=PRODUCT_NODE_COLOR).next_to(arrow1, UP, buff=0.05)

        self.play(GrowArrow(arrow1), FadeIn(op1), run_time=T_FAST)
        self.play(FadeIn(mat_xx, scale=0.7), FadeIn(mat_lbl), FadeIn(mat_dim),
                  run_time=T_MEDIUM)

        # ── x ⊗ x ⊗ x → rank-3 block ────────────────────────────────────
        block3 = Tensor3D(nx=3, ny=3, nz=3, cell_size=0.28,
                          face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block3.shift(LEFT * 0.8)
        b3_lbl = Text("x⊗³", font_size=22,
                         color=TENSOR_EDGE_COLOR).next_to(block3, UP, buff=0.1)
        b3_dim = Text("(n × n × n)", font_size=14,
                      color=SUBTITLE_COLOR).next_to(block3, DOWN, buff=0.08)

        arrow2 = Arrow(mat_xx.get_right(), block3.get_left(),
                       color=SUBTITLE_COLOR, stroke_width=2,
                       max_tip_length_to_length_ratio=0.2)
        op2 = Text("⊗ x", font_size=18,
                      color=PRODUCT_NODE_COLOR).next_to(arrow2, UP, buff=0.05)

        self.play(GrowArrow(arrow2), FadeIn(op2), run_time=T_FAST)
        self.play(FadeIn(block3, scale=0.7), FadeIn(b3_lbl), FadeIn(b3_dim),
                  run_time=T_MEDIUM)

        # ── x^⊗4 (represented as stacked blocks) → contraction with W ────
        block4_grp = VGroup()
        for i in range(3):
            b = Tensor3D(nx=3, ny=3, nz=3, cell_size=0.22,
                         face_color="#334466", edge_color="#5577aa")
            b.shift(RIGHT * 1.8 + UP * (i * 0.12) + RIGHT * (i * 0.1))
            block4_grp.add(b)
        b4_lbl = Text("x⊗⁴", font_size=22,
                         color="#5577aa").next_to(block4_grp, UP, buff=0.1)

        arrow3 = Arrow(block3.get_right(), block4_grp.get_left(),
                       color=SUBTITLE_COLOR, stroke_width=2,
                       max_tip_length_to_length_ratio=0.2)
        op3 = Text("⊗ x", font_size=16,
                      color=PRODUCT_NODE_COLOR).next_to(arrow3, UP, buff=0.05)

        self.play(GrowArrow(arrow3), FadeIn(op3), run_time=T_FAST)
        self.play(
            LaggedStart(*[FadeIn(b, scale=0.7) for b in block4_grp], lag_ratio=0.15),
            FadeIn(b4_lbl),
            run_time=T_MEDIUM,
        )

        # W tensor + contraction → scalar y
        W_box = Rectangle(width=1.0, height=0.9,
                          fill_color=PRODUCT_NODE_COLOR, fill_opacity=0.4,
                          stroke_color=PRODUCT_NODE_COLOR, stroke_width=2)
        W_box.shift(RIGHT * 3.6)
        W_lbl2 = Text("W", font_size=20,
                         color=PRODUCT_NODE_COLOR).next_to(W_box, UP, buff=0.08)

        contract_arrow = Arrow(block4_grp.get_right(), W_box.get_left(),
                               color=HIGHLIGHT_COLOR, stroke_width=2,
                               max_tip_length_to_length_ratio=0.2)
        y_dot = Dot(W_box.get_right() + RIGHT * 0.5,
                    color=HIGHLIGHT_COLOR, radius=0.18)
        y_lbl = Text("y", font_size=26,
                     color=HIGHLIGHT_COLOR).next_to(y_dot, UP, buff=0.08)

        self.play(GrowArrow(contract_arrow), FadeIn(W_box), FadeIn(W_lbl2),
                  run_time=T_FAST)
        self.play(GrowFromCenter(y_dot), FadeIn(y_lbl), run_time=T_FAST)

        vo2 = Text("Bắt được mọi tương tác bậc cao giữa các đặc trưng",
                   font_size=17, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(vo2), run_time=T_FAST)
        self.wait(0.7)

        # ── Decision boundary comparison ──────────────────────────────────
        self.play(
            FadeOut(VGroup(x_vec, x_lbl, mat_xx, mat_lbl, mat_dim,
                           block3, b3_lbl, b3_dim, block4_grp, b4_lbl,
                           W_box, W_lbl2, y_dot, y_lbl,
                           arrow1, arrow2, arrow3, op1, op2, op3,
                           contract_arrow, vo2)),
            run_time=T_FAST,
        )

        # Draw two decision boundaries side by side
        ax1 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                   x_length=3.5, y_length=3.5,
                   axis_config={"stroke_color": SUBTITLE_COLOR,
                                "stroke_width": 1.2,
                                "include_tip": False})
        ax1.shift(LEFT * 2.8)

        ax2 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                   x_length=3.5, y_length=3.5,
                   axis_config={"stroke_color": SUBTITLE_COLOR,
                                "stroke_width": 1.2,
                                "include_tip": False})
        ax2.shift(RIGHT * 2.8)

        # Linear boundary
        linear_line = ax1.plot(lambda x: 0.7 * x, color=VECTOR_COLOR,
                               stroke_width=2.5)
        lbl_lin = Text("Linear\n(rank-1)", font_size=16,
                       color=VECTOR_COLOR).next_to(ax1, DOWN, buff=0.15)

        # Nonlinear boundary (circle-ish)
        circle_curve = ax2.plot_parametric_curve(
            lambda t: np.array([2.2 * np.cos(t), 1.6 * np.sin(t) + 0.3, 0]),
            t_range=[0, TAU], color=TENSOR_EDGE_COLOR, stroke_width=2.5,
        )
        lbl_nl = Text("Đa thức\n(rank-4)", font_size=16,
                      color=TENSOR_EDGE_COLOR).next_to(ax2, DOWN, buff=0.15)

        # Scatter dots
        rng = np.random.default_rng(42)
        dots_a = VGroup(*[
            Dot(ax1.c2p(x, y), radius=0.07, color=VECTOR_COLOR, fill_opacity=0.7)
            for x, y in zip(rng.uniform(-2.5, 0.5, 14), rng.uniform(-2.5, 2.5, 14))
        ])
        dots_b = VGroup(*[
            Dot(ax1.c2p(x, y), radius=0.07, color=PRODUCT_NODE_COLOR, fill_opacity=0.7)
            for x, y in zip(rng.uniform(-0.5, 2.5, 14), rng.uniform(-2.5, 2.5, 14))
        ])
        # Nonlinear: inside vs outside a circle
        dots_c = VGroup(*[
            Dot(ax2.c2p(x, y), radius=0.07, color=TENSOR_EDGE_COLOR, fill_opacity=0.7)
            for x, y in zip(rng.uniform(-1.5, 1.5, 10), rng.uniform(-1.0, 1.0, 10))
        ])
        dots_d = VGroup(*[
            Dot(ax2.c2p(x, y), radius=0.07, color=PRODUCT_NODE_COLOR, fill_opacity=0.7)
            for x, y in zip(
                np.concatenate([rng.uniform(-3, -1.8, 5), rng.uniform(1.8, 3, 5)]),
                rng.uniform(-2.5, 2.5, 10),
            )
        ])

        self.play(
            Create(ax1), Create(ax2),
            run_time=T_FAST,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots_a + dots_b + dots_c + dots_d],
                        lag_ratio=0.04),
            run_time=T_MEDIUM,
        )
        self.play(
            Create(linear_line), Create(circle_curve),
            FadeIn(lbl_lin), FadeIn(lbl_nl),
            run_time=T_MEDIUM,
        )

        compare_txt = Text(
            "Tensor bậc cao giúp AI nắm bắt quan hệ phi tuyến",
            font_size=18, color=HIGHLIGHT_COLOR, weight=BOLD,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(compare_txt), run_time=T_FAST)
        self.wait(1.2)

        self.play(FadeOut(VGroup(ax1, ax2, linear_line, circle_curve,
                                 dots_a, dots_b, dots_c, dots_d,
                                 lbl_lin, lbl_nl, compare_txt)),
                  run_time=T_MEDIUM)
