"""
scenes/scene_1a_point_to_block.py
─────────────────────────────────────────────────────────────────────────────
SCENE 1A  "From a point to a block"  (0:00 – 0:40)

Pedagogical goals (from feedback):
  1. Show that Tensor = multidimensional array that INCLUDES scalars, vectors,
     and matrices as special cases (rank-0, 1, 2).
  2. Explicitly label each order/rank so learners understand the hierarchy.
  3. Transition smoothly into the 3-D block (rank-3 tensor).

Timeline:
  0-5s   Black screen → glowing white dot (scalar, rank 0)
  5-12s  Dot stretches into a row of 5 values (vector, rank 1)
  12-22s Vector replicates into 4 rows → 4×5 matrix (rank 2)
  22-35s Matrix replicates along depth → 6 slices → 4×5×6 tensor (rank 3)
  35-40s Zoom out; X,Y,Z axis labels appear; "Tensor = multidim. array" text
─────────────────────────────────────────────────────────────────────────────
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D


# ── helpers ──────────────────────────────────────────────────────────────────

VALUES = [3, 7, 2, 9, 1]   # sample data values shown in the vector


def make_value_dot(val: int, color=VECTOR_COLOR, font_size: int = 20):
    dot = Circle(radius=0.22, fill_color=color, fill_opacity=0.9, stroke_width=0)
    num = Text(str(val), font_size=font_size, color=BLACK, weight=BOLD)
    return VGroup(dot, num)


def make_vector_row(values, color=VECTOR_COLOR, spacing: float = 0.6):
    row = VGroup(*[make_value_dot(v, color) for v in values])
    row.arrange(RIGHT, buff=spacing - 0.44)
    return row


def rank_label(text: str, color=HIGHLIGHT_COLOR, font_size: int = 28):
    return Text(text, font_size=font_size, color=color, weight=BOLD)


# ── Scene ─────────────────────────────────────────────────────────────────────

class PointToBlock(Scene):

    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── 0-5s  Scalar (rank 0) ─────────────────────────────────────────
        scalar_dot = Dot(ORIGIN, radius=0.18, color=WHITE)
        scalar_dot.set_glow_factor(1.5)
        rlabel = rank_label("Scalar  (rank 0 tensor)")

        self.wait(0.4)
        self.play(GrowFromCenter(scalar_dot), run_time=T_FAST)
        self.play(Flash(scalar_dot, color=WHITE, flash_radius=0.4, line_length=0.15),
                  run_time=0.5)
        rlabel.next_to(scalar_dot, DOWN, buff=0.4)
        self.play(FadeIn(rlabel, shift=UP * 0.1), run_time=T_FAST)
        self.wait(0.8)

        # ── 5-12s  Vector (rank 1) ────────────────────────────────────────
        vec_row = make_vector_row(VALUES)
        vec_row.move_to(ORIGIN)

        v_label_top = rank_label("Vector  (rank-1 tensor)", color=VECTOR_COLOR)
        v_label_top.to_edge(UP, buff=0.3)

        # Scalar "stretches" into the first dot of the vector
        self.play(
            FadeOut(rlabel),
            ReplacementTransform(scalar_dot, vec_row[0]),
            run_time=T_MEDIUM,
        )
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in vec_row[1:]], lag_ratio=0.18),
            FadeIn(v_label_top, shift=DOWN * 0.1),
            run_time=T_MEDIUM,
        )

        # Python index hint: vec[i]
        idx_hint = Text("vec[i]", font="Monospace", font_size=18,
                        color=SUBTITLE_COLOR)
        idx_hint.next_to(vec_row, DOWN, buff=0.2)
        self.play(FadeIn(idx_hint), run_time=T_FAST)
        self.wait(0.6)

        # ── 12-22s  Matrix (rank 2) ───────────────────────────────────────
        rows = VGroup(*[make_vector_row(VALUES, color=MATRIX_COLOR) for _ in range(4)])
        rows.arrange(DOWN, buff=0.18)
        rows.move_to(ORIGIN)

        m_label_top = rank_label("Matrix  (rank-2 tensor)", color=MATRIX_COLOR)
        m_label_top.to_edge(UP, buff=0.3)

        m_idx_hint = Text("mat[i, j]", font="Monospace", font_size=18,
                          color=SUBTITLE_COLOR)
        m_idx_hint.next_to(rows, DOWN, buff=0.2)

        self.play(
            FadeOut(v_label_top), FadeOut(idx_hint),
            # Transform first row into matrix row 0, then grow the rest
            ReplacementTransform(vec_row, rows[0]),
            run_time=T_MEDIUM,
        )
        self.play(
            LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in rows[1:]],
                        lag_ratio=0.25),
            FadeIn(m_label_top, shift=DOWN * 0.1),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(m_idx_hint), run_time=T_FAST)
        self.wait(0.5)

        # ── 22-35s  Tensor rank-3 ─────────────────────────────────────────
        # Fade the 2-D matrix, bring in the 3-D block
        tensor_block = Tensor3D(nx=5, ny=4, nz=6,
                                cell_size=0.32,
                                face_color=TENSOR_COLOR,
                                edge_color=TENSOR_EDGE_COLOR)
        tensor_block.move_to(ORIGIN)

        t_label_top = rank_label("Tensor  (rank ≥ 3)", color=TENSOR_EDGE_COLOR)
        t_label_top.to_edge(UP, buff=0.3)

        t_idx_hint = Text("tensor[i, j, k, ...]", font="Monospace", font_size=18,
                          color=SUBTITLE_COLOR)
        t_idx_hint.next_to(tensor_block, DOWN, buff=0.25)

        self.play(
            FadeOut(m_label_top), FadeOut(m_idx_hint),
            FadeOut(rows),
            run_time=T_FAST,
        )
        self.play(
            FadeIn(tensor_block, shift=UP * 0.1),
            FadeIn(t_label_top, shift=DOWN * 0.1),
            run_time=T_SLOW,
        )
        self.play(FadeIn(t_idx_hint), run_time=T_FAST)

        # Slow rotation effect: shift the block slightly left/right
        self.play(tensor_block.animate.shift(LEFT * 0.15), run_time=0.8,
                  rate_func=there_and_back)
        self.wait(0.4)

        # ── 35-40s  Axis labels + taxonomy summary ────────────────────────
        # Move block slightly left to make room for axis labels
        self.play(tensor_block.animate.shift(LEFT * 0.6), run_time=T_MEDIUM)

        # Axis arrows (isometric directions)
        arrow_x = Arrow(ORIGIN, RIGHT * 1.2, color=RED_B, stroke_width=3,
                        max_tip_length_to_length_ratio=0.18)
        arrow_y = Arrow(ORIGIN, UP * 1.2, color=GREEN_B, stroke_width=3,
                        max_tip_length_to_length_ratio=0.18)
        arrow_z = Arrow(ORIGIN, (LEFT + DOWN) * 0.7, color=BLUE_B, stroke_width=3,
                        max_tip_length_to_length_ratio=0.18)

        ax_origin = tensor_block.get_corner(DL) + RIGHT * 0.1 + UP * 0.05
        for arr in [arrow_x, arrow_y, arrow_z]:
            arr.shift(ax_origin)

        lx = Text("axis 0  (rows)",   font_size=16, color=RED_B).next_to(arrow_x, RIGHT, buff=0.08)
        ly = Text("axis 1  (cols)",   font_size=16, color=GREEN_B).next_to(arrow_y, UP, buff=0.05)
        lz = Text("axis 2  (depth)",  font_size=16, color=BLUE_B).next_to(arrow_z, DL, buff=0.05)

        self.play(
            LaggedStart(
                GrowArrow(arrow_x), GrowArrow(arrow_y), GrowArrow(arrow_z),
                lag_ratio=0.3,
            ),
            run_time=T_MEDIUM,
        )
        self.play(
            FadeIn(lx), FadeIn(ly), FadeIn(lz),
            run_time=T_FAST,
        )

        # ── Taxonomy summary on the right ─────────────────────────────────
        summary_lines = VGroup(
            Text("Multidimensional array:", font_size=18, color=WHITE, weight=BOLD),
            Text("Scalar  = rank 0  (1 number)",        font_size=15, color=SCALAR_COLOR),
            Text("Vector  = rank 1  (list)",             font_size=15, color=VECTOR_COLOR),
            Text("Matrix  = rank 2  (grid)",             font_size=15, color=MATRIX_COLOR),
            Text("Tensor  = rank ≥ 3  (block…)",        font_size=15, color=TENSOR_EDGE_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        summary_lines.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)

        self.play(
            FadeOut(t_label_top), FadeOut(t_idx_hint),
            run_time=T_FAST,
        )
        self.play(
            LaggedStart(*[FadeIn(l, shift=LEFT * 0.1) for l in summary_lines],
                        lag_ratio=0.2),
            run_time=T_SLOW,
        )
        self.wait(1.5)

        # ── Fade out ready for Scene 1B ───────────────────────────────────
        self.play(
            FadeOut(VGroup(tensor_block, arrow_x, arrow_y, arrow_z,
                           lx, ly, lz, summary_lines)),
            run_time=T_MEDIUM,
        )
