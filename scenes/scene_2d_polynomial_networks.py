"""
scenes/scene_2d_polynomial_networks.py
────────────────────────────────────────────────────────────────────────────
SCENE 2D: Polynomial Networks — When AI Multiplies Itself   (4:00 – 5:00, ≈ 60s)

STORY ARC (Show Don't Tell):
  Beat 1  [0–15s]  SELF-INTERACTION — Input vector x meets itself (x ⊗ x).
                   A single vertical bar (x) clones and rotates horizontal.
                   They "weave" together via outer product → a 2D dot grid (matrix).
                   The geometry shows WHY it's n² entries: every pair (i,j) interacts.

  Beat 2  [15–30s] CLIMBING ORDERS — x⊗x meets x again → 3D dot-stack.
                   x⊗x⊗x meets x again → 4th-order hypercube (shown as 4-layer stack).
                   Each new interaction multiplies the grid: width × height × depth × …

  Beat 3  [30–45s] CONTRACTION — The 4th-order dot-stack contracts with weight W⁴
                   (another dot block, dim-matched). They slide together, fuse → single
                   glowing dot y. The formula y = ⟨W, x⊗x⊗x⊗x⟩ appears AFTER the picture.

  Beat 4  [45–60s] PAYOFF — Side-by-side decision boundaries.
                   LEFT: a straight line cleaving 2D scatter → linear, misses clusters.
                   RIGHT: a rich closed curve wrapping tightly → polynomial, gets them all.
                   No bar charts — the geometry IS the argument.

Design principles:
  • All tensors/matrices are VGroup of Dots (dot_field) or stacked Rectangle layers.
  • The outer product is shown as the literal crossing of row and column index bars.
  • Animation direction conveys meaning: grow → weave → stack → contract → explode.
"""

from manim import *

# ── Palette ───────────────────────────────────────────────────────────────────
BG_COLOR        = "#0d0d0d"
HIGHLIGHT_COLOR = YELLOW
SUBTITLE_COLOR  = GREY_B

VECTOR_COLOR    = "#F5A623"   # warm amber (x)
MATRIX_COLOR    = "#4CAF50"   # green (x⊗x)
TENSOR_COLOR    = "#2196F3"   # blue  (x⊗x⊗x)
ORDER4_COLOR    = "#9C27B0"   # purple (x⊗4)
WEIGHT_COLOR    = "#FF5722"   # deep orange (W)

# ── Layout ────────────────────────────────────────────────────────────────────
Y_TITLE =  3.30
Y_SUB   =  2.65
Y_BODY  =  0.10
Y_NOTE  = -3.10
X_LEFT  = -4.20
X_RIGHT =  3.50

def at(x, y):
    return np.array([x, y, 0])

def tx(s, sz=28, col=WHITE):
    return MathTex(s, font_size=sz, color=col)

def words(s, sz=26, col=WHITE):
    return Text(s, font_size=sz, color=col)


# ── Visual helpers ────────────────────────────────────────────────────────────

def dot_field(rows, cols, dot_r, col, alpha, h_gap, v_gap):
    """VGroup of Dots — 1a-style tensor visualisation (no Cube)."""
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=dot_r, color=col, fill_opacity=alpha)
            d.move_to(RIGHT * c * h_gap + DOWN * r * v_gap)
            g.add(d)
    return g


def stacked_grids(n_layers, rows, cols, dot_r, col_list, alpha,
                  h_gap, v_gap, layer_offset_x=0.18, layer_offset_y=0.15):
    """
    Returns a VGroup of *n_layers* dot-field grids stacked in a 3-D-looking
    offset pattern (right + up per layer), giving the 'tensor depth' effect
    without using Cube.
    """
    layers = VGroup()
    for i in range(n_layers):
        col = col_list[min(i, len(col_list) - 1)]
        grid = dot_field(rows, cols, dot_r, col, alpha - i * 0.06,
                         h_gap, v_gap)
        grid.shift(RIGHT * i * layer_offset_x + UP * i * layer_offset_y)
        layers.add(grid)
    return layers


