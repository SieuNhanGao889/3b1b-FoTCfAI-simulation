"""
scene_5_finale_v2.py
─────────────────────────────────────────────────────────────────────────────
SCENE 5: Tất cả Hội Tụ — Kết
Duration: ~90 giây  (Giây 11:30 – 13:00 theo script)

  5A — Tất cả hội tụ: Các icon từ mọi phần bay về trung tâm
       → tan rã thành công thức CP duy nhất phát sáng
  5B — Message cuối: "AI không phải phép màu. Nó là hình học."
       → Particles / gradient background → Thank-you card

PHONG CÁCH: Bám sát scene_1a
  • Tensor = lưới Dot (dot_block)
  • Mọi icon đều build từ primitive Manim
  • Công thức phát sáng với glow pulse
  • Closing card đẹp với RoundedRectangle
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────
BG          = "#0a0a1a"
C_TENSOR    = BLUE_D
C_VECTOR    = "#ffaa00"   # Vàng cam
C_MATRIX    = GREEN_C
C_HL        = YELLOW
C_SUB       = "#aaaacc"
C_CIRCUIT_S = BLUE_B     # Sum node
C_CIRCUIT_P = "#ff7744"  # Product node
C_PRISM     = "#7fd8ff"

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
    block = VGroup()
    for k in range(layers):
        layer = dot_grid(rows, cols, color=color,
                         radius=radius, h_buff=h_buff, v_buff=v_buff)
        layer.shift(RIGHT * depth * k + UP * depth * k)
        layer.set_opacity(1.0 - k * 0.50 / max(layers - 1, 1))
        block.add(layer)
    return block


def make_icon_tensor() -> VGroup:
    """Mini tensor icon (3×3×3 dot block)."""
    return dot_block(3, 3, 3, color=C_TENSOR,
                     radius=0.07, h_buff=0.19, v_buff=0.19, depth=0.15)


def make_icon_circuit() -> VGroup:
    """Mini circuit icon: 2 circles (sum / product) + connecting line."""
    s = Circle(radius=0.16, fill_color=C_CIRCUIT_S,
               fill_opacity=0.90, stroke_width=0)
    p = Circle(radius=0.16, fill_color=C_CIRCUIT_P,
               fill_opacity=0.90, stroke_width=0).shift(RIGHT * 0.65)
    wire = Line(s.get_right(), p.get_left(),
                color=C_SUB, stroke_width=1.6)
    s_lbl = MathTex(r"+", font_size=14, color=WHITE).move_to(s)
    p_lbl = MathTex(r"\times", font_size=14, color=WHITE).move_to(p)
    return VGroup(s, p, wire, s_lbl, p_lbl)


def make_icon_cp() -> VGroup:
    """Mini CP icon: 3 vector bars (a ∘ b ∘ c)."""
    a = Rectangle(width=0.18, height=0.75,
                  fill_color=C_VECTOR, fill_opacity=0.85, stroke_width=0)
    b = Rectangle(width=0.75, height=0.18,
                  fill_color=C_MATRIX, fill_opacity=0.85, stroke_width=0)
    c = Rectangle(width=0.18, height=0.55,
                  fill_color=BLUE_C, fill_opacity=0.85, stroke_width=0)
    return VGroup(a, b, c).arrange(RIGHT, buff=0.10)


def make_icon_prism() -> VGroup:
    """Mini prism (triangle) icon."""
    return Polygon(
        np.array([0.0,  0.45, 0]),
        np.array([-0.40, -0.30, 0]),
        np.array([ 0.40, -0.30, 0]),
        fill_color=C_PRISM, fill_opacity=0.28,
        stroke_color=C_PRISM, stroke_width=1.8
    )


class Finale(Scene):
    # ─────────────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG

        # ── Main title ────────────────────────────────────────────────────
        title = MathTex(
            r"\text{All Together — A Unified Framework}",
            font_size=42, color=C_HL
        ).move_to(UP * 3.40)
        sub = MathTex(
            r"\text{One principle, infinite applications }",
            font_size=26, color=C_SUB
        ).move_to(UP * 2.72)
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(sub), run_time=T_FAST)

        # ═════════════════════════════════════════════════════════════════
        # PHASE 5A — CÁC ICON BAY VỀ TRUNG TÂM
        # ═════════════════════════════════════════════════════════════════
        # Tạo 4 icon ở 4 góc
        icon_tensor  = make_icon_tensor() .move_to(np.array([-4.0,  1.5, 0]))
        icon_cp      = make_icon_cp()     .move_to(np.array([ 4.0,  1.5, 0]))
        icon_circuit = make_icon_circuit().move_to(np.array([-4.0, -1.5, 0]))
        icon_prism   = make_icon_prism()  .move_to(np.array([ 4.0, -1.5, 0]))

        lbl_tensor   = MathTex(r"\text{Tensor}", font_size=18, color=C_TENSOR)\
            .next_to(icon_tensor, DOWN, buff=0.10)
        lbl_cp       = MathTex(r"\text{CP Decomp}", font_size=18, color=C_VECTOR)\
            .next_to(icon_cp, DOWN, buff=0.10)
        lbl_circuit  = MathTex(r"\text{Circuit}", font_size=18, color=C_CIRCUIT_S)\
            .next_to(icon_circuit, DOWN, buff=0.10)
        lbl_prism    = MathTex(r"\text{Data Mining}", font_size=18, color=C_PRISM)\
            .next_to(icon_prism, DOWN, buff=0.10)

        self.play(
            LaggedStart(
                FadeIn(icon_tensor,  scale=0.7),
                FadeIn(icon_cp,      scale=0.7),
                FadeIn(icon_circuit, scale=0.7),
                FadeIn(icon_prism,   scale=0.7),
                lag_ratio=0.18
            ),
            LaggedStart(
                FadeIn(lbl_tensor), FadeIn(lbl_cp),
                FadeIn(lbl_circuit), FadeIn(lbl_prism),
                lag_ratio=0.18
            ),
            run_time=T_MED
        )
        self.wait(0.5)

        # Tất cả bay về trung tâm và thu nhỏ
        CENTER = np.array([0, 0.1, 0])
        self.play(
            *[icon.animate.move_to(CENTER).scale(0.12)
              for icon in [icon_tensor, icon_cp, icon_circuit, icon_prism]],
            *[FadeOut(lbl) for lbl in [lbl_tensor, lbl_cp, lbl_circuit, lbl_prism]],
            run_time=T_SLOW
        )
        self.play(
            FadeOut(VGroup(icon_tensor, icon_cp, icon_circuit, icon_prism)),
            run_time=T_FAST
        )

        # ═════════════════════════════════════════════════════════════════
        # CÔNG THỨC CP PHÁT SÁNG
        # ═════════════════════════════════════════════════════════════════
        formula = MathTex(
            r"\mathcal{X} \;\approx\; \sum_{r=1}^{R}\; a_r \circ b_r \circ c_r",
            font_size=58, color=C_HL
        ).move_to(np.array([0, 0.30, 0]))

        sub_formula = MathTex(
            r"\text{Low-rank decomposition: Complexity from simple components}",
            font_size=22, color=C_SUB
        ).next_to(formula, DOWN, buff=0.45)

        self.play(Write(formula), run_time=T_SLOW)
        self.play(FadeIn(sub_formula), run_time=T_FAST)

        # Glow pulse (2 lần)
        for _ in range(2):
            glow = formula.copy().set_stroke(C_HL, width=10, opacity=0.22)
            self.play(FadeIn(glow), run_time=0.32)
            self.play(FadeOut(glow), run_time=0.32)

        self.wait(0.8)
        self.play(FadeOut(VGroup(sub, formula, sub_formula)), run_time=T_MED)

        # ═════════════════════════════════════════════════════════════════
        # PHASE 5B — MESSAGE CUỐI
        # ═════════════════════════════════════════════════════════════════
        sub_close = MathTex(
            r"\text{Closing}",
            font_size=26, color=C_HL
        ).move_to(UP * 2.72)
        self.play(FadeIn(sub_close), run_time=T_FAST)

        # Các dòng message xuất hiện từng dòng
        messages = [
            (r"\text{AI is not magic.}",         34, WHITE),
            (r"\text{It is geometry.}",          34, C_TENSOR),
            (r"\text{Tensors are the way we structure the universe of data.}", 26, C_VECTOR),
            (r"\text{Low-Rank is the way we find hidden essences.}",           26, C_HL),
        ]

        msg_group = VGroup()
        for i, (tex, fs, col) in enumerate(messages):
            line = MathTex(tex, font_size=fs, color=col)\
                .move_to(np.array([0, 1.4 - i * 0.85, 0]))
            self.play(FadeIn(line, shift=UP * 0.08), run_time=T_MED)
            self.wait(0.22)
            msg_group.add(line)

        # ── Gradient ambience background ──────────────────────────────────
        grad_strips = VGroup(*[
            Rectangle(
                width=16, height=0.50,
                fill_color=interpolate_color(
                    ManimColor(BG), ManimColor("#001830"), i / 18
                ),
                fill_opacity=0.10, stroke_width=0
            ).shift(DOWN * (4.5 - i * 0.50))
            for i in range(18)
        ])
        self.play(FadeIn(grad_strips), run_time=T_SLOW)

        # ── Particles ─────────────────────────────────────────────────────
        rng = np.random.default_rng(seed=77)
        particles = VGroup(*[
            Dot(
                np.array([rng.uniform(-6.2, 6.2),
                          rng.uniform(-3.8, 3.2), 0]),
                radius=rng.uniform(0.018, 0.052),
                color=C_HL,
                fill_opacity=rng.uniform(0.20, 0.55)
            )
            for _ in range(32)
        ])
        self.play(
            LaggedStart(*[GrowFromCenter(p) for p in particles], lag_ratio=0.025),
            run_time=T_MED
        )
        self.wait(0.4)

        # ── Thank-you card ────────────────────────────────────────────────
        thanks_box = RoundedRectangle(
            corner_radius=0.24,
            width=9.2, height=2.80,
            fill_color="#07071a", fill_opacity=0.96,
            stroke_color=C_HL, stroke_width=1.8
        ).move_to(np.array([0, -1.70, 0]))

        thanks_line1 = MathTex(
            r"\text{Thank you, Professor and everyone for joining us on this journey!}",
            font_size=28, color=WHITE
        ).move_to(thanks_box.get_center() + UP * 0.52)

        thanks_line2 = MathTex(
            r"\text{Exploring Tensors — The }\ \mathbf{TensorTeam}",
            font_size=22, color=C_HL
        ).move_to(thanks_box.get_center() + UP * 0.02)

        # Công thức nhỏ bên dưới
        thanks_formula = MathTex(
            r"\mathcal{X} \approx \sum_{r=1}^{R} a_r \circ b_r \circ c_r",
            font_size=20, color=C_SUB
        ).move_to(thanks_box.get_center() + DOWN * 0.60)

        self.play(FadeIn(thanks_box, scale=0.88), run_time=T_MED)
        self.play(FadeIn(thanks_line1), run_time=T_FAST)
        self.play(FadeIn(thanks_line2), run_time=T_FAST)
        self.play(FadeIn(thanks_formula), run_time=T_FAST)

        # Final glow trên card
        card_glow = thanks_box.copy().set_stroke(C_HL, width=10, opacity=0.15)
        self.play(FadeIn(card_glow), run_time=0.40)
        self.play(FadeOut(card_glow), run_time=0.40)

        self.wait(2.2)

        # ═════════════════════════════════════════════════════════════════
        # FADE TO BLACK
        # ═════════════════════════════════════════════════════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=T_SLOW)