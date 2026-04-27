import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import random

from manim import *
from config import *

# ── Zone constants ────────────────────────────────────────────────────────────
Y_TITLE =  3.40
Y_SUB   =  2.72
Y_BODY  =  0.10
Y_NOTE  = -3.30
X_LEFT  = -3.70
X_RIGHT =  3.10

def at(x, y): return np.array([x, y, 0])

def make_title(s):
    return MathTex(s, font_size=32, color=HIGHLIGHT_COLOR).move_to(at(0, Y_TITLE))

def make_sub(s):
    return MathTex(s, font_size=28, color=SUBTITLE_COLOR).move_to(at(0, Y_SUB))

def make_note(s, color=SUBTITLE_COLOR):
    return MathTex(s, font_size=24, color=color).move_to(at(0, Y_NOTE))

# ── Tensor geometry ───────────────────────────────────────────────────────────
I_DIM = 4      # Users
J_DIM = 3      # Products
K_DIM = 5      # Time slices
SZ    = 0.44   # cell size
DX    = RIGHT * 0.64 + UP * 0.40   # stack offset along Z

def make_tensor_slices():
    """K stacked rectangles centred at (X_LEFT, Y_BODY)."""
    raw = VGroup()
    for k in range(K_DIM):
        face = Rectangle(
            width=J_DIM * SZ, height=I_DIM * SZ,
            stroke_color=TENSOR_EDGE_COLOR,
            stroke_opacity=max(0.35, 1.0 - k * 0.14),
            stroke_width=1.8,
            fill_color=TENSOR_COLOR,
            fill_opacity=max(0.02, 0.10 - k * 0.014),
        ).shift(k * DX)
        raw.add(face)
    raw.move_to(at(X_LEFT, Y_BODY))
    return raw