# ══════════════════════════════════════════════════════════════════════════════
class PolynomialNetworks(Scene):
# ══════════════════════════════════════════════════════════════════════════════
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Fixed title ───────────────────────────────────────────────────────
        title = words("Polynomial Networks: Self-interaction", 34, HIGHLIGHT_COLOR)
        title.move_to(at(0, Y_TITLE))
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 1: x → x ⊗ x
        # Show a vertical dot-bar (x), clone it horizontally, weave outer product
        # ════════════════════════════════════════════════════════════════════
        sub_1 = tx(r"\mathbf{x}\ \otimes\ \mathbf{x}\ =\ \text{all pairs }(i,j)\text{ interact}", 26, SUBTITLE_COLOR)
        sub_1.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_1), run_time=0.5)

        # Vertical bar: x   (n=7 dots column)
        x_col = dot_field(7, 1, 0.09, VECTOR_COLOR, 0.95, 0.0, 0.32)
        x_col.move_to(at(X_LEFT + 0.3, Y_BODY))
        x_col_lbl = tx(r"\mathbf{x}", 30, VECTOR_COLOR).next_to(x_col, LEFT, buff=0.2)

        self.play(FadeIn(x_col), FadeIn(x_col_lbl), run_time=0.6)

        # Horizontal bar: x  (1×n dots row — clone, rotated)
        x_row = dot_field(1, 7, 0.09, VECTOR_COLOR, 0.95, 0.32, 0.0)
        x_row.move_to(at(X_LEFT + 1.5, Y_BODY + 1.5))
        x_row_lbl = tx(r"\mathbf{x}^\top", 26, VECTOR_COLOR).next_to(x_row, UP, buff=0.15)

        self.play(TransformFromCopy(x_col, x_row), FadeIn(x_row_lbl), run_time=0.8)

        # Outer product symbol
        otimes_1 = tx(r"\otimes", 36, WEIGHT_COLOR).move_to(at(X_LEFT + 0.85, Y_BODY + 0.7))
        self.play(Write(otimes_1), run_time=0.4)

        # The 7×7 dot matrix (x ⊗ x)
        mat_xx = dot_field(7, 7, 0.07, MATRIX_COLOR, 0.85, 0.28, 0.28)
        mat_xx.move_to(at(X_LEFT + 1.6, Y_BODY - 0.1))
        mat_lbl = tx(r"\mathbf{x}\otimes\mathbf{x}", 22, MATRIX_COLOR).next_to(mat_xx, DOWN, buff=0.18)

        # Weave animation: col & row converge into matrix
        self.play(
            FadeOut(otimes_1),
            TransformFromCopy(VGroup(x_col, x_row), mat_xx),
            FadeIn(mat_lbl),
            run_time=1.1,
        )
        self.wait(0.5)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 2: x⊗x → x⊗x⊗x → x⊗4
        # Each step: new x bar meets the previous object → stacked deeper
        # ════════════════════════════════════════════════════════════════════
        sub_2 = words("Adding dimensions: 3rd, 4th order, \ldots", 26, SUBTITLE_COLOR)
        sub_2.move_to(at(0, Y_SUB))
        self.play(ReplacementTransform(sub_1, sub_2), run_time=0.5)

        # 3-layer stack for x⊗x⊗x (3D tensor represented as stacked grids)
        BLUE_SHADES = [BLUE_E, BLUE_D, BLUE_C]
        tensor3 = stacked_grids(
            n_layers=3, rows=6, cols=6,
            dot_r=0.065, col_list=BLUE_SHADES,
            alpha=0.85, h_gap=0.24, v_gap=0.24,
            layer_offset_x=0.20, layer_offset_y=0.18,
        )
        tensor3.move_to(at(0.8, Y_BODY + 0.2))
        t3_lbl = tx(r"\mathbf{x}^{\otimes 3}", 24, BLUE_C).next_to(tensor3, DOWN, buff=0.24)

        otimes_2 = tx(r"\otimes\,\mathbf{x}", 26, WEIGHT_COLOR)
        otimes_2.move_to(at(X_LEFT + 3.0, Y_BODY))
        arr_2 = Arrow(mat_xx.get_right(), tensor3.get_left(), buff=0.18,
                      color=SUBTITLE_COLOR, stroke_width=2)

        self.play(GrowArrow(arr_2), FadeIn(otimes_2), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(layer, scale=0.85) for layer in tensor3], lag_ratio=0.18),
            FadeIn(t3_lbl),
            run_time=1.0,
        )
        self.wait(0.3)

        # 4-layer stack for x⊗4
        PURPLE_SHADES = ["#6A0DAD", "#7B2FBE", "#9C27B0", "#BA68C8"]
        tensor4 = stacked_grids(
            n_layers=4, rows=5, cols=5,
            dot_r=0.060, col_list=PURPLE_SHADES,
            alpha=0.88, h_gap=0.22, v_gap=0.22,
            layer_offset_x=0.19, layer_offset_y=0.16,
        )
        tensor4.move_to(at(X_RIGHT - 0.3, Y_BODY + 0.3))
        t4_lbl = tx(r"\mathbf{x}^{\otimes 4}", 24, ORDER4_COLOR).next_to(tensor4, DOWN, buff=0.24)

        arr_3 = Arrow(tensor3.get_right(), tensor4.get_left(), buff=0.18,
                      color=SUBTITLE_COLOR, stroke_width=2)
        otimes_3 = tx(r"\otimes\,\mathbf{x}", 26, WEIGHT_COLOR).next_to(arr_3, UP, buff=0.08)

        self.play(GrowArrow(arr_3), FadeIn(otimes_3), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(layer, scale=0.85) for layer in tensor4], lag_ratio=0.15),
            FadeIn(t4_lbl),
            run_time=1.0,
        )
        self.wait(0.5)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 3: CONTRACTION with W⁴ → scalar y
        # ════════════════════════════════════════════════════════════════════
        sub_3 = tx(r"\langle\mathcal{W},\,\mathbf{x}^{\otimes 4}\rangle = y", 30, HIGHLIGHT_COLOR)
        sub_3.move_to(at(0, Y_SUB))
        self.play(
            FadeOut(VGroup(x_col, x_col_lbl, x_row, x_row_lbl,
                           mat_xx, mat_lbl, arr_2, arr_3, otimes_2, otimes_3,
                           tensor3, t3_lbl, tensor4, t4_lbl, sub_2)),
            run_time=0.6,
        )

        # Weight tensor W — 4-layer stack, orange/red, placed left
        WEIGHT_SHADES = ["#BF360C", "#E64A19", "#FF5722", "#FF8A65"]
        W_block = stacked_grids(
            n_layers=4, rows=5, cols=5,
            dot_r=0.060, col_list=WEIGHT_SHADES,
            alpha=0.88, h_gap=0.22, v_gap=0.22,
            layer_offset_x=0.19, layer_offset_y=0.16,
        )
        W_block.move_to(at(-2.8, Y_BODY + 0.3))
        W_block_lbl = tx(r"\mathcal{W}^{(4)}", 26, WEIGHT_COLOR).next_to(W_block, DOWN, buff=0.22)

        # x⊗4 — purple — placed right
        tensor4b = stacked_grids(
            n_layers=4, rows=5, cols=5,
            dot_r=0.060, col_list=PURPLE_SHADES,
            alpha=0.88, h_gap=0.22, v_gap=0.22,
            layer_offset_x=0.19, layer_offset_y=0.16,
        )
        tensor4b.move_to(at(2.8, Y_BODY + 0.3))
        t4b_lbl = tx(r"\mathbf{x}^{\otimes 4}", 26, ORDER4_COLOR).next_to(tensor4b, DOWN, buff=0.22)

        inner_lbl = tx(r"\langle\ \cdot\ ,\ \cdot\ \rangle", 30, SUBTITLE_COLOR)
        inner_lbl.move_to(at(0, Y_BODY + 0.4))

        self.play(
            LaggedStart(*[FadeIn(l, scale=0.85) for l in W_block], lag_ratio=0.12),
            LaggedStart(*[FadeIn(l, scale=0.85) for l in tensor4b], lag_ratio=0.12),
            FadeIn(W_block_lbl), FadeIn(t4b_lbl),
            run_time=0.9,
        )
        self.play(Write(inner_lbl), run_time=0.4)

        # Contraction animation: both blocks slide to center, shrink, fuse into dot
        y_dot = Dot(at(0, Y_BODY + 0.4), color=HIGHLIGHT_COLOR, radius=0.22)
        y_lbl = tx(r"y", 38, HIGHLIGHT_COLOR).next_to(y_dot, UP, buff=0.12)

        self.play(
            W_block.animate.move_to(at(0, Y_BODY + 0.4)).scale(0.08).set_opacity(0.0),
            tensor4b.animate.move_to(at(0, Y_BODY + 0.4)).scale(0.08).set_opacity(0.0),
            FadeOut(VGroup(W_block_lbl, t4b_lbl, inner_lbl)),
            run_time=1.3,
        )
        self.play(GrowFromCenter(y_dot), FadeIn(y_lbl), run_time=0.5)
        self.play(Flash(y_dot, color=HIGHLIGHT_COLOR, line_length=0.5, num_lines=12))

        self.play(Write(sub_3), run_time=0.8)

        note = words("All higher-order interactions are captured!", 22, SUBTITLE_COLOR)
        note.move_to(at(0, Y_NOTE + 0.5))
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(W_block, tensor4b, y_dot, y_lbl, note, sub_3)),
            run_time=0.5,
        )

        # ════════════════════════════════════════════════════════════════════
        # BEAT 4: PAYOFF — Linear vs Polynomial decision boundary
        # LEFT: straight-line separator (misses non-linear clusters)
        # RIGHT: closed polynomial curve (captures the clusters perfectly)
        # ════════════════════════════════════════════════════════════════════
        sub_4 = words("Decision boundary: linear vs. polynomial", 26, SUBTITLE_COLOR)
        sub_4.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_4), run_time=0.5)

        ax_L = Axes(
            x_range=[-3, 3], y_range=[-3, 3], x_length=4.2, y_length=4.2,
            axis_config={"stroke_color": GREY_D, "include_tip": False,
                         "stroke_width": 1.2},
        ).move_to(at(-2.8, Y_BODY - 0.2))

        ax_R = Axes(
            x_range=[-3, 3], y_range=[-3, 3], x_length=4.2, y_length=4.2,
            axis_config={"stroke_color": GREY_D, "include_tip": False,
                         "stroke_width": 1.2},
        ).move_to(at(3.0, Y_BODY - 0.2))

        # Scatter points: concentric ring pattern (impossible for a line to separate)
        np.random.seed(21)
        inner_pts = np.column_stack([
            np.random.uniform(-1.0, 1.0, 22),
            np.random.uniform(-1.0, 1.0, 22),
        ])
        outer_angles = np.random.uniform(0, 2 * np.pi, 28)
        outer_r = np.random.uniform(1.7, 2.8, 28)
        outer_pts = np.column_stack([outer_r * np.cos(outer_angles),
                                     outer_r * np.sin(outer_angles)])

        dots_in_L  = VGroup(*[Dot(ax_L.c2p(p[0], p[1]), radius=0.07, color=BLUE_B)
                               for p in inner_pts])
        dots_out_L = VGroup(*[Dot(ax_L.c2p(p[0], p[1]), radius=0.07, color=RED_C)
                               for p in outer_pts])
        dots_in_R  = VGroup(*[Dot(ax_R.c2p(p[0], p[1]), radius=0.07, color=BLUE_B)
                               for p in inner_pts])
        dots_out_R = VGroup(*[Dot(ax_R.c2p(p[0], p[1]), radius=0.07, color=RED_C)
                               for p in outer_pts])

        # Left: straight line (fails)
        linear_sep = ax_L.plot(lambda x: 0.5 * x - 0.1,
                               color=VECTOR_COLOR, stroke_width=2.5)
        lin_lbl = words("Linear", 20, VECTOR_COLOR).next_to(ax_L, DOWN, buff=0.18)

        # Right: elliptical polynomial boundary (succeeds)
        poly_bound = ax_R.plot_parametric_curve(
            lambda t: np.array([2.0 * np.cos(t), 1.55 * np.sin(t) + 0.05, 0]),
            t_range=[0, TAU],
            color=HIGHLIGHT_COLOR, stroke_width=2.8,
        )
        poly_lbl = words("Polynomial (Tensor)", 20, HIGHLIGHT_COLOR).next_to(ax_R, DOWN, buff=0.18)

        self.play(
            Create(ax_L), Create(ax_R),
            *[FadeIn(d) for d in list(dots_in_L) + list(dots_out_L)
              + list(dots_in_R) + list(dots_out_R)],
            run_time=0.9,
        )
        self.play(Create(linear_sep), FadeIn(lin_lbl), run_time=0.9)
        self.play(Create(poly_bound), FadeIn(poly_lbl), run_time=1.3)

        # Highlight wrong classifications on the left
        wrong_boxes = VGroup(*[
            SurroundingRectangle(d, color=RED_C, buff=0.04, stroke_width=1.0)
            for d in dots_in_L   # inner dots that the line misclassifies
            if d.get_center()[0] > ax_L.c2p(-0.1, 0)[0]   # rough selection
        ])

        self.play(
            LaggedStart(*[Create(b) for b in wrong_boxes[:6]], lag_ratio=0.12),
            run_time=0.8,
        )

        close_note = tx(r"\text{Higher-order interaction} \Rightarrow \text{more complex boundary!}", 24, HIGHLIGHT_COLOR)
        close_note.move_to(at(0, Y_NOTE - 0.4))
        self.play(FadeIn(close_note), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)