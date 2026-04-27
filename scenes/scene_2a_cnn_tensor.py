"""
scenes/scene_2a_cnn_tensor.py
─────────────────────────────────────────────────────────────────────────────
SCENE 2A  "Mắt AI nhìn thế giới"  (1:30 – 2:10)

- Ảnh mèo → CNN → zoom vào Conv layer → Tensor W 4 chiều
- Label: C_out=64, C_in=3, K_H=7, K_W=7  → 9408 params
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *


class CNNTensor(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Cat image placeholder ─────────────────────────────────────────
        cat = RoundedRectangle(corner_radius=0.2, width=2.2, height=2.2,
                               fill_color="#1a1a2e", fill_opacity=1,
                               stroke_color=VECTOR_COLOR, stroke_width=2)
        cat_text = Text("🐱", font_size=52).move_to(cat)
        cat_grp = VGroup(cat, cat_text).shift(LEFT * 4.5)

        eye_icon = Text("👁", font_size=36).next_to(cat_grp, RIGHT, buff=0.4)

        self.play(FadeIn(cat_grp, scale=0.8), run_time=T_MEDIUM)
        self.play(FadeIn(eye_icon), run_time=T_FAST)

        vo1 = Text("Khi AI nhìn một bức ảnh...", font_size=20,
                   color=SUBTITLE_COLOR).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(vo1), run_time=T_FAST)
        self.wait(0.6)

        # ── Simple CNN diagram ────────────────────────────────────────────
        layers = VGroup()
        colors = [BLUE_D, BLUE_C, TEAL_D, TEAL_C]
        widths = [0.4, 0.5, 0.6, 0.7]
        heights = [1.8, 1.5, 1.2, 1.0]
        for i, (c, w, h) in enumerate(zip(colors, widths, heights)):
            r = Rectangle(width=w, height=h, fill_color=c,
                          fill_opacity=0.7, stroke_color=TENSOR_EDGE_COLOR,
                          stroke_width=1)
            layers.add(r)
        layers.arrange(RIGHT, buff=0.18).shift(RIGHT * 0.5)

        layer_labels = VGroup(
            Text("Conv1", font_size=13, color=TENSOR_EDGE_COLOR),
            Text("Conv2", font_size=13, color=TENSOR_EDGE_COLOR),
            Text("Conv3", font_size=13, color=TENSOR_EDGE_COLOR),
            Text("FC",    font_size=13, color=TENSOR_EDGE_COLOR),
        )
        for lbl, lay in zip(layer_labels, layers):
            lbl.next_to(lay, DOWN, buff=0.1)

        arrow_in = Arrow(eye_icon.get_right(), layers[0].get_left(),
                         color=VECTOR_COLOR, stroke_width=2,
                         max_tip_length_to_length_ratio=0.2)

        self.play(FadeOut(vo1), run_time=T_FAST)
        self.play(
            GrowArrow(arrow_in),
            LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in layers], lag_ratio=0.2),
            LaggedStart(*[FadeIn(l) for l in layer_labels], lag_ratio=0.2),
            run_time=T_SLOW,
        )
        self.wait(0.4)

        # ── Zoom into Conv1 ───────────────────────────────────────────────
        highlight_box = SurroundingRectangle(layers[0], color=HIGHLIGHT_COLOR,
                                             stroke_width=2, buff=0.05)
        self.play(Create(highlight_box), run_time=T_FAST)
        self.play(
            FadeOut(VGroup(cat_grp, eye_icon, arrow_in,
                           layers[1:], layer_labels, highlight_box)),
            layers[0].animate.move_to(LEFT * 3.5).scale(1.8),
            run_time=T_MEDIUM,
        )

        # ── 4D Tensor W visualization ─────────────────────────────────────
        # Represent as stacked colored slabs
        slab_colors = [
            "#1e3a5f", "#1e4a6f", "#1e5a7f", "#1e6a8f",
        ]
        slabs = VGroup()
        for i in range(4):
            s = Rectangle(width=2.2, height=1.4,
                          fill_color=TENSOR_COLOR, fill_opacity=0.55 + i*0.08,
                          stroke_color=TENSOR_EDGE_COLOR, stroke_width=1)
            s.shift(RIGHT * (i * 0.18) + UP * (i * -0.12))
            slabs.add(s)
        slabs.shift(RIGHT * 1.2 + UP * 0.2)

        tensor_title = Text("Tensor W  (4 chiều)", font_size=20,
                            color=TENSOR_EDGE_COLOR, weight=BOLD)
        tensor_title.next_to(slabs, UP, buff=0.2)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.05) for s in slabs], lag_ratio=0.15),
            FadeIn(tensor_title),
            run_time=T_MEDIUM,
        )

        # Dimension annotations
        dims = [
            ("C_out = 64", "số filter đầu ra",  VECTOR_COLOR,  RIGHT * 3.8 + UP * 1.1),
            ("C_in  = 3",  "kênh màu RGB",       MATRIX_COLOR,  RIGHT * 3.8 + UP * 0.45),
            ("K_H = 7",    "chiều cao kernel",   "#ff99aa",     RIGHT * 3.8 + DOWN * 0.2),
            ("K_W = 7",    "chiều rộng kernel",  "#ffcc66",     RIGHT * 3.8 + DOWN * 0.85),
        ]
        dim_mobs = VGroup()
        for label_str, desc, col, pos in dims:
            math = Text(label_str, font="Monospace", font_size=20, color=col)
            dsc  = Text(f"({desc})", font_size=14, color=SUBTITLE_COLOR)
            grp  = VGroup(math, dsc).arrange(RIGHT, buff=0.12)
            grp.move_to(pos)
            dim_mobs.add(grp)

        self.play(
            LaggedStart(*[FadeIn(d, shift=LEFT * 0.1) for d in dim_mobs], lag_ratio=0.3),
            run_time=T_SLOW,
        )
        self.wait(0.5)

        # Multiplication chain
        mult = Text("64 × 3 × 7 × 7 = 9,408",
                       font_size=26, color=HIGHLIGHT_COLOR)
        mult.to_edge(DOWN, buff=0.4)
        self.play(Write(mult), run_time=T_MEDIUM)

        note = Text("…chỉ cho MỘT layer!", font_size=18, color="#ff5555")
        note.next_to(mult, RIGHT, buff=0.2)
        self.play(FadeIn(note, scale=1.1), run_time=T_FAST)
        self.wait(1.2)

        self.play(FadeOut(VGroup(layers[0], layer_labels[0], slabs, tensor_title,
                                 dim_mobs, mult, note)),
                  run_time=T_MEDIUM)