# ══════════════════════════════════════════════════════════════════════════════
class RecommenderTensor(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Fixed title ───────────────────────────────────────────────────────
        title = make_title(
            r"\textbf{Tensor in Recommender Systems}\ \text{— Netflix example}"
        )
        self.play(FadeIn(title), run_time=T_FAST)

        # ══════════════════════════════════════════════════════════════════════
        # [40–50s]  WHY a 2-D matrix loses information
        #
        # LEFT  zone: 2-D matrix diagram (static, no time axis)
        # RIGHT zone: 3-D tensor diagram (adds Time axis)
        # SUB   zone: subtitle explaining the gap
        # BOTTOM zone: key formula
        # ══════════════════════════════════════════════════════════════════════
        sub_why = make_sub(r"\text{Why not just a 2-D matrix?}")
        self.play(FadeIn(sub_why), run_time=T_FAST)

        # ── 2-D matrix (LEFT zone, slightly right of X_LEFT) ─────────────────
        mat2d = Rectangle(width=2.4, height=2.0,
                          fill_color=BLUE_E, fill_opacity=0.30,
                          stroke_color=BLUE_C, stroke_width=2)
        mat2d.move_to(at(-4.2, Y_BODY))

        # Row / col labels
        rows_lbl = MathTex(r"\text{Users}", font_size=18, color=SUBTITLE_COLOR)
        rows_lbl.rotate(PI / 2).next_to(mat2d, LEFT, buff=0.18)
        cols_lbl = MathTex(r"\text{Movies}", font_size=18, color=SUBTITLE_COLOR)
        cols_lbl.next_to(mat2d, DOWN, buff=0.18)

        # Missing time icon — clock drawn from primitives
        clock_circle = Circle(radius=0.28, color=RED_B, stroke_width=2)
        clock_h = Line(ORIGIN, UP * 0.15, color=RED_B, stroke_width=2)
        clock_m = Line(ORIGIN, RIGHT * 0.18, color=RED_B, stroke_width=2)
        clock   = VGroup(clock_circle, clock_h, clock_m).move_to(mat2d)
        cross   = Cross(clock_circle, stroke_color=RED, stroke_width=5).move_to(mat2d)

        lbl2d_top = MathTex(r"\mathbf{M} \in \mathbb{R}^{U \times V}",
                            font_size=20, color=BLUE_C)
        lbl2d_top.next_to(mat2d, UP, buff=0.14)
        lbl2d_fail = MathTex(r"\times\ \text{Time axis lost!}",
                             font_size=18, color=RED)
        lbl2d_fail.next_to(mat2d, DOWN, buff=0.42)

        # ── 3-D tensor sketch (RIGHT zone) ────────────────────────────────────
        # Three stacked rectangles = quick tensor silhouette
        t_slabs = VGroup()
        for k in range(3):
            slab = Rectangle(width=1.8, height=1.4,
                             fill_color=TENSOR_COLOR,
                             fill_opacity=0.12 + k * 0.06,
                             stroke_color=TENSOR_EDGE_COLOR,
                             stroke_width=1.5)
            slab.shift(k * (RIGHT * 0.30 + UP * 0.22))
            t_slabs.add(slab)
        t_slabs.move_to(at(X_RIGHT, Y_BODY))

        # Time arrow running along depth
        t_arr_start = t_slabs[0].get_corner(UR) + RIGHT * 0.06 + UP * 0.06
        t_arr_end   = t_slabs[-1].get_corner(UR) + RIGHT * 0.06 + UP * 0.06
        t_arr = Arrow(t_arr_start, t_arr_end,
                      color=VECTOR_COLOR, stroke_width=2.2,
                      max_tip_length_to_length_ratio=0.22)
        t_arr_lbl = MathTex(r"\text{Time}", font_size=18, color=VECTOR_COLOR)
        t_arr_lbl.next_to(t_arr, RIGHT, buff=0.10)

        lbl3d_top = MathTex(
            r"\mathcal{X} \in \mathbb{R}^{U \times V \times T}",
            font_size=20, color=TENSOR_EDGE_COLOR,
        ).next_to(t_slabs, UP, buff=0.14)
        lbl3d_ok = MathTex(r"\checkmark\ \text{Captures temporal trends}",
                           font_size=18, color=GREEN_B)
        lbl3d_ok.next_to(t_slabs, DOWN, buff=0.42)

        # Trend arrow over the 3D sketch
        trend = VMobject(color=YELLOW, stroke_width=3)
        trend.set_points_as_corners([
            t_slabs[0].get_left() + DOWN * 0.1,
            t_slabs[1].get_center() + UP * 0.25,
            t_slabs[2].get_right() + UP * 0.55,
        ])

        # Bottom note
        note_why = make_note(
            r"\mathbf{M}_{U\times V}\ \text{cannot model how preferences}\ "
            r"\textit{change over time}\ \Rightarrow\ "
            r"\mathcal{X}_{U\times V\times T}\ \text{preserves all three modes}"
        )

        # Animate
        self.play(
            FadeIn(mat2d), FadeIn(rows_lbl), FadeIn(cols_lbl),
            FadeIn(lbl2d_top),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(clock), run_time=T_FAST)
        self.play(Create(cross), run_time=T_FAST)
        self.play(FadeIn(lbl2d_fail), run_time=T_FAST)

        self.play(
            LaggedStart(*[FadeIn(s, scale=0.8) for s in t_slabs], lag_ratio=0.2),
            FadeIn(lbl3d_top),
            run_time=T_MEDIUM,
        )
        self.play(GrowArrow(t_arr), FadeIn(t_arr_lbl), run_time=T_FAST)
        self.play(Create(trend), run_time=T_MEDIUM)
        self.play(FadeIn(lbl3d_ok), run_time=T_FAST)
        self.play(Write(note_why), run_time=T_MEDIUM)
        self.wait(1.2)

        # Clear WHY section
        self.play(
            FadeOut(VGroup(sub_why, mat2d, rows_lbl, cols_lbl, clock, cross,
                           lbl2d_top, lbl2d_fail,
                           t_slabs, t_arr, t_arr_lbl, lbl3d_top, lbl3d_ok,
                           trend, note_why)),
            run_time=T_FAST,
        )

        # ══════════════════════════════════════════════════════════════════════
        # [50–60s]  BUILD TENSOR BLOCK  +  AXIS LABELS  +  FIBER
        # ══════════════════════════════════════════════════════════════════════
        sub_build = make_sub(
            r"\mathcal{X}_{U \times V \times T}\ \text{— Users} \times "
            r"\text{Products} \times \text{Time}"
        )
        slices = make_tensor_slices()
        self.play(FadeIn(sub_build), FadeIn(slices, scale=0.8), run_time=T_MEDIUM)

        # Axis labels
        lbl_u = MathTex(r"\text{Users}", font_size=13, color=HIGHLIGHT_COLOR)
        lbl_u.rotate(PI / 2).move_to(slices[0].get_left() + LEFT * 0.40)

        lbl_p = MathTex(r"\text{Products}", font_size=13, color=HIGHLIGHT_COLOR)
        lbl_p.move_to(slices[0].get_bottom() + DOWN * 0.35)

        t_start = slices[0].get_corner(UR) + RIGHT * 0.10 + UP * 0.10
        t_end   = slices[-1].get_corner(UR) + RIGHT * 0.10 + UP * 0.10
        arr_t   = Arrow(t_start, t_end, color=HIGHLIGHT_COLOR,
                        stroke_width=2.2, max_tip_length_to_length_ratio=0.18)
        lbl_t   = MathTex(r"\text{Time}", font_size=13, color=HIGHLIGHT_COLOR)
        lbl_t.move_to(t_end + RIGHT * 0.38 + UP * 0.08)

        self.play(
            LaggedStart(FadeIn(lbl_u), FadeIn(lbl_p),
                        GrowArrow(arr_t), FadeIn(lbl_t), lag_ratio=0.2),
            run_time=T_MEDIUM,
        )
        self.wait(0.6)

        # ── Fiber annotation panel (RIGHT zone) ───────────────────────────────
        sub_fib = make_sub(
            r"\text{Fiber } \mathcal{X}[i,\,j,\,:] \;—\; "
            r"\text{vector along one axis (all indices except one fixed)}"
        )
        self.play(
            FadeOut(VGroup(sub_build, lbl_u, lbl_p, arr_t, lbl_t)),
            FadeIn(sub_fib),
            slices.animate.set_opacity(0.22),
            run_time=T_FAST,
        )

        # Index panel — RIGHT zone, three MathTex lines stacked
        idx_panel = VGroup(
            MathTex(r"\text{Fix 2 indices, free 1:}", font_size=24,
                    color=SUBTITLE_COLOR),
            MathTex(r"\mathcal{X}[i,\,j,\,:] \;\longrightarrow\; \text{fiber along Time}",
                    font_size=20, color=VECTOR_COLOR),
            MathTex(r"\mathcal{X}[:,\,j,\,k] \;\longrightarrow\; \text{fiber along Users}",
                    font_size=20, color=YELLOW_D),
            MathTex(r"\mathcal{X}[i,\,:,\,k] \;\longrightarrow\; \text{fiber along Products}",
                    font_size=20, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        idx_panel.move_to(at(X_RIGHT, Y_BODY + 0.2))

        self.play(
            LaggedStart(*[FadeIn(l, shift=LEFT * 0.08) for l in idx_panel],
                        lag_ratio=0.22),
            run_time=T_MEDIUM,
        )
        self.wait(0.5)

        # ── Draw Fiber X[0,0,:] in LEFT zone ─────────────────────────────────
        def cell_center(k, r, c):
            base = slices[k].get_corner(DL)
            return base + RIGHT * (c + 0.5) * SZ + UP * (r + 0.5) * SZ

        FI, FJ = I_DIM - 1, 0   # fixed user & product indices

        fib_cells = VGroup()
        fib_lines = VGroup()
        prev = None
        for k in range(K_DIM):
            pos = cell_center(k, FI, FJ)
            cell = Square(side_length=SZ * 0.82,
                          fill_color=YELLOW_D, fill_opacity=0.85,
                          stroke_color=YELLOW, stroke_width=2).move_to(pos)
            fib_cells.add(cell)
            if prev is not None:
                fib_lines.add(Line(prev, pos, color=YELLOW, stroke_width=3))
            prev = pos

        for k in range(K_DIM):
            anims = [FadeIn(fib_cells[k])]
            if k > 0:
                anims.append(Create(fib_lines[k - 1]))
            self.play(*anims, run_time=0.20)

        fib_lbl = MathTex(r"\mathcal{X}[0,\,0,\,:]\ \text{— fiber along Time}",
                          font_size=24, color=YELLOW)
        fib_lbl.move_to(at(X_LEFT, Y_NOTE + 0.55))
        self.play(FadeIn(fib_lbl), run_time=T_FAST)
        self.wait(0.4)

        # ── Two more parallel fibers (②b) ─────────────────────────────────────
        for ri, ci, col in [(1, 1, YELLOW_D), (2, 2, ORANGE)]:
            cf = VGroup()
            lf = VGroup()
            pp = None
            for k in range(K_DIM):
                pos = cell_center(k, ri, ci)
                c = Square(side_length=SZ * 0.78,
                           fill_color=col, fill_opacity=0.72,
                           stroke_color=col, stroke_width=1.5).move_to(pos)
                cf.add(c)
                if pp is not None:
                    lf.add(Line(pp, pos, color=col, stroke_width=2.2))
                pp = pos
            self.play(
                LaggedStart(
                    *[AnimationGroup(FadeIn(cf[k]),
                                     *([] if k == 0 else [Create(lf[k - 1])]))
                      for k in range(K_DIM)],
                    lag_ratio=0.16,
                ),
                run_time=0.55,
            )

        note_par = MathTex(
            r"\text{Every fiber along Time is}\ \parallel\ \text{to the Time axis}",
            font_size=24, color=SUBTITLE_COLOR,
        ).move_to(at(0, Y_NOTE))
        self.play(FadeIn(note_par), run_time=T_FAST)
        self.wait(0.7)

        # Clear fiber section
        self.play(
            *[FadeOut(m) for m in self.mobjects
              if m not in [title, slices]],
            run_time=T_FAST,
        )

        # ══════════════════════════════════════════════════════════════════════
        # [60–65s]  SLICE  X[:,:,k]
        # ══════════════════════════════════════════════════════════════════════
        sub_sl = make_sub(
            r"\text{Slice } \mathcal{X}[:,\,:,\,2] \;—\; "
            r"\text{2-D matrix at fixed Time } k=2"
        )
        self.play(FadeIn(sub_sl), slices.animate.set_opacity(0.30), run_time=T_FAST)

        # RIGHT zone — index explanation
        sl_panel = VGroup(
            MathTex(r"\text{Fix 1 index, free 2:}", font_size=15,
                    color=SUBTITLE_COLOR),
            MathTex(r"\mathcal{M} = \mathcal{X}[:,\,:,\,k] \in \mathbb{R}^{U \times V}",
                    font_size=16, color=MATRIX_COLOR),
            MathTex(r"\texttt{Python:}\ X[:, :, 2]", font_size=13,
                    color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        sl_panel.move_to(at(X_RIGHT, Y_BODY + 0.6))

        self.play(
            LaggedStart(*[FadeIn(l) for l in sl_panel], lag_ratio=0.2),
            run_time=T_MEDIUM,
        )

        # Highlight slice k=2 in LEFT zone
        hl = Rectangle(width=J_DIM * SZ, height=I_DIM * SZ,
                       stroke_color=MATRIX_COLOR, stroke_width=3.5,
                       fill_opacity=0).move_to(slices[2].get_center())
        self.play(Create(hl), run_time=T_FAST)

        # Extract 2-D matrix (RIGHT zone, below sl_panel)
        CW, CH = 0.62, 0.46
        dummy = [["4.5","—","3.0"],["—","5.0","2.5"],
                 ["3.5","4.0","—"],["—","2.0","4.5"]]
        tl_x = X_RIGHT - (J_DIM * CW) / 2
        tl_y = Y_BODY - 0.50 + (I_DIM * CH) / 2

        mat_grp = VGroup()
        for r in range(I_DIM):
            for c in range(J_DIM):
                v = dummy[r][c]
                cx = tl_x + (c + 0.5) * CW
                cy = tl_y - (r + 0.5) * CH
                cell = Rectangle(width=CW, height=CH,
                                 stroke_color=MATRIX_COLOR, stroke_width=1.0,
                                 fill_color=MATRIX_COLOR if v != "—" else BG_COLOR,
                                 fill_opacity=0.25 if v != "—" else 0.04
                                 ).move_to(at(cx, cy))
                txt  = MathTex(v if v != "—" else r"\text{—}",
                               font_size=11,
                               color=WHITE if v != "—" else DARK_GRAY
                               ).move_to(at(cx, cy))
                mat_grp.add(cell, txt)

        # Column / row headers
        col_names = [r"\text{A}", r"\text{B}", r"\text{C}"]
        row_names = [r"\text{U}_1", r"\text{U}_2",
                     r"\text{U}_3", r"\text{U}_4"]
        for c, h in enumerate(col_names):
            mat_grp.add(MathTex(h, font_size=9, color=HIGHLIGHT_COLOR)
                        .move_to(at(tl_x + (c + 0.5) * CW, tl_y + 0.26)))
        for r, h in enumerate(row_names):
            mat_grp.add(MathTex(h, font_size=9, color=HIGHLIGHT_COLOR)
                        .move_to(at(tl_x - 0.28, tl_y - (r + 0.5) * CH)))

        t3_lbl = MathTex(r"@ \; t_3", font_size=13, color=MATRIX_COLOR)
        t3_lbl.move_to(at(X_RIGHT, tl_y + 0.52))

        self.play(FadeOut(sl_panel), run_time=T_FAST)
        self.play(
            ReplacementTransform(hl.copy(), mat_grp),
            FadeIn(t3_lbl),
            run_time=T_MEDIUM,
        )
        self.wait(0.8)
        self.play(FadeOut(VGroup(sub_sl, hl, mat_grp, t3_lbl)), run_time=T_FAST)

        # ══════════════════════════════════════════════════════════════════════
        # [65–70s]  MODE-1 UNFOLDING
        # ══════════════════════════════════════════════════════════════════════
        sub_uf = make_sub(r"\text{Mode-1 Unfolding}\ \mathbf{X}_{(1)} \in \mathbb{R}^{I \times JK}")
        self.play(
            FadeIn(sub_uf),
            slices.animate.set_opacity(0.88),
            run_time=T_FAST,
        )

        # Shrink tensor LEFT to make room
        self.play(
            slices.animate.scale(0.60).move_to(at(-4.85, Y_BODY)),
            run_time=T_MEDIUM,
        )

        # Unfolded matrix layout
        UCW = 0.25; UCH = 0.40
        UJK = J_DIM * K_DIM
        UW  = UJK * UCW; UH = I_DIM * UCH

        u_tl_x = X_RIGHT - UW / 2
        u_tl_y = Y_BODY  + UH / 2

        UCOLS = [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]

        all_ucells = VGroup()
        random.seed(42)

        for k in range(K_DIM):
            for j in range(J_DIM):
                col_idx = k * J_DIM + j

                # Source fiber column in shrunken tensor
                sk = slices[k]
                src_cx  = sk.get_corner(DL)[0] + (j + 0.5) * SZ * 0.60
                src_top = sk.get_corner(UL)[1]
                src_bot = sk.get_corner(DL)[1]
                src_fib = Rectangle(
                    width=SZ * 0.60,
                    height=abs(src_top - src_bot),
                    fill_color=UCOLS[k], fill_opacity=0.55,
                    stroke_color=UCOLS[k], stroke_width=1.5,
                ).move_to(at(src_cx, (src_top + src_bot) / 2))

                # Destination column in unfolded matrix
                dst_cx = u_tl_x + (col_idx + 0.5) * UCW
                dst_col = VGroup()
                for r in range(I_DIM):
                    cy = u_tl_y - (r + 0.5) * UCH
                    cell = Rectangle(width=UCW, height=UCH,
                                     fill_color=UCOLS[k], fill_opacity=0.40,
                                     stroke_color=UCOLS[k], stroke_width=0.7,
                                     ).move_to(at(dst_cx, cy))
                    dst_col.add(cell)
                all_ucells.add(dst_col)

                self.play(FadeIn(src_fib), run_time=0.10)
                self.play(ReplacementTransform(src_fib, dst_col), run_time=0.18)

        # Time-slice header bands above columns
        u_headers = VGroup()
        for k in range(K_DIM):
            cx = u_tl_x + (k * J_DIM + J_DIM / 2) * UCW
            bg = Rectangle(width=J_DIM * UCW, height=0.22,
                           fill_color=UCOLS[k], fill_opacity=0.70,
                           stroke_width=0).move_to(at(cx, u_tl_y + 0.17))
            lbl = MathTex(rf"t_{k+1}", font_size=10, color=WHITE)
            lbl.move_to(at(cx, u_tl_y + 0.17))
            u_headers.add(bg, lbl)

        # Row labels
        u_rowlbls = VGroup()
        for r in range(I_DIM):
            cy = u_tl_y - (r + 0.5) * UCH
            u_rowlbls.add(
                MathTex(rf"\text{{U}}_{r+1}", font_size=10, color=SUBTITLE_COLOR)
                .move_to(at(u_tl_x - 0.26, cy))
            )

        self.play(FadeIn(u_headers), FadeIn(u_rowlbls), run_time=T_FAST)

        # Braces + formula in BOTTOM zone
        brace_u = Brace(all_ucells, direction=UP, color=YELLOW)
        b_lbl   = MathTex(r"J \times K = 15\ \text{columns}",
                          font_size=14, color=YELLOW)
        b_lbl.next_to(brace_u, UP, buff=0.06)
        # Clamp to stay below Y_SUB
        if b_lbl.get_top()[1] > Y_SUB - 0.08:
            b_lbl.shift(DOWN * (b_lbl.get_top()[1] - Y_SUB + 0.10))

        brace_l = Brace(all_ucells, direction=LEFT, color=HIGHLIGHT_COLOR)
        bl_lbl  = MathTex(r"I{=}4", font_size=18, color=HIGHLIGHT_COLOR)
        bl_lbl.next_to(brace_l, LEFT, buff=0.06)

        formula = MathTex(
            r"\mathbf{X}_{(1)} \in \mathbb{R}^{4 \times 15}",
            font_size=22, color=MATH_COLOR,
        ).move_to(at(X_RIGHT, Y_NOTE + 0.50))

        note_uf = make_note(
            r"\text{Each fiber (column) in the tensor becomes a column in the unfolded matrix}"
        )

        self.play(
            FadeIn(brace_u), Write(b_lbl),
            FadeIn(brace_l), Write(bl_lbl),
            run_time=T_FAST,
        )
        self.play(Write(formula), FadeIn(note_uf), run_time=T_MEDIUM)
        self.wait(T_SLOW)

        # ── Fade all ──────────────────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(
                title, sub_uf,
                slices, all_ucells, u_headers, u_rowlbls,
                brace_u, b_lbl, brace_l, bl_lbl,
                formula, note_uf,
            )),
            run_time=T_MEDIUM,
        )