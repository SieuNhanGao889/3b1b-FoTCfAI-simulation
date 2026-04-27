"""
scenes/scene_3c_attention.py
─────────────────────────────────────────────────────────────────────────────
SCENE 3C  "Attention và Polynomial Self-Attention"  (6:30 – 7:45)

- Self-attention: N×N matrix, O(N²) complexity
- Polynomial trick → factorize QK^T → O(N)
- Visual: maze → straight path
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *


class PolynomialAttention(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Standard Self-Attention ───────────────────────────────────────
        title = Text("Standard Self-Attention", font_size=22,
                     color=HIGHLIGHT_COLOR, weight=BOLD).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=T_FAST)

        N = 6
        # Draw N×N attention matrix as a grid
        cell_size = 0.45
        grid = VGroup()
        for i in range(N):
            for j in range(N):
                brightness = 0.15 + 0.7 * abs(i - j) / N * \
                             (1 if (i + j) % 3 != 0 else 0.4)
                rect = Square(side_length=cell_size,
                              fill_color=TENSOR_COLOR,
                              fill_opacity=min(brightness, 0.85),
                              stroke_color=TENSOR_EDGE_COLOR,
                              stroke_width=0.6)
                rect.move_to(
                    RIGHT * (j - N / 2 + 0.5) * cell_size +
                    UP    * (N / 2 - i - 0.5) * cell_size +
                    LEFT  * 0.5
                )
                grid.add(rect)

        grid_label = Text("QKᵀ ∈ ℝᴺˣᴺ",
                             font_size=22, color=MATH_COLOR)
        grid_label.next_to(grid, DOWN, buff=0.15)

        complexity_old = Text("O(N²)", font_size=28,
                                 color="#ff4444").to_edge(RIGHT, buff=1.0).shift(UP * 0.3)
        comp_note = Text("Mỗi từ nhìn mọi từ khác", font_size=16,
                         color=SUBTITLE_COLOR).next_to(complexity_old, DOWN, buff=0.15)

        self.play(
            LaggedStart(*[FadeIn(r, scale=0.8) for r in grid], lag_ratio=0.02),
            run_time=T_SLOW,
        )
        self.play(FadeIn(grid_label), FadeIn(complexity_old), FadeIn(comp_note),
                  run_time=T_FAST)
        self.wait(0.6)

        # Zoom into QK^T formula
        formula_std = Text("Attn(Q,K,V) = softmax( QKᵀ/√d ) V",
            font_size=22, color=MATH_COLOR,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(formula_std), run_time=T_MEDIUM)

        highlight_qkt = SurroundingRectangle(
            formula_std[0][17:21], color=PRODUCT_NODE_COLOR, stroke_width=2, buff=0.05
        )
        self.play(Create(highlight_qkt), run_time=T_FAST)
        self.wait(0.4)

        self.play(FadeOut(VGroup(grid_label, formula_std, highlight_qkt, comp_note)),
                  run_time=T_FAST)

        # ── Polynomial Self-Attention ─────────────────────────────────────
        self.play(
            title.animate.become(
                Text("Polynomial Self-Attention", font_size=22,
                     color=HIGHLIGHT_COLOR, weight=BOLD).to_edge(UP, buff=0.3)
            ),
            run_time=T_FAST,
        )

        # Grid "collapses" into a vector (linear)
        vec_linear = VGroup(*[
            Square(side_length=cell_size,
                   fill_color=MATRIX_COLOR,
                   fill_opacity=0.8,
                   stroke_color=MATRIX_COLOR,
                   stroke_width=0.6).move_to(
                       RIGHT * (-N / 2 + 0.5 + i) * cell_size + LEFT * 0.5)
            for i in range(N)
        ])

        self.play(
            ReplacementTransform(grid, vec_linear),
            run_time=T_SLOW,
        )

        # Show new complexity
        complexity_new = Text("O(N)", font_size=28,
                                 color="#44cc44").to_edge(RIGHT, buff=1.0).shift(UP * 0.3)
        self.play(
            ReplacementTransform(complexity_old, complexity_new),
            run_time=T_MEDIUM,
        )

        formula_poly = Text("Attn*(Q,K,V) = φ(Q)( φ(K)ᵀV )",
            font_size=22, color=MATH_COLOR,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(formula_poly), run_time=T_MEDIUM)

        idea_note = Text(
            "Đổi thứ tự nhân: tính K^TV trước → không cần ma trận N×N",
            font_size=16, color=SUBTITLE_COLOR,
        ).next_to(formula_poly, UP, buff=0.15)
        self.play(FadeIn(idea_note), run_time=T_FAST)
        self.wait(0.5)

        # ── Complexity comparison visual ──────────────────────────────────
        self.play(FadeOut(VGroup(vec_linear, formula_poly, idea_note, complexity_new)),
                  run_time=T_FAST)

        # Before: winding maze path
        maze_pts_before = [
            LEFT * 3.5 + DOWN * 1.0,
            LEFT * 3.5 + UP * 0.5,
            LEFT * 2.0 + UP * 0.5,
            LEFT * 2.0 + DOWN * 0.8,
            LEFT * 0.5 + DOWN * 0.8,
            LEFT * 0.5 + UP * 0.3,
            RIGHT * 1.0 + UP * 0.3,
            RIGHT * 1.0 + DOWN * 1.0,
            RIGHT * 2.5 + DOWN * 1.0,
        ]
        maze = VMobject(color="#ff4444", stroke_width=3)
        maze.set_points_as_corners(maze_pts_before)

        # After: straight line
        straight = Line(LEFT * 3.5, RIGHT * 2.5,
                        color="#44cc44", stroke_width=3)

        maze_lbl = Text("O(N²)", font_size=22,
                        color="#ff4444").next_to(maze, DOWN, buff=0.2)
        straight_lbl = Text("O(N)", font_size=22,
                            color="#44cc44").next_to(straight, DOWN, buff=0.2)

        maze.shift(UP * 0.5)
        straight.shift(DOWN * 0.8)
        maze_lbl.shift(UP * 0.5)

        self.play(Create(maze), FadeIn(maze_lbl), run_time=T_SLOW)
        self.play(Create(straight), FadeIn(straight_lbl), run_time=T_MEDIUM)

        result = Text("Từ O(N²) xuống O(N)  –  xử lý chuỗi dài gấp 1000 lần!",
                      font_size=18, color=HIGHLIGHT_COLOR, weight=BOLD)
        result.to_edge(DOWN, buff=0.35)
        self.play(Write(result), run_time=T_MEDIUM)
        self.wait(1.2)

        self.play(FadeOut(VGroup(maze, straight, maze_lbl, straight_lbl,
                                 result, title)),
                  run_time=T_MEDIUM)
