"""
scenes/scene_2b_cp_decomposition.py
SCENE 2B: CP Decomposition — The Resurrection from Fibers (2:10 – 3:20)

Target runtime: ~70 seconds
─────────────────────────────────────────────────────────────────────────────
Phase A  (0 – 10s)  : Tensor W từ scene trước quay; câu hỏi "Có cách nào…"
Phase B  (10 – 30s) : Khối "tan chảy" → 3 vector a, b, c (màu vàng/cam/đỏ nhạt)
Phase C  (30 – 60s) : Outer-product animation: a⊗b → ma trận 2D, ⊗c → khối 3D;
                       sau đó 5 bộ (a_r, b_r, c_r) mỗi màu khác nhau
Phase D  (60 – 70s) : 5 khối nhỏ chồng lên nhau (+=), dấu ≈ W, công thức hoàn chỉnh
─────────────────────────────────────────────────────────────────────────────
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D

# ── Layout constants ──────────────────────────────────────────────────────────
Y_TITLE =  3.30
Y_SUB   =  2.65
Y_BODY  =  0.10
Y_NOTE  = -3.10

X_LEFT  = -4.20
X_MID   =  0.00
X_RIGHT =  3.20

def at(x, y):
    return np.array([x, y, 0])

def tex(s, size=30, color=WHITE):
    return MathTex(s, font_size=size, color=color)

def txt(s, size=28, color=WHITE):
    return Text(s, font_size=size, color=color)

# Colour palette for rank-1 terms (5 bộ)
RANK_COLORS = [YELLOW, ORANGE, "#FF6B6B", TEAL_C, BLUE_C]

# ── Helper: build a simple 3-D box with coloured faces using Polygon ──────────
def make_box(nx, ny, nz, cx=0.22, fc=BLUE, ec=WHITE, opacity=0.75):
    """Return a VGroup that looks like an isometric 3-D box of nx×ny×nz cells."""
    # We'll draw the three visible faces of the box using parallelograms.
    w  = nx * cx        # width  (x-axis on screen → RIGHT)
    h  = ny * cx        # height (y-axis on screen → UP)
    d  = nz * cx * 0.5 # depth  (projected as UP-RIGHT at 30°)

    dx = RIGHT * cx * 0.866  # isometric x-step
    dy = UP    * cx * 0.5    # isometric depth y-step

    origin = ORIGIN
    # Front face  (nx × ny, lies in screen plane)
    front_corners = [
        origin,
        origin + RIGHT * w,
        origin + RIGHT * w + UP * h,
        origin + UP * h,
    ]
    # Top face (nx × nz, slopes up-right)
    top_corners = [
        origin + UP * h,
        origin + UP * h + RIGHT * w,
        origin + UP * h + RIGHT * w + dx * nz,
        origin + UP * h + dx * nz,
    ]
    # Right face (ny × nz, slopes up from right edge)
    right_corners = [
        origin + RIGHT * w,
        origin + RIGHT * w + dx * nz,
        origin + RIGHT * w + dx * nz + UP * h,
        origin + RIGHT * w + UP * h,
    ]

    def face(corners, alpha):
        return Polygon(*corners,
                       fill_color=fc, fill_opacity=alpha,
                       stroke_color=ec, stroke_width=0.8)

    grp = VGroup(
        face(front_corners, opacity),
        face(top_corners,   opacity * 0.65),
        face(right_corners, opacity * 0.80),
    )
    return grp


# ── Main scene ────────────────────────────────────────────────────────────────
class CPDecomposition(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ══════════════════════════════════════════════════════════════════════
        # PHASE A (0–10s): Tensor W quay, câu hỏi xuất hiện
        # ══════════════════════════════════════════════════════════════════════
        title = tex(r"\mathcal{W}\text{ — weight tensor}", 32, HIGHLIGHT_COLOR)
        title.move_to(at(X_MID, Y_TITLE))
        self.play(FadeIn(title), run_time=0.6)

        # Tensor block
        tensor_W = make_box(5, 4, 6, cx=0.26, fc=TENSOR_COLOR, ec=TENSOR_EDGE_COLOR)
        tensor_W.move_to(at(X_MID - 0.5, Y_BODY))

        lbl_W   = tex(r"\mathcal{W}", 36, TENSOR_EDGE_COLOR).next_to(tensor_W, UP, buff=0.15)
        size_lbl = txt("9,408 parameters", 18, SUBTITLE_COLOR).next_to(tensor_W, DOWN, buff=0.14)

        self.play(FadeIn(tensor_W, scale=0.85), FadeIn(lbl_W), FadeIn(size_lbl), run_time=0.8)

        # Slow rotation (just shift-scale illusion via animate)
        self.play(tensor_W.animate.shift(RIGHT * 0.12).scale(1.03), run_time=1.0,
                  rate_func=there_and_back)

        # Question text
        question = txt("Is it possible to store fewer parameters?", 28, YELLOW)
        question.move_to(at(X_MID, Y_NOTE + 0.6))
        self.play(Write(question), run_time=1.2)
        self.wait(2.0)   # hold so voice-over can land

        # ══════════════════════════════════════════════════════════════════════
        # PHASE B (10–30s): Khối "tan chảy" → 3 vector a, b, c
        # ══════════════════════════════════════════════════════════════════════
        sub_b = tex(r"\text{Decomposing the tensor into three vectors}", 26, HIGHLIGHT_COLOR)
        sub_b.move_to(at(X_MID, Y_SUB))
        self.play(FadeIn(sub_b), run_time=0.5)

        # Build the three factor vectors
        def make_vec_col(n, color, cell_h=0.30, cell_w=0.14):
            return VGroup(*[
                Rectangle(height=cell_h, width=cell_w,
                           fill_color=color, fill_opacity=0.9, stroke_width=0.6,
                           stroke_color=WHITE)
                for _ in range(n)
            ]).arrange(DOWN, buff=0.07)

        def make_vec_row(n, color, cell_h=0.14, cell_w=0.30):
            return VGroup(*[
                Rectangle(height=cell_h, width=cell_w,
                           fill_color=color, fill_opacity=0.9, stroke_width=0.6,
                           stroke_color=WHITE)
                for _ in range(n)
            ]).arrange(RIGHT, buff=0.07)

        vec_a = make_vec_col(5, YELLOW)
        vec_b = make_vec_row(4, ORANGE)
        vec_c = make_vec_col(6, "#FF9999")   # light red / salmon

        # Position: spread to left side after melt
        vec_a.move_to(at(X_LEFT + 0.5, Y_BODY + 0.3))
        vec_b.move_to(at(X_LEFT + 2.0, Y_BODY + 0.3))
        vec_c.move_to(at(X_LEFT + 3.5, Y_BODY + 0.3))

        lbl_a = tex(r"a\in\mathbb{R}^5",  20, YELLOW ).next_to(vec_a, DOWN, buff=0.10)
        lbl_b = tex(r"b\in\mathbb{R}^4",  20, ORANGE ).next_to(vec_b, DOWN, buff=0.10)
        lbl_c = tex(r"c\in\mathbb{R}^6",  20, "#FF9999").next_to(vec_c, DOWN, buff=0.10)

        # Melt animation: tensor fades + dissolves into vectors
        self.play(
            tensor_W.animate.set_opacity(0.12),
            FadeOut(lbl_W), FadeOut(size_lbl), FadeOut(question),
            run_time=1.0
        )
        self.play(
            LaggedStart(
                TransformFromCopy(tensor_W, vec_a),
                TransformFromCopy(tensor_W, vec_b),
                TransformFromCopy(tensor_W, vec_c),
                lag_ratio=0.35
            ),
            run_time=2.5
        )
        self.play(
            FadeIn(lbl_a), FadeIn(lbl_b), FadeIn(lbl_c),
            FadeOut(tensor_W),
            run_time=0.7
        )

        voice_note = txt("Instead of storing the entire tensor, we only store the three vectors.", 22, SUBTITLE_COLOR)
        voice_note.move_to(at(X_MID, Y_NOTE + 0.5))
        self.play(FadeIn(voice_note), run_time=0.5)
        self.wait(3.5)   # voice-over time

        # ══════════════════════════════════════════════════════════════════════
        # PHASE C (30–60s): Outer-product demo + 5 rank-1 terms
        # ══════════════════════════════════════════════════════════════════════
        sub_c = tex(r"\text{Outer Product: }a\circ b \rightarrow \text{Matrix}\ 5\times4", 26, HIGHLIGHT_COLOR)
        sub_c.move_to(at(X_MID, Y_SUB))
        self.play(ReplacementTransform(sub_b, sub_c), FadeOut(voice_note), run_time=0.6)

        # ── a ⊗ b → 2D matrix ─────────────────────────────────────────────
        mat_ab = VGroup(*[
            VGroup(*[
                Square(side_length=0.22,
                       fill_color=interpolate_color(YELLOW, ORANGE, j / 3),
                       fill_opacity=0.55, stroke_width=0.6)
                for j in range(4)
            ]).arrange(RIGHT, buff=0.04)
            for i in range(5)
        ]).arrange(DOWN, buff=0.04)
        mat_ab.move_to(at(X_RIGHT - 0.5, Y_BODY + 0.2))

        lbl_ab = tex(r"a\circ b", 22, ORANGE).next_to(mat_ab, UP, buff=0.12)

        # Animate: a and b sweep together to form matrix
        self.play(
            vec_a.animate.move_to(at(X_RIGHT - 2.0, Y_BODY)),
            vec_b.animate.move_to(at(X_RIGHT - 0.5, Y_BODY + 1.4)),
            run_time=1.0
        )
        self.play(
            LaggedStart(
                FadeOut(vec_a), FadeOut(lbl_a),
                FadeOut(vec_b), FadeOut(lbl_b),
                lag_ratio=0.2
            ),
            FadeIn(mat_ab, scale=0.8), FadeIn(lbl_ab),
            run_time=1.2
        )
        self.wait(1.0)

        # ── (a ⊗ b) ⊗ c → 3D tensor ──────────────────────────────────────
        sub_c2 = tex(r"(a\circ b)\circ c \rightarrow \text{3D tensor}\ 5\times4\times6", 26, HIGHLIGHT_COLOR)
        sub_c2.move_to(at(X_MID, Y_SUB))
        self.play(ReplacementTransform(sub_c, sub_c2), run_time=0.5)

        hint_c = txt("Matrix encountering vector c → explodes into a 3D tensor!", 22, SUBTITLE_COLOR)
        hint_c.move_to(at(X_MID, Y_NOTE + 0.5))
        self.play(FadeIn(hint_c), run_time=0.4)

        tensor_r1 = make_box(5, 4, 6, cx=0.20, fc=interpolate_color(YELLOW, ORANGE, 0.5), ec=ORANGE)
        tensor_r1.move_to(at(X_RIGHT - 0.5, Y_BODY))
        lbl_r1 = tex(r"a_1\circ b_1\circ c_1", 20, ORANGE).next_to(tensor_r1, UP, buff=0.12)

        self.play(
            vec_c.animate.move_to(at(X_RIGHT - 0.5, Y_BODY - 1.3)),
            run_time=0.6
        )
        self.play(
            ReplacementTransform(mat_ab, tensor_r1),
            ReplacementTransform(lbl_ab, lbl_r1),
            FadeOut(vec_c), FadeOut(lbl_c),
            run_time=1.5
        )
        self.wait(1.5)

        # ── 5 bộ (a_r, b_r, c_r) mỗi màu khác nhau ─────────────────────
        sub_c3 = tex(r"\text{Creating multiple sets }(a_r,\,b_r,\,c_r)", 26, HIGHLIGHT_COLOR)
        sub_c3.move_to(at(X_MID, Y_SUB))
        self.play(ReplacementTransform(sub_c2, sub_c3), FadeOut(hint_c), run_time=0.5)

        voice2 = txt("We create multiple sets like this.", 22, SUBTITLE_COLOR)
        voice2.move_to(at(X_MID, Y_NOTE + 0.5))
        self.play(FadeIn(voice2), run_time=0.4)

        R = 5
        small_blocks = VGroup()
        small_lbls   = VGroup()
        xs = np.linspace(-4.5, 3.5, R)

        for r in range(R):
            blk = make_box(5, 4, 6, cx=0.14, fc=RANK_COLORS[r], ec=RANK_COLORS[r], opacity=0.75)
            blk.move_to(at(xs[r], Y_BODY - 0.4))
            lbl = tex(rf"a_{r+1}\circ b_{r+1}\circ c_{r+1}", 16, RANK_COLORS[r])
            lbl.next_to(blk, DOWN, buff=0.08)
            small_blocks.add(blk)
            small_lbls.add(lbl)

        self.play(
            FadeOut(tensor_r1), FadeOut(lbl_r1),
            run_time=0.4
        )
        self.play(
            LaggedStart(
                *[FadeIn(small_blocks[r], shift=UP * 0.2) for r in range(R)],
                lag_ratio=0.25
            ),
            run_time=2.0
        )
        self.play(
            LaggedStart(
                *[FadeIn(small_lbls[r]) for r in range(R)],
                lag_ratio=0.15
            ),
            run_time=1.0
        )
        self.wait(2.0)

        # ══════════════════════════════════════════════════════════════════════
        # PHASE D (60–70s): Chồng khối, ≈ W, công thức hoàn chỉnh
        # ══════════════════════════════════════════════════════════════════════
        sub_d = MathTex(
            r"\text{Adding all together } \approx \text{ Original tensor } \mathcal{W}",
            font_size=26,
            color=GREEN_C
        )
        sub_d.move_to(at(X_MID, Y_SUB))
        self.play(ReplacementTransform(sub_c3, sub_d), FadeOut(voice2), run_time=0.5)

        # Stack all small blocks at center with offset
        stack_center = at(X_MID - 0.8, Y_BODY)
        stacked = VGroup()
        for r in range(R):
            b = make_box(5, 4, 6, cx=0.20, fc=RANK_COLORS[r], ec=RANK_COLORS[r], opacity=0.70)
            b.move_to(stack_center + UR * 0.09 * r)
            stacked.add(b)

        self.play(
            FadeOut(small_lbls),
            LaggedStart(
                *[ReplacementTransform(small_blocks[r], stacked[r]) for r in range(R)],
                lag_ratio=0.18
            ),
            run_time=2.0
        )

        # Plus signs between offsets (visual shorthand)
        plus_signs = VGroup(*[
            tex("+", 28, WHITE).move_to(stack_center + UR * 0.09 * r + LEFT * 0.6)
            for r in range(1, R)
        ])
        self.play(LaggedStart(*[FadeIn(p) for p in plus_signs], lag_ratio=0.1), run_time=0.6)
        self.wait(0.4)

        # ≈ W label
        approx_W = tex(r"\approx\,\mathcal{W}", 42, HIGHLIGHT_COLOR)
        approx_W.next_to(stacked, RIGHT, buff=0.5)
        self.play(FadeIn(approx_W, scale=1.2), run_time=0.6)

        # Full formula
        formula = MathTex(
            r"\mathcal{W} \approx \sum_{r=1}^{R}"
            r"a_r \circ b_r \circ c_r",
            font_size=38, color=HIGHLIGHT_COLOR
        ).move_to(at(X_RIGHT + 0.2, Y_BODY - 1.5))
        self.play(Write(formula), run_time=1.2)

        voice3 = txt("This is the CP Decomposition!", 26, GREEN_C)
        voice3.move_to(at(X_MID, Y_NOTE + 0.5))
        self.play(FadeIn(voice3, scale=1.1), run_time=0.6)
        self.wait(3.0)

        # ── Outro ─────────────────────────────────────────────────────────────
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)