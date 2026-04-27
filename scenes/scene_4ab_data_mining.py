"""
scenes/scene_4ab_data_mining.py
─────────────────────────────────────────────────────────────────────────────
SCENE 4A  "Bài toán bữa tiệc – Blind Source Separation"  (8:30 – 9:15)
SCENE 4B  "Non-negative Tensor Factorization + Completion"  (9:15 – 10:00)
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
import numpy as np
from config import *
from utils.tensor_objects import Tensor3D


class DataMiningAB(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ════════════════════════════════════════════════════════════════
        # SCENE 4A – Cocktail party / Blind Source Separation
        # ════════════════════════════════════════════════════════════════

        title = Text("Tensor Factorization như một chiếc lăng kính",
                     font_size=21, color=HIGHLIGHT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=T_FAST)

        # ── People icons (abstract circles + sound waves) ─────────────────
        icons = VGroup(
            self._person_icon(LEFT * 4.5 + UP * 0.5,  "#ff8888"),
            self._person_icon(LEFT * 3.3 + DOWN * 0.3, "#88ff88"),
            self._person_icon(LEFT * 4.0 + DOWN * 1.0, "#8888ff"),
        )
        # Mixed waveforms → chaotic blob
        mixed_wave = self._wave_group(ORIGIN + LEFT * 1.0, mix=True)
        mic_icon = Text("🎤", font_size=28).shift(LEFT * 1.8 + DOWN * 0.2)

        self.play(
            LaggedStart(*[GrowFromCenter(ic) for ic in icons], lag_ratio=0.2),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(mic_icon), Create(mixed_wave), run_time=T_MEDIUM)

        vo1 = Text("Nhiều nguồn âm trộn lẫn → làm sao tách từng giọng?",
                   font_size=17, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(vo1), run_time=T_FAST)
        self.wait(0.5)
        self.play(FadeOut(vo1), run_time=T_FAST)

        # ── Tensor block (Frequency × Time × Mic) ────────────────────────
        tensor_mix = Tensor3D(nx=5, ny=4, nz=4, cell_size=0.26,
                              face_color="#334455", edge_color=TENSOR_EDGE_COLOR)
        tensor_mix.shift(RIGHT * 1.8)

        ax_lbls = VGroup(
            Text("Frequency", font_size=13, color=VECTOR_COLOR),
            Text("Time",      font_size=13, color=MATRIX_COLOR),
            Text("Mic",       font_size=13, color=TENSOR_EDGE_COLOR),
        )
        ax_lbls[0].next_to(tensor_mix, DOWN + LEFT, buff=0.05).shift(LEFT * 0.3)
        ax_lbls[1].next_to(tensor_mix, LEFT,        buff=0.08)
        ax_lbls[2].next_to(tensor_mix, UP + LEFT,   buff=0.05)

        self.play(FadeIn(tensor_mix, scale=0.7), FadeIn(ax_lbls), run_time=T_MEDIUM)
        self.wait(0.3)

        # ── Prism → separated rays ────────────────────────────────────────
        prism = Triangle(fill_color="#aaddff", fill_opacity=0.3,
                         stroke_color="#aaddff", stroke_width=2)
        prism.scale(0.6).shift(RIGHT * 4.2)

        ray_in = Line(tensor_mix.get_right(), prism.get_left(),
                      color=WHITE, stroke_width=2)

        ray_colors = ["#ff8888", "#88ff88", "#8888ff"]
        ray_labels = ["Giọng A", "Giọng B", "Nhạc nền"]
        rays_out = VGroup()
        for i, (col, lbl_str) in enumerate(zip(ray_colors, ray_labels)):
            end = prism.get_right() + RIGHT * 1.2 + UP * (1 - i) * 0.55
            ray = Line(prism.get_right(), end, color=col, stroke_width=2.5)
            lbl = Text(lbl_str, font_size=13, color=col).next_to(end, RIGHT, buff=0.08)
            rays_out.add(VGroup(ray, lbl))

        self.play(Create(ray_in), FadeIn(prism), run_time=T_FAST)
        self.play(
            LaggedStart(*[Create(r) for r in rays_out], lag_ratio=0.25),
            run_time=T_MEDIUM,
        )

        bss_lbl = Text("Blind Source Separation via Tensor Factorization",
                       font_size=16, color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(bss_lbl), run_time=T_FAST)
        self.wait(1.0)

        self.play(FadeOut(VGroup(icons, mixed_wave, mic_icon, tensor_mix, ax_lbls,
                                 ray_in, prism, rays_out, bss_lbl, title)),
                  run_time=T_FAST)

        # ════════════════════════════════════════════════════════════════
        # SCENE 4B – NTF + Tensor Completion
        # ════════════════════════════════════════════════════════════════

        title2 = Text("Non-negative Tensor Factorization  (NTF)",
                      font_size=21, color=HIGHLIGHT_COLOR, weight=BOLD)
        title2.to_edge(UP, buff=0.3)
        self.play(FadeIn(title2), run_time=T_FAST)

        # ── Customer tensor (User × Product × Time) ───────────────────────
        cust_block = Tensor3D(nx=5, ny=4, nz=5, cell_size=0.27,
                              face_color="#223344", edge_color=TENSOR_EDGE_COLOR)
        cust_block.shift(LEFT * 3.5)
        c_ax = VGroup(
            Text("User",    font_size=13, color=VECTOR_COLOR),
            Text("Product", font_size=13, color=MATRIX_COLOR),
            Text("Time",    font_size=13, color=TENSOR_EDGE_COLOR),
        )
        c_ax[0].next_to(cust_block, DOWN + LEFT, buff=0.05).shift(LEFT * 0.2)
        c_ax[1].next_to(cust_block, LEFT, buff=0.08)
        c_ax[2].next_to(cust_block, UP + LEFT, buff=0.05)

        # Some "missing" cells shown as grey patches
        missing_cells = VGroup(*[
            Square(side_length=0.27,
                   fill_color="#333333", fill_opacity=0.95,
                   stroke_color="#555555", stroke_width=0.5
                   ).move_to(cust_block.get_center() +
                              RIGHT * 0.3 * (i - 1) + UP * 0.3 * (j - 1))
            for i, j in [(0, 0), (1, -1), (-1, 1), (2, 0), (-2, -1)]
        ])

        self.play(FadeIn(cust_block, scale=0.7), FadeIn(c_ax), run_time=T_MEDIUM)
        self.play(FadeIn(missing_cells), run_time=T_FAST)

        missing_lbl = Text("Dữ liệu còn thiếu (ô xám)", font_size=15,
                           color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(missing_lbl), run_time=T_FAST)
        self.wait(0.5)
        self.play(FadeOut(missing_lbl), run_time=T_FAST)

        # ── Factorize → 3 colored "behavior" slices ───────────────────────
        pieces_data = [
            ("#cc3333", "#ff6666", "Teen mua game\ncuối tuần"),
            ("#1166aa", "#33aaff", "Trung niên mua sách\nbuổi sáng"),
            ("#aaaa00", "#ffff44", "Đồ tech – Black Friday"),
        ]
        pieces = VGroup()
        for i, (fc, ec, lbl_str) in enumerate(pieces_data):
            slab = Rectangle(
                width=2.2, height=0.38,
                fill_color=fc, fill_opacity=0.75,
                stroke_color=ec, stroke_width=1.5,
            ).shift(RIGHT * 1.5 + UP * (0.6 - i * 0.55))
            lbl = Text(lbl_str, font_size=12, color=ec, line_spacing=0.35)
            lbl.next_to(slab, RIGHT, buff=0.12)
            pieces.add(VGroup(slab, lbl))

        # Non-negativity badge
        nn_badge = VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.8, height=0.5,
                             fill_color="#003300", fill_opacity=0.8,
                             stroke_color="#44cc44", stroke_width=1.5),
            Text("≥ 0  (Non-negative)", font_size=15, color="#44cc44"),
        )
        nn_badge[1].move_to(nn_badge[0])
        nn_badge.to_edge(DOWN, buff=0.9)

        self.play(
            cust_block.animate.set_opacity(0.25),
            LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pieces], lag_ratio=0.3),
            FadeOut(missing_cells),
            run_time=T_SLOW,
        )
        self.play(FadeIn(nn_badge), run_time=T_FAST)

        nn_note = Text(
            "Ràng buộc không âm → mỗi nhóm mang ý nghĩa thực tế",
            font_size=15, color=SUBTITLE_COLOR,
        ).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(nn_note), run_time=T_FAST)
        self.wait(0.6)

        # ── Tensor Completion: filled missing cells ────────────────────────
        self.play(FadeOut(VGroup(nn_badge, nn_note, pieces, c_ax)), run_time=T_FAST)
        self.play(cust_block.animate.set_opacity(0.8), run_time=T_FAST)

        filled_cells = VGroup(*[
            Square(side_length=0.27,
                   fill_color=TENSOR_COLOR, fill_opacity=0.85,
                   stroke_color=TENSOR_EDGE_COLOR, stroke_width=0.5
                   ).move_to(cust_block.get_center() +
                              RIGHT * 0.3 * (i - 1) + UP * 0.3 * (j - 1))
            for i, j in [(0, 0), (1, -1), (-1, 1), (2, 0), (-2, -1)]
        ])

        completion_lbl = Text("Tensor Completion – Dự đoán giá trị còn thiếu!",
                              font_size=18, color=HIGHLIGHT_COLOR, weight=BOLD)
        completion_lbl.to_edge(DOWN, buff=0.4)

        self.play(
            LaggedStart(*[GrowFromCenter(c) for c in filled_cells], lag_ratio=0.15),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(completion_lbl), run_time=T_FAST)
        self.wait(1.0)

        self.play(FadeOut(VGroup(cust_block, filled_cells,
                                 completion_lbl, title2)),
                  run_time=T_MEDIUM)

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _person_icon(pos, color):
        head = Circle(radius=0.18, fill_color=color,
                      fill_opacity=0.8, stroke_width=0)
        body = RoundedRectangle(corner_radius=0.08, width=0.28, height=0.38,
                                fill_color=color, fill_opacity=0.6,
                                stroke_width=0)
        body.next_to(head, DOWN, buff=0.04)
        return VGroup(head, body).move_to(pos)

    @staticmethod
    def _wave_group(pos, mix=False):
        rng = np.random.default_rng(7)
        curves = VGroup()
        for k in range(3 if mix else 1):
            pts = [pos + RIGHT * t * 0.18 +
                   UP * (0.3 * np.sin(5 * t + k * 2) +
                         (0.15 * rng.uniform(-1, 1) if mix else 0))
                   for t in np.linspace(0, 8, 40)]
            wave = VMobject(color=WHITE if mix else VECTOR_COLOR,
                            stroke_width=1.5, stroke_opacity=0.7)
            wave.set_points_as_corners(pts)
            curves.add(wave)
        return curves
