"""
scene_3d_tensorgrad_v2.py
─────────────────────────────────────────────────────────────────────────────
SCENE 3D: TensorGrad — Phân tách Gradient để tiết kiệm bộ nhớ 5×
Duration: ~45 giây  (Giây 7:45 – 8:30 theo script)

PHONG CÁCH: Bám sát scene_1a
  • Tensor = lưới Dot (không dùng Cube / Prism)
  • Show-don't-tell: visual dẫn trước, text xác nhận sau
  • Mỗi phase có sub-title riêng ở Y_SUB
  • Công thức / ký hiệu hiện bằng MathTex

LAYOUT ZONES:
  Y_TITLE  =  3.40   Main title (cố định)
  Y_SUB    =  2.72   Sub-title / phase label
  X_LEFT   = -3.70   Visual chính
  X_RIGHT  =  3.10   Biểu đồ / thanh bar / thống kê
  Y_BOTTOM = -3.30   Ghi chú / công thức phụ
"""

from manim import *
import numpy as np

# ── Palette (nhất quán với toàn project) ──────────────────────────────────
BG          = "#0a0a1a"
C_TENSOR    = BLUE_D          
C_GRAD      = "#FF3333"       # SỬA: Đỏ tươi, sáng hơn
C_CORE      = "#FF1744"       # SỬA: Đỏ đậm rực
C_FACTOR    = "#FFB09C"       # SỬA: Cam đào sáng
C_HL        = YELLOW
C_OK        = "#44ff44"       # Kết quả tốt
C_WARN      = RED_C           # Cảnh báo
C_FWD       = BLUE_C          # Forward pass
C_SUB       = "#aaaacc"       # Subtitle / note nhẹ

T_SLOW   = 2.0
T_MED    = 1.2
T_FAST   = 0.5

# ── Helper: tạo lưới Dot (phong cách scene_1a) ───────────────────────────
def dot_grid(rows: int, cols: int, color=BLUE_D, radius=0.08, h_buff=0.22, v_buff=0.22) -> VGroup:
    """Tạo lưới Dot rows×cols, trả về VGroup."""
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=radius, color=color)
            d.move_to(RIGHT * c * h_buff + DOWN * r * v_buff)
            grid.add(d)
    return grid


X_LEFT  = -3.6
X_RIGHT =  3.2

def at(x, y): 
    return np.array([x, y, 0])


def dot_block(layers: int, rows: int, cols: int, color=BLUE_D,
              radius=0.07, h_buff=0.20, v_buff=0.20, depth_shift=0.18) -> VGroup:
    """Tensor giả 3-D: nhiều lớp lưới Dot xếp chéo nhau."""
    block = VGroup()
    for k in range(layers):
        layer = dot_grid(rows, cols, color=color, radius=radius,
                         h_buff=h_buff, v_buff=v_buff)
        layer.shift(RIGHT * depth_shift * k + UP * depth_shift * k)
        layer.set_opacity(1.0 - k * 0.05) 
        block.add(layer)
    return block


