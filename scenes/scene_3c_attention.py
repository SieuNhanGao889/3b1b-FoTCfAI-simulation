"""
scenes/scene_3c_attention.py
────────────────────────────────────────────────────────────────────────────
SCENE 3C: Polynomial Self-Attention   (6:30 – 7:45, ≈ 75s)

STORY ARC (Show Don't Tell):

  Beat 1  [0–20s]  THE COST OF LOOKING AT EVERYTHING
    An N×N grid fills the left half of the screen — built as a dot-grid, 
    so the viewer FEELS the density. Color darkens toward diagonal (self-attention
    weighting). Label: "N=512 → 262,144 cells". Big red O(N²) hovers above.
    Formula: Attention(Q,K,V) = softmax(QKᵀ)V
    QKᵀ is boxed in red — that's the culprit.

  Beat 2  [20–40s]  THE POLYNOMIAL TRICK
    "What if we remove softmax?" — the N×N grid COLLAPSES.
    Left dots compress row-by-row into a single thin row (N cells).
    New formula with φ(Q)(φ(K)ᵀV) appears — parentheses show reordering.
    The key insight: K'ᵀV is computed FIRST (d×d, not N×N).
    Show this with a small square (d×d green block) next to the thin row.

  Beat 3  [40–60s]  SIDE-BY-SIDE COMPLEXITY
    LEFT: "Maze" — O(N²) tangle of crossing red lines (N=8 shown).
    RIGHT: "Highway" — O(N) straight parallel green lines.
    The contrast is pure geometry — no bar charts.
    Each line in the highway carries one token's information forward cleanly.

  Beat 4  [60–75s]  PAYOFF NUMBERS
    Counter animates: N=512 → O(N²)=262,144 vs O(N)=512.
    Then: "Chuỗi dài 1000× — cùng bộ nhớ."
    Flash, hold, fade.

Design principles:
  • N×N attention grid = dot_field (1a-style). NO matrix primitives from Manim.
  • Collapse animation: rows of dots shrink/merge into a single horizontal bar.
  • Every number is shown geometrically before being stated as text.
  • Diagonal gradient on the attention grid signals "self-similarity" focus.
"""

from manim import *
from manim import ManimColor

# ── Palette ───────────────────────────────────────────────────────────────────
BG_COLOR        = "#0d0d0d"
HIGHLIGHT_COLOR = YELLOW
SUBTITLE_COLOR  = GREY_B

ATTN_HI = "#1565C0"    # dark blue — dense attention cell
ATTN_LO = "#4FC3F7"    # light blue — sparse attention cell
POLY_COL = "#E0C424"   # yellow — polynomial / O(N)
KV_COL   = "#F7F7F7"   # light gray — K'ᵀV block

# ── Layout ────────────────────────────────────────────────────────────────────
Y_TITLE =  3.40  # Đẩy Title lên sát mép trên cùng (cũ: 3.30)
Y_SUB   =  2.80  # Đẩy Subtitle lên cao hơn để mở rộng vùng an toàn (cũ: 2.65)
Y_BODY  = -0.30  # Hạ trọng tâm TOÀN BỘ đồ thị & công thức xuống (cũ: 0.10)
Y_NOTE  = -3.40  # Hạ phần text note ở đáy màn hình xuống theo (cũ: -3.10)
X_LEFT  = -3.50  # Giữ nguyên
X_RIGHT =  3.20  # Giữ nguyên

def at(x, y):
    return np.array([x, y, 0])

def tx(s, sz=28, col=WHITE):
    return MathTex(s, font_size=sz, color=col)

def words(s, sz=26, col=WHITE):
    return Text(s, font_size=sz, color=col)


# ── Visual helpers ────────────────────────────────────────────────────────────

def attention_grid(n, cell, center):
    """
    NxN dot grid where diagonal dots are brighter (self-attention pattern).
    Returns VGroup of Dots.
    """
    g = VGroup()
    for i in range(n):
        for j in range(n):
            # Brightness: diagonal = max, off-diagonal fades
            dist = abs(i - j)
            alpha = max(0.25, 1.0 - dist * 0.15)
            col = interpolate_color(ManimColor(ATTN_LO),ManimColor(ATTN_HI), 1.0 - alpha)
            d = Dot(radius=cell * 0.34, color=col, fill_opacity=alpha)
            d.move_to(RIGHT * j * cell + DOWN * i * cell)
            g.add(d)
    g.move_to(center)
    return g


