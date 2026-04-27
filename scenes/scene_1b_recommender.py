import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *

# ═══════════════════════════════════════════════════════════════════════════════
# SCENE: RecommenderTensor
# Flow: [3D Overview] → [Fiber concept] → [Slice concept] → [Unfolding]
# ═══════════════════════════════════════════════════════════════════════════════

class RecommenderTensor(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Constants ──────────────────────────────────────────────────────────
        I  = 4          # Users
        J  = 3          # Products
        K  = 5          # Time slices
        SZ = 0.5        # cell size
        DX = RIGHT * 0.8 + UP * 0.48   # stack offset per slice

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 1 — 3D OVERVIEW  (đơn giản, nhanh)
        # ══════════════════════════════════════════════════════════════════════
        title = Text("Tensor 3 Dimensions — Data Recommendation",
                     font_size=21, color=HIGHLIGHT_COLOR, weight=BOLD
                     ).to_edge(UP, buff=0.28)
        self.play(FadeIn(title), run_time=0.4)

        # Vẽ K slices — chỉ outline, không fill rườm rà
        slices = VGroup()
        for k in range(K):
            face = Rectangle(
                width=J * SZ, height=I * SZ,
                stroke_color=TENSOR_EDGE_COLOR,
                stroke_opacity=1.0 - k * 0.14,
                stroke_width=2,
                fill_color=TENSOR_COLOR,
                fill_opacity=0.07 + (K - 1 - k) * 0.035,
            ).shift(k * DX)
            slices.add(face)

        slices.center().shift(DOWN * 0.55 + LEFT * 1.5)

        # Xuất hiện từng lớp nhanh
        self.play(FadeIn(slices[0]), run_time=0.3)
        for k in range(1, K):
            self.play(FadeIn(slices[k]), run_time=0.1)

        # 3 trục label — ngắn gọn, đặt đúng chỗ
        lbl_u = Text("Users", font_size=17, color=HIGHLIGHT_COLOR, weight=BOLD)
        lbl_u.rotate(PI / 2).next_to(slices[0], LEFT, buff=0.22)

        lbl_p = Text("Products", font_size=17, color=HIGHLIGHT_COLOR, weight=BOLD)
        lbl_p.next_to(slices[0], DOWN, buff=0.22)

        arr_t = Arrow(
            slices[0].get_corner(UR) + RIGHT * 0.1 + UP * 0.1,
            slices[-1].get_corner(UR) + RIGHT * 0.1 + UP * 0.1,
            color=HIGHLIGHT_COLOR, stroke_width=2.5, buff=0, tip_length=0.16
        )
        lbl_t = Text("Time", font_size=17, color=HIGHLIGHT_COLOR, weight=BOLD)
        lbl_t.next_to(arr_t.get_end(), UR, buff=0.08)

        # Vài điểm dữ liệu "nổi" trên slice đầu
        sample_dots = VGroup()
        positions = [(0, 0), (1, 1), (2, 2), (3, 1)]
        sample_vals = ["4.5★", "3.0★", "5.0★", "2.5★"]
        for (r, c), val in zip(positions, sample_vals):
            dot_pos = (
                slices[0].get_corner(DL)
                + RIGHT * (c + 0.5) * SZ
                + UP    * (r + 0.5) * SZ
            )
            dot = Dot(dot_pos, radius=0.07, color=VECTOR_COLOR)
            lbl = Text(val, font_size=10, color=WHITE).next_to(dot, UP, buff=0.04)
            sample_dots.add(dot, lbl)

        self.play(
            LaggedStart(
                FadeIn(lbl_u), FadeIn(lbl_p),
                GrowArrow(arr_t), FadeIn(lbl_t),
                lag_ratio=0.2
            ),
            run_time=0.7
        )
        self.play(LaggedStart(*[FadeIn(d) for d in sample_dots], lag_ratio=0.15), run_time=0.6)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 2 — ZOOM VÀO FIBER CONCEPT
        # Không giữ full 3D — vẽ lại fiber như 1 đường thẳng
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(lbl_u, lbl_p, arr_t, lbl_t, sample_dots)),
            run_time=0.3
        )

        fiber_title = Text(
            "Fiber  X[i, j, :]  —  1 user × 1 product, at all time slices",
            font_size=19, color=VECTOR_COLOR, weight=BOLD
        ).next_to(title, DOWN, buff=0.18)
        self.play(Write(fiber_title), run_time=0.5)

        # Mờ tensor gốc
        self.play(slices.animate.set_opacity(0.15), run_time=0.35)

        # ── Vẽ fiber như timeline ngang, tách biệt, rõ ràng ──
        FIBER_Y   = -2.4
        DOT_GAP   = 1.4
        fiber_xs  = [(-2) * DOT_GAP + i * DOT_GAP for i in range(K)]
        time_lbls = ["t₁", "t₂", "t₃", "t₄", "t₅"]
        fiber_vals = [2.0, 3.5, 4.0, 3.0, 4.5]
        fiber_colors = [
            interpolate_color(VECTOR_COLOR, YELLOW, v / 5.0)
            for v in fiber_vals
        ]

        # Đường ngang (timeline)
        timeline = Line(
            LEFT * DOT_GAP * 2.5, RIGHT * DOT_GAP * 2.5,
            color=GRAY, stroke_width=1.5
        ).shift(DOWN * abs(FIBER_Y))

        self.play(Create(timeline), run_time=0.4)

        fiber_nodes = VGroup()
        fiber_annots = VGroup()
        for i, (x, val, col, t) in enumerate(zip(fiber_xs, fiber_vals, fiber_colors, time_lbls)):
            pos = RIGHT * x + DOWN * abs(FIBER_Y)
            node = Circle(radius=0.28, fill_color=col, fill_opacity=0.9,
                          stroke_color=WHITE, stroke_width=1.5).move_to(pos)
            val_txt = Text(f"{val}★", font_size=13, color=WHITE, weight=BOLD).move_to(pos)
            t_txt   = Text(t, font_size=14, color=SUBTITLE_COLOR).next_to(node, DOWN, buff=0.12)
            fiber_nodes.add(node, val_txt)
            fiber_annots.add(t_txt)
            self.play(
                FadeIn(node), FadeIn(val_txt), FadeIn(t_txt),
                run_time=0.18
            )

        fiber_bracket = Brace(fiber_nodes, direction=UP, color=VECTOR_COLOR)
        fiber_eq = MathTex(r"\mathbf{x} = [2.0,\ 3.5,\ 4.0,\ 3.0,\ 4.5]",
                           font_size=20, color=VECTOR_COLOR
                           ).next_to(fiber_bracket, UP, buff=0.1)
        self.play(FadeIn(fiber_bracket), Write(fiber_eq), run_time=0.5)
        self.wait(0.9)

        # ── Clean up fiber, chuyển sang Slice ──
        self.play(
            FadeOut(VGroup(fiber_title, timeline, fiber_nodes,
                           fiber_annots, fiber_bracket, fiber_eq)),
            run_time=0.35
        )

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 2b — SLICE CONCEPT
        # Tách 1 lát cắt ra, vẽ như ma trận 2D rõ ràng
        # ══════════════════════════════════════════════════════════════════════
        slice_title = Text(
            "Slice  X[:, :, t₃]  —  All users × products at t₃",
            font_size=19, color=MATRIX_COLOR, weight=BOLD
        ).next_to(title, DOWN, buff=0.18)
        self.play(Write(slice_title), run_time=0.45)

        # Highlight slice k=2 (t₃) trong tensor gốc
        hl_rect = Rectangle(
            width=J * SZ, height=I * SZ,
            stroke_color=MATRIX_COLOR, stroke_width=3.5, fill_opacity=0
        ).move_to(slices[2].get_center())
        self.play(
            slices.animate.set_opacity(0.55),
            Create(hl_rect),
            run_time=0.4
        )

        # Tách slice ra thành ma trận 2D bên phải
        CELL_2D = 0.62
        matrix_2d = VGroup()
        dummy_vals = [
            ["4.5", "—",   "3.0"],
            ["—",   "5.0", "2.5"],
            ["3.5", "4.0", "—"  ],
            ["—",   "2.0", "4.5"],
        ]
        col_hdrs = ["Movie A", "Movie B", "Movie C"]
        row_hdrs = ["User 1", "User 2", "User 3", "User 4"]

        mat_origin = RIGHT * 2.4 + DOWN * 0.5

        for r, row in enumerate(dummy_vals):
            for c, val in enumerate(row):
                cell_rect = Rectangle(
                    width=CELL_2D, height=CELL_2D * 0.72,
                    stroke_color=MATRIX_COLOR, stroke_width=1.2,
                    fill_color=(MATRIX_COLOR if val != "—" else BG_COLOR),
                    fill_opacity=(0.25 if val != "—" else 0.04),
                ).shift(mat_origin + RIGHT * c * CELL_2D + DOWN * r * CELL_2D * 0.72)
                cell_txt = Text(val, font_size=12,
                                color=(WHITE if val != "—" else GRAY)
                                ).move_to(cell_rect.get_center())
                matrix_2d.add(cell_rect, cell_txt)

        # Header cols
        for c, h in enumerate(col_hdrs):
            t = Text(h, font_size=11, color=HIGHLIGHT_COLOR, weight=BOLD)
            t.move_to(mat_origin + RIGHT * c * CELL_2D + UP * CELL_2D * 0.5)
            matrix_2d.add(t)
        for r, h in enumerate(row_hdrs):
            t = Text(h, font_size=11, color=HIGHLIGHT_COLOR, weight=BOLD)
            t.move_to(mat_origin + LEFT * CELL_2D * 0.65 + DOWN * r * CELL_2D * 0.72)
            matrix_2d.add(t)

        # t₃ label
        t3_lbl = Text("@ t₃", font_size=16, color=MATRIX_COLOR, weight=BOLD)
        t3_lbl.next_to(matrix_2d, UP, buff=0.15)

        self.play(
            ReplacementTransform(hl_rect.copy(), matrix_2d),
            run_time=T_SLOW
        )
        self.play(FadeIn(t3_lbl), run_time=0.3)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 3 — UNFOLDING (PHẦN QUAN TRỌNG NHẤT)
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(slice_title, hl_rect, matrix_2d, t3_lbl)),
            slices.animate.set_opacity(0.85),
            run_time=0.4
        )

        unfold_title = Text(
            "Mode-1 Unfolding — Flatten Tensor → 2D Matrix",
            font_size=19, color=YELLOW, weight=BOLD
        ).next_to(title, DOWN, buff=0.18)
        self.play(Write(unfold_title), run_time=0.45)

        # Thu nhỏ tensor sang trái
        self.play(
            slices.animate.scale(0.62).move_to(LEFT * 4.0 + DOWN * 0.5),
            run_time=T_MEDIUM
        )

        # ── Animated mapping: mỗi slice → 1 block màu trong unfolded matrix ──
        UF_W   = 1.0        # width của 1 block (= J cols → thu gọn)
        UF_H   = I * SZ * 0.62 * 0.9   # height = I users
        UF_GAP = 0.05
        UF_X0  = -0.3       # x bắt đầu của unfolded
        UF_Y   = -0.5

        block_colors = [
            BLUE_D, TEAL_D, GREEN_D, GOLD_D, RED_D
        ]

        unfolded_blocks = VGroup()
        arrow_group    = VGroup()

        for k in range(K):
            x_pos = UF_X0 + k * (UF_W + UF_GAP)
            block = Rectangle(
                width=UF_W, height=UF_H,
                fill_color=block_colors[k], fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=1.2
            ).move_to(RIGHT * x_pos + DOWN * abs(UF_Y))

            # Nhãn thời gian
            t_lbl = Text(f"t{k+1}", font_size=13, color=WHITE, weight=BOLD
                         ).move_to(block.get_center())
            unfolded_blocks.add(block, t_lbl)

            # Mũi tên từ slice k → block k
            src = slices[k].get_right() + RIGHT * 0.05
            dst = block.get_left()
            arr = Arrow(src, dst, color=block_colors[k],
                        stroke_width=1.8, buff=0.06, tip_length=0.13)
            arrow_group.add(arr)

            self.play(
                GrowArrow(arr),
                FadeIn(block), FadeIn(t_lbl),
                run_time=0.28
            )

        # Brace tổng và công thức
        brace_top = Brace(unfolded_blocks, direction=UP, color=YELLOW)
        brace_lbl = MathTex(
            r"J \times K = 3 \times 5 = 15 \text{ columns}",
            font_size=18, color=YELLOW
        ).next_to(brace_top, UP, buff=0.08)

        brace_left = Brace(unfolded_blocks, direction=LEFT, color=HIGHLIGHT_COLOR)
        brace_left_lbl = MathTex(r"I = 4", font_size=18, color=HIGHLIGHT_COLOR
                                 ).next_to(brace_left, LEFT, buff=0.08)

        math_eq = MathTex(
            r"\mathbf{X}_{(1)} \in \mathbb{R}^{4 \times 15}",
            font_size=28, color=MATH_COLOR
        ).next_to(unfolded_blocks, DOWN, buff=0.3)

        self.play(
            FadeIn(brace_top), Write(brace_lbl),
            FadeIn(brace_left), Write(brace_left_lbl),
            run_time=0.5
        )
        self.play(Write(math_eq), run_time=0.5)

        # Note cuối
        note = Text(
            "Now we can use SVD, PCA, Matrix Factorization...",
            font_size=15, color=SUBTITLE_COLOR
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(T_SLOW)

        # Fade out
        self.play(
            FadeOut(VGroup(
                slices, arrow_group, unfolded_blocks,
                title, unfold_title,
                brace_top, brace_lbl, brace_left, brace_left_lbl,
                math_eq, note
            )),
            run_time=T_MEDIUM
        )