class TensorGrad(Scene):
    # ─────────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG

        # ── CỐ ĐỊNH: Main title ──────────────────────────────────────────
        title = MathTex(
            r"\text{TensorGrad: Factorize Gradient}",
            font_size=38, color=C_HL
        ).move_to(UP * 3.40)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=T_FAST)

        # ═════════════════════════════════════════════════════════════════
        # PHASE 1 — GRADIENT LÀ GÌ VÀ TẠI SAO NÓ "NẶNG"
        # ═════════════════════════════════════════════════════════════════
        sub1 = MathTex(
            r"\text{Training: Forward} \rightarrow \text{Backward}",
            font_size=28, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub1), run_time=T_FAST)

        # — Mạng nơ-ron đơn giản: 4 layer, mỗi layer là cột Dot ——————————
        layer_xs = [-5.2, -4.2, -3.2, -2.2]
        layer_ns   = [3,    5,    5,      3  ]
        node_cols  = []
        for lx, ln in zip(layer_xs, layer_ns):
            col = VGroup(*[
                Circle(radius=0.14, fill_color=C_FWD,
                       fill_opacity=0.85, stroke_width=0)
                .move_to(RIGHT * lx + UP * (i - (ln - 1) / 2) * 0.55)
                for i in range(ln)
            ])
            node_cols.append(col)

        # Edges giữa các layer
        edges = VGroup()
        for i in range(len(node_cols) - 1):
            for a in node_cols[i]:
                for b in node_cols[i + 1]:
                    edges.add(Line(
                        a.get_center(), b.get_center(),
                        stroke_color=WHITE, stroke_opacity=0.35, # SỬA: Đổi sang Trắng và tăng opacity
                        stroke_width=1.0
                    ))

        all_nodes = VGroup(*node_cols)
        net_group = VGroup(edges, all_nodes)
        net_group.scale(0.75)
        net_group.move_to(LEFT * 3.8 + UP * 0.2)

        self.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.005),
            LaggedStart(*[GrowFromCenter(n)
                          for col in node_cols for n in col],
                        lag_ratio=0.04),
            run_time=T_MED
        )

        # Mũi tên Forward (xanh)
        fwd_arr = Arrow(
            start=LEFT * 5.5 + DOWN * 1.6,
            end  =LEFT * 0.1 + DOWN * 1.6,
            color=C_FWD, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.07
        )
        fwd_lbl = MathTex(r"\text{forward pass}", font_size=16, color=C_FWD)\
            .next_to(fwd_arr, DOWN, buff=0.08)

        # Mũi tên Backward (đỏ)
        bwd_arr = Arrow(
            start=LEFT * 0.1 + DOWN * 2.10,
            end  =LEFT * 5.5 + DOWN * 2.10,
            color=C_WARN, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.07
        )
        bwd_lbl = MathTex(
            r"\text{backward: } \nabla W", font_size=16, color=C_WARN
        ).next_to(bwd_arr, DOWN, buff=0.08)

        self.play(GrowArrow(fwd_arr), FadeIn(fwd_lbl), run_time=T_FAST)
        self.play(GrowArrow(bwd_arr), FadeIn(bwd_lbl), run_time=T_FAST)

        # Khối Tensor gradient bên phải (Thu nhỏ lại 4x5x5 để bớt thô)
        grad_block = dot_block(
            layers=4, rows=5, cols=5,
            color="#FF3333", radius=0.06,
            h_buff=0.18, v_buff=0.18, depth_shift=0.15
        )
        # SỬA Ở ĐÂY: Ép khối đỏ dịch hẳn sang phải để né mạng NN
        RIGHT_ANCHOR = RIGHT * 3.2 + UP * 0.5 
        grad_block.move_to(RIGHT_ANCHOR)

        grad_label = MathTex(
            r"\nabla W \in \mathbb{R}^{n_1 \times n_2 \times \cdots}",
            font_size=24, color=WHITE
        ).next_to(grad_block, UP, buff=0.15)

        note_heavy = MathTex(
            r"\text{Raw Gradient occupies memory comparable to the model!}",
            font_size=24, color=WHITE      # SỬA: Chữ trắng cho dễ đọc
        ).move_to(DOWN * 3.30)

        self.play(FadeIn(grad_block, scale=0.7), FadeIn(grad_label),
                  run_time=T_MED)
        self.play(FadeIn(note_heavy), run_time=T_FAST)
        self.wait(0.8)

        # ═════════════════════════════════════════════════════════════════
        # PHASE 2 — PHÂN TÁCH GRADIENT (Tucker-style)
        # ═════════════════════════════════════════════════════════════════
        sub2 = MathTex(
            r"\text{Solution: Factorize } \nabla W",
            font_size=28, color=C_HL
        ).move_to(UP * 2.72)

        self.play(
            ReplacementTransform(sub1, sub2),
            FadeOut(note_heavy),
            run_time=T_FAST
        )

        # Core tensor (Thu nhỏ bán kính và khoảng cách)
        core_block = dot_block(
            layers=2, rows=3, cols=3,
            color=C_CORE, radius=0.06,  
            h_buff=0.18, v_buff=0.18, depth_shift=0.12
        )

        # Factor matrices — Ép mỏng lại cho tinh tế
        factor_U = Rectangle(
            width=0.15, height=1.0,
            fill_color=C_FACTOR, fill_opacity=0.9, stroke_width=0
        ).next_to(core_block, LEFT, buff=0.15)

        factor_V = Rectangle(
            width=1.0, height=0.15,
            fill_color=C_FACTOR, fill_opacity=0.9, stroke_width=0
        ).next_to(core_block, DOWN, buff=0.15)

        factor_W_mat = Rectangle(
            width=0.15, height=0.8,
            fill_color=C_FACTOR, fill_opacity=0.9, stroke_width=0
        ).next_to(core_block, RIGHT, buff=0.15)

        # Gom nhóm cụm Tucker Decomposition
        # ... (Phần khai báo core_block, factor_U, factor_V, factor_W_mat giữ nguyên) ...

        # ... (Phần trên khai báo core_block, factor_U, factor_V, factor_W_mat giữ nguyên) ...

        decomp_group = VGroup(core_block, factor_U, factor_V, factor_W_mat)
        approx_sign = MathTex(r"\approx", font_size=36, color=C_HL)

        # ─── 1. SỬA LỖI CỤC ĐỎ KHÔNG DI CHUYỂN ───
        # Animate cục đỏ sang trái một chút để nhường chỗ cho cụm phân rã
        GRAD_POS = RIGHT * -0.4 + UP * 0.5
        self.play(
            grad_block.animate.scale(0.6).move_to(GRAD_POS),
            run_time=T_MED
        )

        # Cố định anchor cho cụm tiếp theo
        approx_sign.move_to(RIGHT * 1.2 + UP * 0.5)
        decomp_group.move_to(RIGHT * 2.8 + UP * 0.5)

        # Label dời thẳng xuống dưới cụm Tucker
        decomp_lbl = MathTex(
            r"\mathcal{G} \times_1 U \times_2 V \times_3 W",
            font_size=24, color=C_HL
        ).next_to(decomp_group, DOWN, buff=0.4)

        note_decomp = MathTex(
            r"\text{Tucker: Core small} + \text{3 factor thin}",
            font_size=24, color=WHITE
        ).move_to(DOWN * 3.30)

        # Hiện các phần còn lại lên
        self.play(
            FadeIn(approx_sign),
            FadeIn(decomp_group, shift=UP * 0.1),
            FadeIn(decomp_lbl),
            run_time=T_MED
        )
        self.play(FadeIn(note_decomp), run_time=T_FAST)
        self.wait(1.0)

        # ─── 2. SỬA LỖI QUÊN XÓA (Dọn dẹp trước khi sang Phase 3) ───
        self.play(
            FadeOut(sub2),
            FadeOut(grad_block),
            FadeOut(approx_sign),
            FadeOut(decomp_group),
            FadeOut(decomp_lbl),
            FadeOut(note_decomp),
            FadeOut(grad_label),
            run_time=T_FAST
        )
    
        # ═════════════════════════════════════════════════════════════════
        # PHASE 3 — SO SÁNH BỘ NHỚ (Thanh bar trực quan)
        # ═════════════════════════════════════════════════════════════════
        sub3 = MathTex(
            r"\text{Result: Memory reduced by } 5\times",
            font_size=28, color=C_OK
        ).move_to(UP * 2.72)
        self.play(ReplacementTransform(sub2, sub3), run_time=T_FAST)

        # Xóa phần network, giữ lại grad mờ + decomp
        self.play(
            FadeOut(VGroup(edges, all_nodes, fwd_arr, fwd_lbl, bwd_arr, bwd_lbl)),
            run_time=T_FAST
        )

        # — Build so sánh bar —————————————————————————————————————————————
        bar_x      = -0.80          # tâm thanh bar
        bar_y_top  =  1.20
        bar_y_bot  = -0.20
        bar_w_full =  5.20
        bar_h      =  0.48

        # Nền bar (xám)
        bg_bar_old = Rectangle(
            width=bar_w_full, height=bar_h,
            fill_color="#222233", fill_opacity=1, stroke_width=0
        ).move_to(RIGHT * bar_x + UP * bar_y_top)

        bg_bar_new = Rectangle(
            width=bar_w_full, height=bar_h,
            fill_color="#222233", fill_opacity=1, stroke_width=0
        ).move_to(RIGHT * bar_x + UP * bar_y_bot)

        # Thanh đỏ "trước" — 100 %
        old_fill = Rectangle(
            width=bar_w_full, height=bar_h,
            fill_color=C_WARN, fill_opacity=0.88, stroke_width=0
        )
        old_fill.align_to(bg_bar_old, LEFT).move_to(
            bg_bar_old.get_left() + RIGHT * bar_w_full / 2
        )

        # Thanh xanh "sau" — 20 %
        new_w = bar_w_full * 0.20
        new_fill = Rectangle(
            width=new_w, height=bar_h,
            fill_color=C_OK, fill_opacity=0.88, stroke_width=0
        )
        new_fill.align_to(bg_bar_new, LEFT).move_to(
            bg_bar_new.get_left() + RIGHT * new_w / 2
        )

        lbl_old = MathTex(
            r"\text{Before:}\ 100\%\ \nabla W\ \text{fully populated}",
            font_size=20, color=C_WARN
        ).next_to(bg_bar_old, RIGHT, buff=0.18)

        lbl_new = MathTex(
            r"\text{After:}\ 20\%\ \text{(core + factors)}",
            font_size=20, color=C_OK
        ).next_to(bg_bar_new, RIGHT, buff=0.18)

        # Chú thích "Trước / Sau"
        lbl_title_old = MathTex(r"\text{Raw Gradient}", font_size=18, color=C_WARN)\
            .next_to(bg_bar_old, LEFT, buff=0.18)
        lbl_title_new = MathTex(r"\text{TensorGrad}", font_size=18, color=C_OK)\
            .next_to(bg_bar_new, LEFT, buff=0.18)

        self.play(FadeIn(bg_bar_old), FadeIn(lbl_title_old), run_time=T_FAST)
        self.play(GrowFromEdge(old_fill, LEFT), FadeIn(lbl_old), run_time=T_MED)

        self.play(FadeIn(bg_bar_new), FadeIn(lbl_title_new), run_time=T_FAST)
        self.play(GrowFromEdge(new_fill, LEFT), FadeIn(lbl_new), run_time=T_MED)

        # Nhãn "5× tiết kiệm" với mũi tên nối 2 thanh
        arrow_compare = Arrow(
            old_fill.get_left() + LEFT * 0.6,
            new_fill.get_left() + LEFT * 0.6,
            color=C_HL, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.12
        )
        save_lbl = MathTex(
            r"5\times", font_size=36, color=C_HL
        ).next_to(arrow_compare, LEFT, buff=0.12)

        self.play(GrowArrow(arrow_compare), FadeIn(save_lbl), run_time=T_FAST)

        note_final = MathTex(
            r"\text{TensorGrad: Train large models with GPU efficiently!}",
            font_size=24, color=C_HL
        ).move_to(DOWN * 3.30)
        self.play(FadeIn(note_final), run_time=T_FAST)
        self.wait(1.2)

        # ═════════════════════════════════════════════════════════════════
        # PHASE 4 — CÔNG THỨC ĐẦY ĐỦ (chốt ý)
        # ═════════════════════════════════════════════════════════════════
        sub4 = MathTex(
            r"\text{Key Idea}",
            font_size=28, color=C_HL
        ).move_to(UP * 2.72)
        self.play(ReplacementTransform(sub3, sub4), run_time=T_FAST)

        # Fade hết visual bar
        self.play(
            FadeOut(VGroup(
                bg_bar_old, old_fill, lbl_old, lbl_title_old,
                bg_bar_new, new_fill, lbl_new, lbl_title_new,
                arrow_compare, save_lbl, note_final
            )),
            run_time=T_FAST
        )

        # Công thức Tucker decomposition cho gradient
        formula = MathTex(
            r"\nabla W \;\approx\; \mathcal{G} \times_1 U_1 \times_2 U_2 \times_3 U_3",
            font_size=44, color=C_HL
        ).move_to(UP * 0.5)

        explain = VGroup(
            MathTex(r"\mathcal{G}\ \text{: Core tensor (small)}", font_size=26, color=C_CORE),
            MathTex(r"U_k\ \text{: Factor matrix (orthogonal)}", font_size=26, color=C_FACTOR),
            MathTex(r"\Rightarrow\ \text{Memory}\ \propto\ r^3 + 3nr", font_size=26, color=C_OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.4)

        self.play(Write(formula), run_time=T_SLOW)
        self.play(
            LaggedStart(*[FadeIn(e, shift=UP * 0.05) for e in explain],
                        lag_ratio=0.25),
            run_time=T_MED
        )

        # Glow effect trên công thức
        glow = formula.copy().set_stroke(C_HL, width=8, opacity=0.18)
        self.play(FadeIn(glow), run_time=0.35)
        self.play(FadeOut(glow), run_time=0.35)

        self.wait(1.5)

        # OUTRO
        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MED)