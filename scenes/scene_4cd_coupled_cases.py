"""
scene_4cd_coupled_cases_v2.py
─────────────────────────────────────────────────────────────────────────────
SCENE 4C + 4D: Coupled Tensor Factorization & Case Studies Flash
Duration: ~90 giây  (Giây 10:00 – 11:30 theo script)

  4C — Coupled Factorization: Tensor (3D) + Matrix (2D) chia sẻ factor
  4D — Case flash: Y tế / Mạng xã hội / Giao thông

PHONG CÁCH: Bám sát scene_1a
  • Tensor = lưới Dot xếp lớp (không dùng Tensor3D class)
  • Matrix 2D = lưới Dot phẳng
  • Shared factor = sợi dây phát sáng + animation dòng chảy
  • Card flash = RoundedRectangle + Flash effect
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────
BG          = "#0a0a1a"
C_TENSOR    = BLUE_D
C_MATRIX    = GREEN_C
C_SHARED    = YELLOW
C_HL        = YELLOW
C_SUB       = "#aaaacc"
C_CARD_BG   = "#0d0d22"

T_SLOW  = 2.0
T_MED   = 1.2
T_FAST  = 0.5

# ── Helpers ───────────────────────────────────────────────────────────────
def dot_grid(rows, cols, color=BLUE_D, radius=0.07,
             h_buff=0.21, v_buff=0.21) -> VGroup:
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=radius, color=color)
            d.move_to(RIGHT * c * h_buff + DOWN * r * v_buff)
            g.add(d)
    return g


def dot_block(layers, rows, cols, color=BLUE_D, radius=0.07,
              h_buff=0.20, v_buff=0.20, depth=0.17) -> VGroup:
    """Giả 3-D: lưới Dot nhiều lớp xếp chéo, opacity giảm dần."""
    block = VGroup()
    for k in range(layers):
        layer = dot_grid(rows, cols, color=color,
                         radius=radius, h_buff=h_buff, v_buff=v_buff)
        layer.shift(RIGHT * depth * k + UP * depth * k)
        layer.set_opacity(1.0 - k * 0.50 / max(layers - 1, 1))
        block.add(layer)
    return block


class CoupledAndCases(Scene):
    # ─────────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG

        # ── Main title ────────────────────────────────────────────────────
        title = MathTex(
            r"\text{Coupled Tensor Factorization \& Case Studies}",
            font_size=36, color=C_HL
        ).move_to(UP * 3.40)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=T_FAST)

        # ═════════════════════════════════════════════════════════════════
        # SCENE 4C — COUPLED FACTORIZATION
        # ═════════════════════════════════════════════════════════════════
        sub_4c = MathTex(
            r"\text{4C — Coupled Factorization: Multi-Modal, Shared Factor}",
            font_size=26, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub_4c), run_time=T_FAST)

        # ── Tensor 3D bên trái (User × Action × Time) ────────────────────
        tensor_3d = dot_block(
            layers=4, rows=4, cols=4,
            color=C_TENSOR, radius=0.075,
            h_buff=0.21, v_buff=0.21, depth=0.20
        ).move_to(np.array([-3.6, 0.3, 0]))

        t3_lbl = MathTex(
            r"\text{User} \times \text{Action} \times \text{Time}",
            font_size=17, color=C_TENSOR
        ).next_to(tensor_3d, DOWN, buff=0.14)

        t3_title = MathTex(r"\text{Tensor } \mathcal{T}", font_size=20, color=C_TENSOR)\
            .next_to(tensor_3d, UP, buff=0.10)

        # ── Matrix 2D bên phải (User × Demographics) ─────────────────────
        matrix_2d = dot_grid(
            rows=4, cols=5,
            color=C_MATRIX, radius=0.09,
            h_buff=0.26, v_buff=0.26
        ).move_to(np.array([3.2, 0.2, 0]))

        m2_lbl = MathTex(
            r"\text{User} \times \text{Demographics}",
            font_size=17, color=C_MATRIX
        ).next_to(matrix_2d, DOWN, buff=0.14)

        m2_title = MathTex(r"\text{Matrix } M", font_size=20, color=C_MATRIX)\
            .next_to(matrix_2d, UP, buff=0.10)

        self.play(
            FadeIn(tensor_3d, scale=0.8),
            FadeIn(t3_lbl), FadeIn(t3_title),
            run_time=T_MED
        )
        self.play(
            FadeIn(matrix_2d, scale=0.8),
            FadeIn(m2_lbl), FadeIn(m2_title),
            run_time=T_MED
        )
        self.wait(0.4)

        # ── Factorization → Factor matrices xuất hiện ────────────────────
        # Factor "User" từ tensor
        lf_tensor = Rectangle(
            width=0.26, height=1.2,
            fill_color=C_SHARED, fill_opacity=0.88, stroke_width=0
        ).move_to(np.array([-1.45, 0.4, 0]))

        lbl_lf_t = MathTex(r"U_{\text{user}}", font_size=18, color=C_SHARED)\
            .next_to(lf_tensor, UP, buff=0.07)

        # Factor "User" từ matrix
        lf_matrix = Rectangle(
            width=0.26, height=1.2,
            fill_color=C_SHARED, fill_opacity=0.88, stroke_width=0
        ).move_to(np.array([1.45, 0.4, 0]))

        lbl_lf_m = MathTex(r"U_{\text{user}}", font_size=18, color=C_SHARED)\
            .next_to(lf_matrix, UP, buff=0.07)

        self.play(
            ReplacementTransform(tensor_3d.copy(), lf_tensor),
            ReplacementTransform(matrix_2d.copy(), lf_matrix),
            FadeIn(lbl_lf_t), FadeIn(lbl_lf_m),
            run_time=T_MED
        )

        # ── Dây kết nối (shared factor) ──────────────────────────────────
        wire_glow = Line(
            lf_tensor.get_right(), lf_matrix.get_left(),
            color=C_SHARED, stroke_width=9, stroke_opacity=0.18
        )
        wire = Line(
            lf_tensor.get_right(), lf_matrix.get_left(),
            color=C_SHARED, stroke_width=2.8
        )
        equal_lbl = MathTex(r"=\ \text{shared!}", font_size=20, color=C_SHARED)\
            .move_to(np.array([0.0, 0.95, 0]))

        self.play(Create(wire_glow), Create(wire), FadeIn(equal_lbl), run_time=T_FAST)

        # ── Dòng chảy thông tin qua dây ───────────────────────────────────
        # Dot chạy T→M rồi M→T
        flow_dot_1 = Dot(lf_tensor.get_right(), color=C_SHARED, radius=0.09)
        flow_dot_2 = Dot(lf_matrix.get_left(), color=C_MATRIX, radius=0.09)

        self.play(GrowFromCenter(flow_dot_1), run_time=T_FAST)
        self.play(
            flow_dot_1.animate.move_to(lf_matrix.get_left()),
            run_time=T_MED
        )
        self.play(FadeOut(flow_dot_1), run_time=T_FAST)
        self.play(GrowFromCenter(flow_dot_2), run_time=T_FAST)
        self.play(
            flow_dot_2.animate.move_to(lf_tensor.get_right()),
            run_time=T_MED
        )
        self.play(FadeOut(flow_dot_2), run_time=T_FAST)

        note_4c = MathTex(
            r"\text{Information 'flows' through the shared factor — Understand users from multiple perspectives!}",
            font_size=21, color=C_HL
        ).move_to(DOWN * 3.30)
        self.play(FadeIn(note_4c), run_time=T_FAST)

        # Công thức
        formula_4c = MathTex(
            r"\min\ \|\mathcal{T} - [U, V, W]\|^2 + \lambda\|M - U D^T\|^2",
            font_size=26, color=C_HL
        ).move_to(np.array([0, -1.70, 0]))
        self.play(Write(formula_4c), run_time=T_MED)
        self.wait(1.0)

        # ── Xóa 4C ───────────────────────────────────────────────────────
        group_4c = VGroup(
            sub_4c, tensor_3d, t3_lbl, t3_title,
            matrix_2d, m2_lbl, m2_title,
            lf_tensor, lf_matrix, lbl_lf_t, lbl_lf_m,
            wire_glow, wire, equal_lbl, note_4c, formula_4c
        )
        self.play(FadeOut(group_4c), run_time=T_FAST)

        # ═════════════════════════════════════════════════════════════════
        # SCENE 4D — CASE STUDIES FLASH
        # ═════════════════════════════════════════════════════════════════
        sub_4d = MathTex(
            r"\text{4D — A lens, all domains}",
            font_size=26, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub_4d), run_time=T_FAST)

        # Dữ liệu cho từng card
        cases = [
            {
                "domain":  r"\text{Healthcare}",
                "tensor":  r"\text{Patient} \times \text{Symptom} \times \text{Time}",
                "result":  r"\text{Detecting hidden diseases from electronic records}",
                "icon":    r"\heartsuit",
                "color":   RED_C,
            },
            {
                "domain":  r"\text{Social Media}",
                "tensor":  r"\text{User} \times \text{Hashtag} \times \text{Time}",
                "result":  r"\text{Detecting trends \& communities}",
                "icon":    r"\bigstar",
                "color":   BLUE_B,
            },
            {
                "domain":  r"\text{Transportation}",
                "tensor":  r"\text{Location} \times \text{Flow} \times \text{Time}",
                "result":  r"\text{Real-time traffic congestion prediction}",
                "icon":    r"\rightarrow",
                "color":   GREEN_C,
            },
        ]

        for case in cases:
            col = case["color"]

            # Card background
            card = RoundedRectangle(
                corner_radius=0.20,
                width=8.0, height=2.60,
                fill_color=C_CARD_BG, fill_opacity=1.0,
                stroke_color=col, stroke_width=2.2
            ).move_to(np.array([0, -0.10, 0]))

            # Tensor mini (3 lớp) bên trái trong card
            mini_block = dot_block(
                layers=3, rows=3, cols=3,
                color=col, radius=0.055,
                h_buff=0.18, v_buff=0.18, depth=0.14
            ).move_to(np.array([-2.9, -0.10, 0]))

            # Icon lĩnh vực
            icon = MathTex(case["icon"], font_size=40, color=col)\
                .move_to(np.array([-1.0, 0.55, 0]))

            # Text domain
            domain_tex = MathTex(case["domain"], font_size=28, color=col)\
                .move_to(np.array([1.0, 0.55, 0]))

            # Tensor axes label
            tensor_tex = MathTex(case["tensor"], font_size=18, color=C_SUB)\
                .move_to(np.array([1.0, -0.02, 0]))

            # Result
            result_tex = MathTex(case["result"], font_size=20, color=col)\
                .move_to(np.array([1.0, -0.65, 0]))

            card_grp = VGroup(card, mini_block, icon, domain_tex,
                              tensor_tex, result_tex)

            self.play(FadeIn(card_grp, shift=UP * 0.12), run_time=T_MED)

            # Flash trên icon
            self.play(
                Flash(icon.get_center(), color=col,
                      flash_radius=0.40, line_length=0.12,
                      run_time=T_FAST)
            )

            # Highlight tensor mini: các dot sáng lên tuần tự
            for layer in mini_block:
                self.play(
                    layer.animate.set_color(WHITE).set_opacity(0.9),
                    run_time=0.15
                )
                self.play(
                    layer.animate.set_color(col).set_opacity(1.0),
                    run_time=0.12
                )

            self.wait(0.55)
            self.play(FadeOut(card_grp), run_time=T_FAST)

        # ── Closing message ───────────────────────────────────────────────
        close_msg = MathTex(
            r"\textbf{A Tensor Lens — Infinite Applications}",
            font_size=34, color=C_HL
        ).move_to(np.array([0, 0.5, 0]))

        sub_close = MathTex(
            r"\text{Healthcare} \cdot \text{Social Media} \cdot \text{Transportation} \cdot \ldots",
            font_size=24, color=C_SUB
        ).next_to(close_msg, DOWN, buff=0.35)

        note_final = MathTex(
            r"\text{Any multi-dimensional data can be decoded with Tensors!}",
            font_size=22, color=C_SUB
        ).move_to(DOWN * 3.30)

        self.play(FadeIn(close_msg, scale=0.85), run_time=T_MED)
        self.play(FadeIn(sub_close), run_time=T_FAST)
        self.play(FadeIn(note_final), run_time=T_FAST)
        self.wait(1.2)

        # ═════════════════════════════════════════════════════════════════
        # OUTRO
        # ═════════════════════════════════════════════════════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=T_MED)