"""
scenes/scene_3d_tensorgrad.py
─────────────────────────────────────────────────────────────────────────────
SCENE 3D  "TensorGrad"  (7:45 – 8:30)

- Forward + Backward pass visualization
- Gradient tensor → Tucker factorization (core + factors)
- Memory bar: 100% → 20%
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D


class TensorGrad(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Neural network diagram ────────────────────────────────────────
        title = Text("TensorGrad – Nén gradient", font_size=22,
                     color=HIGHLIGHT_COLOR, weight=BOLD).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=T_FAST)

        # Nodes
        def make_neuron(pos, color=BLUE_D):
            return Circle(radius=0.2, fill_color=color,
                          fill_opacity=0.85, stroke_width=0).move_to(pos)

        layers_pos = [LEFT * 4, LEFT * 2, ORIGIN, RIGHT * 2, RIGHT * 4]
        sizes      = [3, 4, 4, 3, 2]
        neurons = []
        for lx, sz in zip(layers_pos, sizes):
            col = VGroup(*[make_neuron(lx + UP * (j - (sz-1)/2) * 0.65)
                           for j in range(sz)])
            neurons.append(col)

        all_neurons = VGroup(*neurons)

        # Edges between layers
        edges_fwd = VGroup()
        for li in range(len(neurons) - 1):
            for na in neurons[li]:
                for nb in neurons[li + 1]:
                    edges_fwd.add(
                        Line(na.get_center(), nb.get_center(),
                             stroke_color=BLUE_C, stroke_width=0.6,
                             stroke_opacity=0.4)
                    )

        self.play(
            LaggedStart(*[Create(e) for e in edges_fwd], lag_ratio=0.01),
            LaggedStart(*[GrowFromCenter(n) for layer in neurons for n in layer],
                        lag_ratio=0.04),
            run_time=T_SLOW,
        )

        # Forward pass arrow
        fwd_arrow = Arrow(LEFT * 5, RIGHT * 5, color=BLUE_C,
                          stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
        fwd_arrow.to_edge(DOWN, buff=1.0)
        fwd_lbl = Text("Forward pass", font_size=16, color=BLUE_C)
        fwd_lbl.next_to(fwd_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(fwd_arrow), FadeIn(fwd_lbl), run_time=T_MEDIUM)

        # Backward pass arrow
        bwd_arrow = Arrow(RIGHT * 5, LEFT * 5, color="#ff6666",
                          stroke_width=2.5, max_tip_length_to_length_ratio=0.08)
        bwd_arrow.to_edge(DOWN, buff=0.45)
        bwd_lbl = Text("Backward pass (gradients)", font_size=16, color="#ff6666")
        bwd_lbl.next_to(bwd_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(bwd_arrow), FadeIn(bwd_lbl), run_time=T_MEDIUM)
        self.wait(0.5)

        # ── Gradient tensor ───────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(all_neurons, edges_fwd, fwd_arrow, fwd_lbl,
                           bwd_arrow, bwd_lbl)),
            run_time=T_FAST,
        )

        G = Tensor3D(nx=6, ny=5, nz=7, cell_size=0.26,
                     face_color="#553333", edge_color="#ff8888")
        G.shift(LEFT * 2.5)
        G_lbl = Text("∇W", font_size=26,
                        color="#ff8888").next_to(G, UP, buff=0.15)
        G_size = Text("Gradient tensor\n(rất lớn!)", font_size=15,
                      color=SUBTITLE_COLOR, line_spacing=0.4).next_to(G, DOWN, buff=0.1)

        self.play(FadeIn(G, scale=0.7), FadeIn(G_lbl), FadeIn(G_size),
                  run_time=T_MEDIUM)
        self.wait(0.3)

        # ── Tucker factorization ──────────────────────────────────────────
        # Core tensor (small) + 3 factor matrices (thin slabs)
        core = Tensor3D(nx=2, ny=2, nz=2, cell_size=0.32,
                        face_color="#882222", edge_color="#ff5555")
        core.shift(RIGHT * 1.5 + UP * 0.3)

        fac_U = Rectangle(width=0.3, height=1.5,
                          fill_color=VECTOR_COLOR, fill_opacity=0.85,
                          stroke_width=0).shift(RIGHT * 2.9 + UP * 0.3)
        fac_V = Rectangle(width=1.5, height=0.3,
                          fill_color=MATRIX_COLOR, fill_opacity=0.85,
                          stroke_width=0).shift(RIGHT * 1.5 + DOWN * 0.5)
        fac_W = Rectangle(width=0.3, height=1.0,
                          fill_color=TENSOR_EDGE_COLOR, fill_opacity=0.85,
                          stroke_width=0).shift(RIGHT * 3.5 + UP * 0.3)

        core_lbl = Text("Core\n(nhỏ)", font_size=13,
                        color="#ff5555", line_spacing=0.35).next_to(core, UP, buff=0.08)
        fac_lbl = Text("Factor\nmatrices", font_size=13,
                       color=SUBTITLE_COLOR, line_spacing=0.35).next_to(fac_W, RIGHT, buff=0.08)

        approx = Text("≈", font_size=30,
                         color=HIGHLIGHT_COLOR).move_to(RIGHT * 0.3 + UP * 0.3)

        self.play(
            G.animate.set_opacity(0.3),
            FadeIn(approx),
            FadeIn(core, scale=0.6),
            FadeIn(fac_U), FadeIn(fac_V), FadeIn(fac_W),
            FadeIn(core_lbl), FadeIn(fac_lbl),
            run_time=T_SLOW,
        )
        self.wait(0.4)

        # ── Memory bar comparison ─────────────────────────────────────────
        self.play(
            FadeOut(VGroup(G, G_lbl, G_size, core, fac_U, fac_V, fac_W,
                           core_lbl, fac_lbl, approx)),
            run_time=T_FAST,
        )

        bar_bg_old = Rectangle(width=5.0, height=0.55,
                               fill_color="#222222", fill_opacity=1,
                               stroke_width=0).shift(UP * 0.5 + LEFT * 0.2)
        bar_fill_old = Rectangle(width=5.0, height=0.55,
                                 fill_color="#ff4444", fill_opacity=0.9,
                                 stroke_width=0).align_to(bar_bg_old, LEFT)

        bar_bg_new = Rectangle(width=5.0, height=0.55,
                               fill_color="#222222", fill_opacity=1,
                               stroke_width=0).shift(DOWN * 0.25 + LEFT * 0.2)
        bar_fill_new = Rectangle(width=1.0, height=0.55,
                                 fill_color="#44cc44", fill_opacity=0.9,
                                 stroke_width=0).align_to(bar_bg_new, LEFT)

        lbl_old = Text("Full gradient  100%", font_size=16,
                       color="#ff4444").next_to(bar_bg_old, RIGHT, buff=0.15)
        lbl_new = Text("TensorGrad  ~20%", font_size=16,
                       color="#44cc44").next_to(bar_bg_new, RIGHT, buff=0.15)

        self.play(
            FadeIn(bar_bg_old), GrowFromEdge(bar_fill_old, LEFT),
            FadeIn(lbl_old),
            run_time=T_MEDIUM,
        )
        self.play(
            FadeIn(bar_bg_new), GrowFromEdge(bar_fill_new, LEFT),
            FadeIn(lbl_new),
            run_time=T_MEDIUM,
        )

        saving = Text("Tiết kiệm bộ nhớ 5×  –  huấn luyện mô hình lớn bằng GPU thường!",
                      font_size=17, color=HIGHLIGHT_COLOR, weight=BOLD)
        saving.to_edge(DOWN, buff=0.4)
        self.play(Write(saving), run_time=T_MEDIUM)
        self.wait(1.2)

        self.play(FadeOut(VGroup(bar_bg_old, bar_fill_old, bar_bg_new,
                                 bar_fill_new, lbl_old, lbl_new, saving, title)),
                  run_time=T_MEDIUM)