def thin_row(n, cell, col, alpha, center):
    """A single row of n dots — represents O(N) linear memory."""
    g = VGroup()
    for j in range(n):
        d = Dot(radius=cell * 0.38, color=col, fill_opacity=alpha)
        d.move_to(RIGHT * j * cell)
        g.add(d)
    g.move_to(center)
    return g


def kv_block(w, h, col, center):
    """Small square representing d×d KᵀV intermediate — much smaller than N×N."""
    r = Rectangle(width=w, height=h,
                  fill_color=col, fill_opacity=0.75,
                  stroke_color=col, stroke_width=1.5)
    r.move_to(center)
    return r


# ══════════════════════════════════════════════════════════════════════════════
class PolynomialAttention(Scene):
# ══════════════════════════════════════════════════════════════════════════════
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Fixed title ───────────────────────────────────────────────────────
        title = tx(r"\text{Polynomial Self-Attention: }O(N^2)\to O(N)", 30, HIGHLIGHT_COLOR)
        title.move_to(at(0, Y_TITLE))
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 1: THE N×N ATTENTION GRID — feel the density
        # ════════════════════════════════════════════════════════════════════
        sub_1 = words("Standard Attention: every token attends to every token", 26, SUBTITLE_COLOR)
        sub_1.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_1), run_time=0.5)

        # Build N=9 attention grid (representative of large N)
        N = 9
        cell_size = 0.34
        grid = attention_grid(N, cell_size, at(X_LEFT + 0.3, Y_BODY + 0.2))

        grid_lbl = tx(r"QK^\top \in \mathbb{R}^{N\times N}", 21, WHITE)
        grid_lbl.next_to(grid, DOWN, buff=0.22)

        on2_badge = tx(r"\mathcal{O}(N^2)", 42, RED_C)
        on2_badge.move_to(at(X_LEFT + 0.3, Y_BODY + 2.2))

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.6) for d in grid], lag_ratio=0.004),
            run_time=1.4,
        )
        self.play(FadeIn(grid_lbl), run_time=0.4)
        self.play(Write(on2_badge), run_time=0.6)

        # Standard formula on the right
        formula_old = tx(
            r"\text{Attn}(Q,K,V)=\text{ softmax }(QK^\top)V",
            26, WHITE,
        )
        formula_old.move_to(at(X_RIGHT - 0.3, Y_BODY + 0.8))
        self.play(Write(formula_old), run_time=0.8)

        # Box the culprit: QKᵀ
        culprit_box = SurroundingRectangle(formula_old[0][12:19],
                                            color=RED_C, buff=0.08, stroke_width=2.0)
        culprit_arrow = Arrow(
            culprit_box.get_left() + LEFT * 0.1,    
            grid.get_right() + RIGHT * 0.2,         
            buff=0.0, color=RED_C, stroke_width=1.8, tip_length=0.18,
        )
        culprit_note = tx(r"\text{create matrix }N\times N!", 20, RED_C)
        culprit_note.next_to(culprit_box, UP, buff=0.12)

        self.play(Create(culprit_box), FadeIn(culprit_note), run_time=0.6)
        self.play(Create(culprit_arrow), run_time=0.5)
        self.wait(1.8)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 2: THE POLYNOMIAL TRICK — collapse the grid
        # ════════════════════════════════════════════════════════════════════
        sub_2 = tx(r"\phi(Q)\big(\phi(K)^\top V\big)\ \text{— change the order of computation}", 26, HIGHLIGHT_COLOR)
        sub_2.move_to(at(0, Y_SUB))
        self.play(
            ReplacementTransform(sub_1, sub_2),
            FadeOut(culprit_box), FadeOut(culprit_note), FadeOut(culprit_arrow),
            run_time=0.5,
        )

        # Collapse animation: rows of the N×N grid merge into a thin row
        # Each row of grid dots slides vertically to Y_BODY - 0.5, packing into 1 row
        n_dots = len(grid)
        n_rows = N
        target_y = Y_BODY - 0.5
        # Compute target positions (all dots collapse to their column position, row=0)
        col_centers = [grid[j].get_center()[0] for j in range(N)]

        collapse_anims = []
        for idx, dot in enumerate(grid):
            col_idx = idx % N
            target = np.array([col_centers[col_idx], target_y, 0])
            collapse_anims.append(dot.animate.move_to(target).set_opacity(0.0))

        # Simultaneously, build the new thin row (O(N))
        row_poly = thin_row(N, cell_size, POLY_COL, 0.92, at(X_LEFT + 0.3, target_y))

        self.play(
            LaggedStart(*collapse_anims, lag_ratio=0.01),
            run_time=1.2,
        )
        self.play(
            FadeOut(grid),
            FadeIn(row_poly),
            FadeOut(grid_lbl),
            FadeOut(on2_badge),
            run_time=0.6,
        )

        row_lbl = tx(r"\phi(Q)\in\mathbb{R}^{N}", 20, POLY_COL)
        row_lbl.next_to(row_poly, DOWN, buff=0.18)
        self.play(FadeIn(row_lbl), run_time=0.3)

        # Small d×d KᵀV block — show that this step is cheap
        kv_rect = kv_block(0.95, 0.95, KV_COL, at(X_LEFT + 0.3, Y_BODY + 1.3))
        # SỬA: Tăng cỡ chữ 18 -> 26 và 24
        kv_lbl  = tx(r"\phi(K)^\top V \in \mathbb{R}^{d\times d}", 26, KV_COL)
        kv_lbl.next_to(kv_rect, RIGHT, buff=0.30)
        kv_note = tx(r"d\ll N\ (\text{cheap!})", 24, KV_COL).next_to(kv_lbl, DOWN, buff=0.15)

        self.play(GrowFromCenter(kv_rect), FadeIn(kv_lbl), FadeIn(kv_note), run_time=0.7)

        on_badge = tx(r"\mathcal{O}(N)", 42, POLY_COL)
        on_badge.move_to(at(X_LEFT + 0.3, Y_BODY + 2.3))
        self.play(Write(on_badge), run_time=0.5)

        # New formula
        formula_new = tx(r"\phi(Q)\underbrace{\bigl(\phi(K)^\top V\bigr)}_{d\times d}", 26, POLY_COL)
        formula_new.move_to(at(X_RIGHT - 0.3, Y_BODY - 0.4))
        self.play(
            FadeOut(formula_old),
            Write(formula_new),
            run_time=0.8,
        )
        self.wait(1.5)

        # ── Clear beat-2, keep title ──────────────────────────────────────
        self.play(
            FadeOut(VGroup(row_poly, row_lbl, kv_rect, kv_lbl, kv_note,
                           on_badge, formula_new, sub_2)),
            run_time=0.5,
        )

        # ════════════════════════════════════════════════════════════════════
        # BEAT 3: SIDE-BY-SIDE — Maze (N²) vs Highway (N)
        # Geometry IS the argument. No bar charts.
        # ════════════════════════════════════════════════════════════════════
        sub_3 = words("Geometry of the Difference", 26, SUBTITLE_COLOR)
        sub_3.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_3), run_time=0.4)

        # LEFT: Dense tangle — O(N²) cross-connections (8 tokens, all-to-all)
        n_tok = 8
        tok_L = [at(-4.5 + i * 0.45, Y_BODY - 1.8) for i in range(n_tok)]
        tok_L_dots = VGroup(*[Dot(p, color=RED_C, radius=0.10) for p in tok_L])

        # All-to-all edges (N*(N-1)/2 lines)
        tangle = VGroup()
        for i in range(n_tok):
            for j in range(i + 1, n_tok):
                tangle.add(Line(tok_L[i], tok_L[j],
                                color=RED_C, stroke_width=0.9, stroke_opacity=0.5))

        on2_lbl = tx(r"\mathcal{O}(N^2) = " + str(n_tok * n_tok), 24, RED_C)
        on2_lbl.move_to(at(X_LEFT + 1.2, Y_BODY + 1.6))

        left_cap = words("All-to-all (crossing paths)", 19, RED_C)
        left_cap.move_to(at(X_LEFT + 1.2, Y_NOTE + 0.7))

        self.play(
            LaggedStart(*[Create(e) for e in tangle], lag_ratio=0.02),
            FadeIn(tok_L_dots),
            run_time=1.0,
        )
        self.play(Write(on2_lbl), FadeIn(left_cap), run_time=0.5)

        # RIGHT: Clean highway — O(N) straight parallel lines
        tok_R_start = [at(1.0, Y_BODY - 1.8 + i * 0.52) for i in range(n_tok)]
        tok_R_end   = [at(5.0, Y_BODY - 1.8 + i * 0.52) for i in range(n_tok)]
        tok_R_dots  = VGroup(*[Dot(p, color=POLY_COL, radius=0.10) for p in tok_R_start])
        
        highway = VGroup(*[
            Line(tok_R_start[i], tok_R_end[i],
                 color=POLY_COL, stroke_width=2.0, stroke_opacity=0.85)
            for i in range(n_tok)
        ])

        on_lbl = tx(r"\mathcal{O}(N) = " + str(n_tok), 24, POLY_COL)
        on_lbl.move_to(at(X_RIGHT - 0.2, Y_BODY + 1.6))

        right_cap = words("Each token — a separate lane", 19, POLY_COL)
        right_cap.move_to(at(X_RIGHT - 0.2, Y_NOTE + 0.7))

        self.play(
            LaggedStart(*[Create(line) for line in highway], lag_ratio=0.09),
            FadeIn(tok_R_dots),
            run_time=0.9,
        )
        self.play(Write(on_lbl), FadeIn(right_cap), run_time=0.5)

        # Dividing line between left and right panels
        div = DashedLine(at(0, Y_BODY - 2.5), at(0, Y_BODY + 2.2),
                          color=GREY_D, stroke_width=1.2, stroke_opacity=0.5)
        self.play(Create(div), run_time=0.4)
        self.wait(1.5)

        # ════════════════════════════════════════════════════════════════════
        # BEAT 4: PAYOFF NUMBERS — animated counter
        # ════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(tangle, tok_L_dots, on2_lbl, left_cap,
                           highway, tok_R_dots, on_lbl, right_cap, div, sub_3)),
            run_time=0.5,
        )

        sub_4 = words("N = 512:", 26, SUBTITLE_COLOR)
        sub_4.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_4), run_time=0.4)

        # N² count
        n2_row = VGroup(
            tx(r"\mathcal{O}(N^2):", 30, RED_C),
            tx(r"262{,}144\ \text{steps}", 28, RED_C),
        ).arrange(RIGHT, buff=0.3).move_to(at(0, Y_BODY + 0.8))

        n1_row = VGroup(
            tx(r"\mathcal{O}(N):", 30, POLY_COL),
            tx(r"512\ \text{steps}", 28, POLY_COL),
        ).arrange(RIGHT, buff=0.3).move_to(at(0, Y_BODY - 0.2))

        self.play(FadeIn(n2_row), run_time=0.5)
        self.play(FadeIn(n1_row), run_time=0.5)

        # Ratio
        ratio_line = tx(r"\times\ 512\ \text{times faster!}", 32, HIGHLIGHT_COLOR)
        ratio_line.move_to(at(0, Y_BODY - 1.3))
        self.play(Write(ratio_line), run_time=0.6)

        # Final big payoff stamp
        stamp_ring  = Circle(radius=1.5, stroke_color=HIGHLIGHT_COLOR, stroke_width=4,
                              fill_color=BG_COLOR, fill_opacity=0.96)
        stamp_line1 = words("Long Sequence", 24, HIGHLIGHT_COLOR)
        stamp_line2 = tx(r"1000\times", 46, HIGHLIGHT_COLOR)
        stamp_line3 = words("Less Memory!", 22, POLY_COL)
        stamp_inner = VGroup(stamp_line1, stamp_line2, stamp_line3).arrange(DOWN, buff=0.12)
        stamp = VGroup(stamp_ring, stamp_inner).move_to(at(0, Y_BODY - 0.7))

        stamp.scale(2.5)
        self.play(
            FadeOut(VGroup(n2_row, n1_row, ratio_line)),
            stamp.animate.scale(1 / 2.5),
            rate_func=rate_functions.ease_out_bounce,
            run_time=0.7,
        )

        self.play(Flash(stamp_ring, color=HIGHLIGHT_COLOR, line_length=0.5, num_lines=16),
                  run_time=0.5)

        # Closing note
        close = tx(r"\text{Tensor reordering} \Rightarrow O(N^2) \to O(N)", 24, POLY_COL)
        close.move_to(at(0, Y_NOTE + 0.4))
        self.play(FadeIn(close), run_time=0.5)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)