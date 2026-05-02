"""
scene_4ab_data_mining_v2.py
─────────────────────────────────────────────────────────────────────────────
SCENE 4A + 4B: Data Mining với Tensor Factorization
Duration: ~90 giây
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────
BG        = "#0a0a1a"
C_TENSOR  = BLUE_D
C_HL      = YELLOW
C_SUB     = "#aaaacc"
C_WARN    = RED_C
C_OK      = GREEN_C
C_SRC_A   = RED_C
C_SRC_B   = GREEN_C
C_SRC_BG  = BLUE_B
C_NTF_1   = "#ff6644"    # Nhóm teen
C_NTF_2   = BLUE_C       # Nhóm trung niên
C_NTF_3   = YELLOW_C     # Nhóm promo
C_MISSING = "#888899"    # Viền xám sáng cho ô trống
C_FILLED  = "#FFD700"    # Vàng Gold chói để dễ nhìn trên nền xanh

T_SLOW  = 2.0
T_MED   = 1.2
T_FAST  = 0.5

# ── Helpers ───────────────────────────────────────────────────────────────
def dot_grid(rows, cols, color=BLUE_D, radius=0.07,
             h_buff=0.20, v_buff=0.20) -> VGroup:
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=radius, color=color)
            d.move_to(RIGHT * c * h_buff + DOWN * r * v_buff)
            g.add(d)
    return g


def dot_block(layers, rows, cols, color=BLUE_D, radius=0.065,
              h_buff=0.19, v_buff=0.19, depth=0.17) -> VGroup:
    block = VGroup()
    for k in range(layers):
        layer = dot_grid(rows, cols, color=color,
                         radius=radius, h_buff=h_buff, v_buff=v_buff)
        layer.shift(RIGHT * depth * k + UP * depth * k)
        layer.set_opacity(1.0 - k * 0.50 / max(layers - 1, 1))
        block.add(layer)
    return block


def make_wave(x_start, y_center, n_pts, freq, amp, color,
              stroke_w=2.2, x_step=0.15) -> VMobject:
    w = VMobject(color=color, stroke_width=stroke_w)
    pts = [
        np.array([x_start + t * x_step,
                  y_center + amp * np.sin(freq * t), 0])
        for t in range(n_pts)
    ]
    w.set_points_as_corners(pts)
    return w


def mark_missing_dots(tensor_block, missing_indices, color, bg_color):
    """
    Tạo hiệu ứng "lỗ hổng" cho các ô dữ liệu bị khuyết.
    """
    for layer_idx, row_idx, col_idx in missing_indices:
        layer = tensor_block[layer_idx]
        dot_idx = row_idx * 5 + col_idx
        if dot_idx < len(layer):
            dot = layer[dot_idx]
            dot.set_fill(color=bg_color, opacity=1.0) # Làm rỗng ruột
            dot.set_stroke(color=color, width=2.5)    # Viền xám sáng
            dot.set_radius(0.12)                      # To hơn chút để lộ viền
    return tensor_block


class DataMiningAB(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Main title ───────────────────────────────────────────────────
        title = MathTex(
            r"\text{Tensor Factorization: The Lens for Decoding Data}",
            font_size=36, color=C_HL
        ).move_to(UP * 3.40)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=T_FAST)

        # ═════════════════════════════════════════════════════════════════
        # SCENE 4A — COCKTAIL PARTY / BLIND SOURCE SEPARATION
        # ═════════════════════════════════════════════════════════════════
        sub_4a = MathTex(
            r"\text{4A — Find source sounds (Cocktail Party Problem)}",
            font_size=26, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub_4a), run_time=T_FAST)

        # ── Fix layout 4A: Dịch qua phải, nới rộng Y, nhãn ở trên (UP) ───
        x_src = -5.2
        y_A = 1.3
        y_B = 0.0
        y_N = -1.3

        src_A = Dot(np.array([x_src, y_A, 0]), color=C_SRC_A, radius=0.14)
        src_B = Dot(np.array([x_src, y_B, 0]), color=C_SRC_B, radius=0.14)
        src_N = Dot(np.array([x_src, y_N, 0]), color=C_SRC_BG, radius=0.14)

        lbl_A = MathTex(r"\text{Source A}", font_size=18, color=C_SRC_A)\
            .next_to(src_A, UP, buff=0.10)
        lbl_B = MathTex(r"\text{Source B}", font_size=18, color=C_SRC_B)\
            .next_to(src_B, UP, buff=0.10)
        lbl_N = MathTex(r"\text{Background Noise}", font_size=18, color=C_SRC_BG)\
            .next_to(src_N, UP, buff=0.10)

        # Căn lại waveform bắt đầu từ sát bên phải của source
        wave_A = make_wave(x_src + 0.4, y_A, 20, 0.8, 0.28, C_SRC_A)
        wave_B = make_wave(x_src + 0.4, y_B, 20, 1.4, 0.22, C_SRC_B)
        wave_N = make_wave(x_src + 0.4, y_N, 20, 0.4, 0.18, C_SRC_BG)

        self.play(
            LaggedStart(
                GrowFromCenter(src_A), GrowFromCenter(src_B), GrowFromCenter(src_N),
                lag_ratio=0.25
            ),
            FadeIn(lbl_A), FadeIn(lbl_B), FadeIn(lbl_N),
            run_time=T_FAST
        )
        self.play(
            LaggedStart(Create(wave_A), Create(wave_B), Create(wave_N),
                        lag_ratio=0.2),
            run_time=T_MED
        )

        # ── Khối Tensor hỗn hợp ─────────────────────────────────────────
        tensor_mix = dot_block(
            layers=4, rows=5, cols=5,
            color=BLUE_D, radius=0.07,
            h_buff=0.20, v_buff=0.20, depth=0.18
        ).move_to(np.array([-0.6, 0.0, 0]))

        axes_lbl = MathTex(
            r"\underbrace{\text{Freq} \times \text{Time} \times \text{Mic}}_{\text{Mixed Tensor}}",
            font_size=18, color=C_SUB
        ).next_to(tensor_mix, DOWN, buff=0.25)

        self.play(FadeIn(tensor_mix, scale=0.8), FadeIn(axes_lbl), run_time=T_MED)

        # ── Lăng kính ────────────────────────────────────────────────────
        center_zone = 1.6
        prism = Polygon(
            np.array([center_zone - 0.45,  0.85, 0]),
            np.array([center_zone - 0.45, -0.65, 0]),
            np.array([center_zone + 0.50,  0.10, 0]),
            fill_color="#7fd8ff", fill_opacity=0.25,
            stroke_color="#7fd8ff", stroke_width=2.0
        )
        prism_lbl = MathTex(
            r"\text{Tensor}\\ \text{Factorization}",
            font_size=16, color="#7fd8ff"
        ).move_to(np.array([center_zone, 1.4, 0]))

        in_ray = Line(
            tensor_mix.get_right(), prism.get_left(),
            color=WHITE, stroke_width=1.8
        )

        self.play(Create(in_ray), FadeIn(prism), FadeIn(prism_lbl), run_time=T_FAST)

        # ── FIX ĐỈNH NỐI: Sử dụng get_right() để lấy đúng đỉnh chóp ───
        prism_tip = prism.get_right()
        right_zone = 3.6
        out_rays = VGroup(
            Line(prism_tip, np.array([right_zone, y_A, 0]),
                 color=C_SRC_A, stroke_width=2.8),
            Line(prism_tip, np.array([right_zone, y_B, 0]),
                 color=C_SRC_B, stroke_width=2.8),
            Line(prism_tip, np.array([right_zone, y_N, 0]),
                 color=C_SRC_BG, stroke_width=2.8),
        )
        out_lbls = VGroup(
            MathTex(r"\text{Source A}", font_size=18, color=C_SRC_A)
                .next_to(out_rays[0], RIGHT, buff=0.15),
            MathTex(r"\text{Source B}", font_size=18, color=C_SRC_B)
                .next_to(out_rays[1], RIGHT, buff=0.15),
            MathTex(r"\text{Background Noise}", font_size=18, color=C_SRC_BG)
                .next_to(out_rays[2], RIGHT, buff=0.15),
        )

        self.play(
            LaggedStart(*[Create(r) for r in out_rays], lag_ratio=0.2),
            LaggedStart(*[FadeIn(lb) for lb in out_lbls], lag_ratio=0.2),
            run_time=T_MED
        )

        note_4a = MathTex(
            r"\text{Blind Source Separation — No need to know the sources beforehand!}",
            font_size=22, color=C_HL
        ).move_to(DOWN * 3.30)
        self.play(FadeIn(note_4a), run_time=T_FAST)
        self.wait(1.5)

        # ── Xóa scene 4A ─────────────────────────────────────────────────
        group_4a = VGroup(
            sub_4a, src_A, src_B, src_N, lbl_A, lbl_B, lbl_N,
            wave_A, wave_B, wave_N, tensor_mix, axes_lbl,
            in_ray, prism, prism_lbl, out_rays, out_lbls, note_4a
        )
        self.play(
            group_4a.animate.set_opacity(0.0).scale(0.9),
            run_time=T_MED
        )

        # ═════════════════════════════════════════════════════════════════
        # SCENE 4B — NON-NEGATIVE TENSOR FACTORIZATION + COMPLETION
        # ═════════════════════════════════════════════════════════════════
        sub_4b = MathTex(
            r"\text{4B — Non-negative Tensor Factorization (NTF)}",
            font_size=26, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub_4b), run_time=T_FAST)

        # ── Khối dữ liệu khách hàng ─────────────────────────────────────
        data_block = dot_block(
            layers=5, rows=5, cols=5,
            color=BLUE_D, radius=0.07,
            h_buff=0.20, v_buff=0.20, depth=0.18
        ).move_to(np.array([-2.0, 0.2, 0])) # Dịch khối data sang trái thêm chút

        data_lbl = MathTex(
            r"\text{User} \times \text{Product} \times \text{Time}",
            font_size=18, color=C_SUB
        ).next_to(data_block, DOWN, buff=0.14)

        self.play(FadeIn(data_block, scale=0.8), FadeIn(data_lbl), run_time=T_MED)

        # ── Các ô dữ liệu bị thiếu ───────────────────────────────────────
        missing_indices = [(1, 0, 1), (2, 2, 3), (3, 1, 2), (4, 3, 1)]
        mark_missing_dots(data_block, missing_indices, C_MISSING, BG)
        
        missing_lbl = MathTex(
            r"\text{Missing Data}",
            font_size=18, color=C_MISSING
        ).next_to(data_block, UP, buff=0.3) # Tăng buff để chữ không dính vào khối

        self.play(FadeIn(missing_lbl), run_time=T_FAST)
        self.wait(0.4)

        # ── FIX KHOẢNG CÁCH: Tăng trục Y (1.1, 0.0, -1.1) ─────────────────
        factors = VGroup(
            Rectangle(width=1.8, height=0.30,
                      fill_color=C_NTF_1, fill_opacity=0.78, stroke_width=0)
                .move_to(np.array([1.0,  1.1, 0])),
            Rectangle(width=1.8, height=0.30,
                      fill_color=C_NTF_2, fill_opacity=0.78, stroke_width=0)
                .move_to(np.array([1.0,  0.0, 0])),
            Rectangle(width=1.8, height=0.30,
                      fill_color=C_NTF_3, fill_opacity=0.78, stroke_width=0)
                .move_to(np.array([1.0, -1.1, 0])),
        )

        f_lbls = VGroup(
            MathTex(r"\text{Teen/Game}", font_size=16, color=C_NTF_1)
                .next_to(factors[0], RIGHT, buff=0.15),
            MathTex(r"\text{Adult/Book}", font_size=16, color=C_NTF_2)
                .next_to(factors[1], RIGHT, buff=0.15),
            MathTex(r"\text{Tech/Promo}", font_size=16, color=C_NTF_3)
                .next_to(factors[2], RIGHT, buff=0.15),
        )

        nn_sign = MathTex(
            r"\text{Non-negative}",
            font_size=18, color=C_HL
        ).move_to(np.array([1.5, -1.80, 0])) # Đẩy chữ non-negative xuống thấp hơn

        self.play(data_block.animate.set_opacity(0.25), run_time=T_FAST)
        self.play(
            LaggedStart(*[FadeIn(f, shift=LEFT * 0.12) for f in factors],
                        lag_ratio=0.2),
            run_time=T_MED
        )
        self.play(FadeIn(f_lbls), FadeIn(nn_sign), run_time=T_FAST)

        note_ntf = MathTex(
            r"\text{Each factor has a real-world interpretation — no 'negative behavior'!}",
            font_size=22, color=C_HL
        ).move_to(DOWN * 3.30)
        self.play(FadeIn(note_ntf), run_time=T_FAST)
        self.wait(1.5)

        # ── Tensor Completion ────────────────────────────────────────────
        sub_4b_comp = MathTex(
            r"\text{Tensor Completion — Predicting missing data}",
            font_size=26, color=C_HL
        ).move_to(UP * 2.72)
        self.play(ReplacementTransform(sub_4b, sub_4b_comp), run_time=T_FAST)

        self.play(
            LaggedStart(*[
                f.animate.set_opacity(0.0).shift(RIGHT * 0.2)
                for f in factors
            ], lag_ratio=0.1),
            FadeOut(VGroup(f_lbls, nn_sign, note_ntf, missing_lbl)),
            data_block.animate.set_opacity(0.85),
            run_time=T_MED
        )

        # Hoạt ảnh lấp đầy data bằng màu Vàng sáng
        fill_animations = []
        for layer_idx, row_idx, col_idx in missing_indices:
            layer = data_block[layer_idx]
            dot_idx = row_idx * 5 + col_idx
            if dot_idx < len(layer):
                fill_animations.append(
                    layer[dot_idx].animate
                        .set_fill(color=C_FILLED, opacity=1.0)
                        .set_stroke(width=0)
                        .set_radius(0.14)
                )

        self.play(
            LaggedStart(*fill_animations, lag_ratio=0.35),
            run_time=T_MED
        )

        for layer_idx, row_idx, col_idx in missing_indices:
            layer = data_block[layer_idx]
            dot_idx = row_idx * 5 + col_idx
            if dot_idx < len(layer):
                self.play(Flash(layer[dot_idx].get_center(), color=C_FILLED,
                                flash_radius=0.22, line_length=0.1,
                                run_time=0.25))

        formula_comp = MathTex(
            r"\min_{\mathcal{X}}\ \|\mathcal{X}_\Omega - \mathcal{M}_\Omega\|_F^2 \quad \text{s.t.}\ \text{rank}(\mathcal{X}) \leq R",
            font_size=26, color=C_HL
        ).move_to(np.array([0.0, -2.00, 0]))

        note_comp = MathTex(
            r"\text{Only need 20\% of the data — can predict 80\% of the rest!}",
            font_size=22, color=C_OK
        ).move_to(DOWN * 3.30)

        self.play(Write(formula_comp), run_time=T_MED)
        self.play(FadeIn(note_comp), run_time=T_FAST)
        self.wait(1.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MED)