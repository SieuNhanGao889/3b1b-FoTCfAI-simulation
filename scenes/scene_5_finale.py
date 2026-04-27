"""
scenes/scene_5_finale.py
─────────────────────────────────────────────────────────────────────────────
SCENE 5A  "Tất cả hội tụ"   (11:30 – 12:15)
SCENE 5B  "Message cuối"     (12:15 – 13:00)

- Tất cả icons từ mọi phần bay về trung tâm, tan thành công thức
- Closing poetry text + gradient background fade-in
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from config import *
from utils.tensor_objects import Tensor3D


class Finale(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ════════════════════════════════════════════════════════════════
        # SCENE 5A – Everything converges
        # ════════════════════════════════════════════════════════════════

        # ── Spawn representatives from all previous parts ─────────────────

        # Part 1 – Tensor block
        block = Tensor3D(nx=4, ny=3, nz=4, cell_size=0.22,
                         face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block.move_to(LEFT * 5.0 + UP * 2.5)

        # Part 2 – CP factor vectors (3 thin bars)
        cp_grp = VGroup(
            Rectangle(width=0.2, height=1.0, fill_color=VECTOR_COLOR,
                      fill_opacity=0.85, stroke_width=0),
            Rectangle(width=1.0, height=0.2, fill_color=MATRIX_COLOR,
                      fill_opacity=0.85, stroke_width=0),
            Rectangle(width=0.2, height=0.65, fill_color=TENSOR_EDGE_COLOR,
                      fill_opacity=0.85, stroke_width=0),
        ).arrange(RIGHT, buff=0.15).move_to(RIGHT * 5.0 + UP * 2.5)

        # Part 3 – Circuit nodes
        def _node(color, symbol):
            c = Circle(radius=0.22, fill_color=color,
                       fill_opacity=0.85, stroke_width=0)
            t = Text(symbol, font_size=18, color=BLACK)
            return VGroup(c, t)

        circuit_grp = VGroup(
            _node(SUM_NODE_COLOR, "+"),
            _node(PRODUCT_NODE_COLOR, r"\times"),
        ).arrange(RIGHT, buff=0.2).move_to(LEFT * 5.0 + DOWN * 2.5)

        # Part 4 – Prism (lăng kính)
        prism = Triangle(fill_color="#aaddff", fill_opacity=0.35,
                         stroke_color="#aaddff", stroke_width=2).scale(0.5)
        prism.move_to(RIGHT * 5.0 + DOWN * 2.5)

        all_icons = VGroup(block, cp_grp, circuit_grp, prism)
        self.play(
            LaggedStart(*[FadeIn(ic, scale=0.6) for ic in all_icons], lag_ratio=0.2),
            run_time=T_SLOW,
        )
        self.wait(0.4)

        # ── All fly to center and shrink ──────────────────────────────────
        self.play(
            *[ic.animate.move_to(ORIGIN).scale(0.1) for ic in all_icons],
            run_time=T_SLOW,
            rate_func=rush_into,
        )
        self.play(FadeOut(all_icons), run_time=T_FAST)

        # ── Core formula materializes ─────────────────────────────────────
        formula = Text("T ≈ Σ(r=1..R)  aᵣ ∘ bᵣ ∘ cᵣ",
            font_size=46, color=HIGHLIGHT_COLOR,
        )
        self.play(Write(formula), run_time=T_SLOW)

        # Glow pulse
        glow = formula.copy().set_stroke(HIGHLIGHT_COLOR, width=8, opacity=0.25)
        self.play(FadeIn(glow, scale=1.05), run_time=0.4)
        self.play(FadeOut(glow), run_time=0.4)

        sub_formula = Text(
            "Sự phức tạp được xây dựng từ những thành phần đơn giản",
            font_size=19, color=SUBTITLE_COLOR,
        ).next_to(formula, DOWN, buff=0.35)
        self.play(FadeIn(sub_formula, shift=UP * 0.1), run_time=T_MEDIUM)
        self.wait(1.2)

        # Particle burst around formula
        particles = VGroup(*[
            Dot(
                formula.get_center()
                + np.array([np.cos(a) * 2.8, np.sin(a) * 1.4, 0]),
                radius=0.05,
                color=HIGHLIGHT_COLOR,
                fill_opacity=0.7,
            )
            for a in np.linspace(0, TAU, 18, endpoint=False)
        ])
        self.play(
            LaggedStart(*[GrowFromCenter(p) for p in particles], lag_ratio=0.04),
            run_time=T_MEDIUM,
        )
        self.play(
            *[p.animate.scale(0).set_opacity(0) for p in particles],
            run_time=T_MEDIUM,
        )

        self.play(FadeOut(VGroup(formula, sub_formula)), run_time=T_MEDIUM)

        # ════════════════════════════════════════════════════════════════
        # SCENE 5B – Closing message
        # ════════════════════════════════════════════════════════════════

        # ── Poetic closing lines ──────────────────────────────────────────
        lines_data = [
            ("AI không phải phép màu.",          WHITE),
            ("Nó là hình học.",                   TENSOR_EDGE_COLOR),
            ("Tensor là cách ta cấu trúc hóa\nvũ trụ dữ liệu.",  VECTOR_COLOR),
            ("Low-Rank là cách ta tìm ra\nbản chất ẩn sau sự phức tạp.", HIGHLIGHT_COLOR),
        ]
        line_mobs = []
        y_start = UP * 1.8
        for i, (txt, col) in enumerate(lines_data):
            mob = Text(txt, font_size=22, color=col,
                       line_spacing=0.5, weight=BOLD if i > 0 else NORMAL)
            mob.move_to(y_start + DOWN * i * 0.95)
            line_mobs.append(mob)

        for mob in line_mobs:
            self.play(FadeIn(mob, shift=UP * 0.1), run_time=T_MEDIUM)
            self.wait(0.6)

        # ── Background gradient sweep ─────────────────────────────────────
        # Simulate gradient: stacked semi-transparent rectangles
        grad_rects = VGroup(*[
            Rectangle(
                width=16, height=0.5,
                fill_color=interpolate_color(BG_COLOR, "#001133",
                                             i / 18),
                fill_opacity=0.06,
                stroke_width=0,
            ).shift(DOWN * (4.5 - i * 0.5))
            for i in range(18)
        ])
        self.play(FadeIn(grad_rects), run_time=T_SLOW)

        # Floating particles
        rng = np.random.default_rng(99)
        float_particles = VGroup(*[
            Dot(
                np.array([rng.uniform(-6.5, 6.5),
                          rng.uniform(-4.0, 4.0), 0]),
                radius=rng.uniform(0.02, 0.07),
                color=HIGHLIGHT_COLOR,
                fill_opacity=rng.uniform(0.3, 0.7),
            )
            for _ in range(30)
        ])
        self.play(
            LaggedStart(*[GrowFromCenter(p) for p in float_particles], lag_ratio=0.04),
            run_time=T_SLOW,
        )

        # ── Thank-you card ────────────────────────────────────────────────
        self.play(
            *[mob.animate.shift(UP * 0.4).set_opacity(0.3)
              for mob in line_mobs],
            run_time=T_MEDIUM,
        )

        ty_box = RoundedRectangle(
            corner_radius=0.25, width=8.5, height=2.8,
            fill_color="#050515", fill_opacity=0.92,
            stroke_color=HIGHLIGHT_COLOR, stroke_width=1.8,
        ).shift(DOWN * 0.3)

        ty_text = Text(
            "Cảm ơn thầy và các bạn đã đồng hành cùng\nnhóm chúng mình trong hành trình khám phá Tensor",
            font_size=20, color=WHITE, line_spacing=0.55,
        ).move_to(ty_box.get_center() + UP * 0.35)

        team_text = Text(
            "Nhóm NeurIPS Tutorial – Tensors in AI",
            font_size=16, color=HIGHLIGHT_COLOR,
        ).next_to(ty_text, DOWN, buff=0.3)

        # Decorative stars
        stars = VGroup(*[
            Text("✦", font_size=16, color=HIGHLIGHT_COLOR).move_to(
                ty_box.get_center() + RIGHT * (-2.5 + i * 1.25) + DOWN * 1.1
            )
            for i in range(5)
        ])

        self.play(FadeIn(ty_box, scale=0.9), run_time=T_MEDIUM)
        self.play(FadeIn(ty_text, shift=UP * 0.05), run_time=T_MEDIUM)
        self.play(FadeIn(team_text), run_time=T_FAST)
        self.play(
            LaggedStart(*[GrowFromCenter(s) for s in stars], lag_ratio=0.15),
            run_time=T_MEDIUM,
        )

        # Final glow on the box border
        self.play(
            ty_box.animate.set_stroke(HIGHLIGHT_COLOR, width=3.0),
            run_time=0.5,
        )
        self.play(
            ty_box.animate.set_stroke(HIGHLIGHT_COLOR, width=1.8),
            run_time=0.5,
        )

        self.wait(2.5)

        # ── Graceful fade to black ────────────────────────────────────────
        everything = VGroup(
            *line_mobs, grad_rects, float_particles,
            ty_box, ty_text, team_text, stars,
        )
        self.play(FadeOut(everything, run_time=T_SLOW))
        self.wait(0.5)
