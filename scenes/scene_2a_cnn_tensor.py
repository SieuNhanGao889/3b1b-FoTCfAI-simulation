import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *

# ══════════════════════════════════════════════════════════════════════════════
# SCENE 2A: AI's Eyes — The Convolutional Weight Tensor  (1:30 – 2:10)
#
# STORY (show-don't-tell, bám script):
#
#   [1:30–1:40]  Ảnh mèo + con mắt AI  →  "Khi AI nhìn một bức ảnh..."
#
#   [1:40–1:55]  Zoom vào CNN abstract  →  highlight Conv layer
#                "Bên trong mỗi layer là một khối tham số..."
#
#   [1:55–2:10]  Bóc tách Tensor W 4D từng chiều, label xuất hiện tuần tự:
#                  C_out = 64  (64 "ông thợ" — mỗi ông chuyên tìm 1 pattern)
#                  C_in  = 3   (3 mắt màu RGB — không nhìn trắng-đen)
#                  K_H × K_W = 7×7  (mỗi mắt quét vùng 7×7 pixel)
#                Phép tính: 64 × 3 × 7 × 7 = 9,408
#                "Gần 10,000 con số — chỉ cho một layer."
#
# LAYOUT GRID (nhất quán với scene 1a/1b/1c):
#   Y_TITLE =  3.40   — title cố định
#   Y_SUB   =  2.72   — step label
#   Y_BODY  =  0.10   — center diagram
#   Y_NOTE  = -3.30   — note / formula
#   X_LEFT  = -3.70   — visuals
#   X_RIGHT =  3.10   — labels / taxonomy panel
# ══════════════════════════════════════════════════════════════════════════════

Y_TITLE =  3.40
Y_SUB   =  2.72
Y_BODY  =  0.10
Y_NOTE  = -3.30
X_LEFT  = -3.70
X_RIGHT =  3.10

def at(x, y): return np.array([x, y, 0])

def make_title(s):
    return MathTex(s, font_size=32, color=HIGHLIGHT_COLOR).move_to(at(0, Y_TITLE))

def make_sub(s, color=SUBTITLE_COLOR):
    return MathTex(s, font_size=26, color=color).move_to(at(0, Y_SUB))

def make_note(s, color=SUBTITLE_COLOR):
    return MathTex(s, font_size=22, color=color).move_to(at(0, Y_NOTE))


# ── Helper: vẽ lớp CNN (hình chữ nhật mỏng, đại diện 1 feature-map layer) ──
def make_layer(w, h, depth, col, alpha, origin):
    """
    Trả về VGroup: depth tấm chồng lên nhau tạo cảm giác 3D.
    origin = vị trí center của lớp ngoài cùng.
    """
    grp = VGroup()
    for d in range(depth):
        slab = Rectangle(
            width=w, height=h,
            stroke_color=col,
            stroke_opacity=max(0.25, 1.0 - d * 0.18),
            stroke_width=1.5,
            fill_color=col,
            fill_opacity=alpha - d * 0.06,
        ).shift(d * (RIGHT * 0.18 + UP * 0.12))
        grp.add(slab)
    grp.move_to(origin)
    return grp


class CNNTensor(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title cố định ─────────────────────────────────────────────────────
        title = make_title(r"\text{How AI Sees: The Convolutional Weight Tensor}")
        self.play(FadeIn(title), run_time=T_FAST)

        # ══════════════════════════════════════════════════════════════════════
        # [1:30–1:40]  ẢNH MÈO + CON MẮT
        # LEFT : khung ảnh mèo đơn giản (primitives, không emoji)
        # RIGHT: nhãn "Input image  H × W × 3"
        # ══════════════════════════════════════════════════════════════════════
        sub1 = make_sub(r"\text{When AI looks at an image\ldots}")
        self.play(FadeIn(sub1), run_time=T_FAST)

        # Khung ảnh — rectangle với lưới pixel gợi ý
        img_frame = Rectangle(
            width=2.6, height=2.6,
            stroke_color=HIGHLIGHT_COLOR, stroke_width=2.2,
            fill_color=BLUE_E, fill_opacity=0.18,
        ).move_to(at(X_LEFT, Y_BODY))

        # Vẽ lưới 4×4 pixel bên trong
        pixel_grid = VGroup()
        pw = 2.6 / 4
        img_dl = img_frame.get_corner(DL)
        for r in range(4):
            for c in range(4):
                brightness = 0.15 + 0.12 * ((r + c) % 3)
                px = Square(
                    side_length=pw * 0.92,
                    fill_color=interpolate_color(BLUE_E, BLUE_A, brightness),
                    fill_opacity=0.55,
                    stroke_color=BLUE_D, stroke_width=0.6,
                ).move_to(img_dl + RIGHT * (c + 0.5) * pw + UP * (r + 0.5) * pw)
                pixel_grid.add(px)

        # "Tai mèo" — 2 tam giác nhỏ trên đỉnh khung
        ear_l = Triangle(color=BLUE_C, fill_opacity=0.60, fill_color=BLUE_C
                         ).scale(0.22).move_to(img_frame.get_corner(UL) + RIGHT*0.28 + DOWN*0.05)
        ear_r = Triangle(color=BLUE_C, fill_opacity=0.60, fill_color=BLUE_C
                         ).scale(0.22).move_to(img_frame.get_corner(UR) + LEFT*0.28 + DOWN*0.05)
        # Vòng tròn mắt
        eye_l = Circle(radius=0.14, fill_color=WHITE, fill_opacity=0.9,
                       stroke_color=BLUE_D, stroke_width=1
                       ).move_to(img_frame.get_center() + LEFT*0.38 + UP*0.25)
        eye_r = Circle(radius=0.14, fill_color=WHITE, fill_opacity=0.9,
                       stroke_color=BLUE_D, stroke_width=1
                       ).move_to(img_frame.get_center() + RIGHT*0.38 + UP*0.25)
        pupil_l = Dot(eye_l.get_center(), radius=0.07, color=DARK_GRAY)
        pupil_r = Dot(eye_r.get_center(), radius=0.07, color=DARK_GRAY)
        # Mulut
        mouth = Arc(radius=0.28, start_angle=PI + 0.3, angle=PI - 0.6,
                    color=BLUE_C, stroke_width=2
                    ).move_to(img_frame.get_center() + DOWN*0.22)

        cat_icon = VGroup(img_frame, pixel_grid, ear_l, ear_r,
                          eye_l, eye_r, pupil_l, pupil_r, mouth)

        # RIGHT panel: input dimensions
        dim_panel = VGroup(
            MathTex(r"\text{Input image}", font_size=18, color=HIGHLIGHT_COLOR),
            MathTex(r"H \times W \times 3", font_size=22, color=TENSOR_EDGE_COLOR),
            MathTex(r"\text{(height} \times \text{width} \times \text{RGB)}", font_size=15,
                    color=SUBTITLE_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).move_to(at(X_RIGHT, Y_BODY))

        self.play(FadeIn(cat_icon, scale=0.85), run_time=T_MEDIUM)
        self.play(FadeIn(dim_panel), run_time=T_FAST)
        self.wait(0.8)

        # ══════════════════════════════════════════════════════════════════════
        # [1:40–1:55]  CNN PIPELINE — zoom vào Conv layer
        # Hiện 4 layer đơn giản theo chiều ngang, highlight layer giữa
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(sub1, dim_panel)),
            run_time=T_FAST,
        )
        sub2 = make_sub(r"\text{Inside: a stack of Convolutional Layers}")
        self.play(FadeIn(sub2), run_time=T_FAST)

        # Thu nhỏ cat_icon sang góc LEFT, nhường không gian cho pipeline
        self.play(
            cat_icon.animate.scale(0.55).move_to(at(-5.80, Y_BODY)),
            run_time=T_MEDIUM,
        )

        # 4 layer: Input → Conv1 → Conv2 → Output
        layer_specs = [
            (1.8, 2.4, 2, BLUE_E,   0.22, at(-3.50, Y_BODY)),  # Input feat map
            (1.2, 2.8, 3, BLUE_D,   0.28, at(-1.40, Y_BODY)),  # Conv1
            (0.9, 2.6, 3, BLUE_C,   0.28, at( 0.50, Y_BODY)),  # Conv2  ← highlight
            (0.6, 2.0, 2, TEAL_D,   0.22, at( 2.10, Y_BODY)),  # Output feat map
        ]
        layer_lbls = [
            r"\text{Input}",
            r"\text{Conv}_1",
            r"\text{Conv}_2",   # này sẽ bị highlight
            r"\text{Output}",
        ]
        layers  = []
        lbl_mobs = []
        arrows_cnn = []

        for i, (w, h, d, col, alpha, pos) in enumerate(layer_specs):
            lyr = make_layer(w, h, d, col, alpha, pos)
            layers.append(lyr)
            lbl = MathTex(layer_lbls[i], font_size=14, color=SUBTITLE_COLOR)
            lbl.move_to(pos + DOWN * (h / 2 + 0.32))
            lbl_mobs.append(lbl)

        for i in range(len(layers) - 1):
            src = layers[i].get_right() + RIGHT * 0.06
            dst = layers[i + 1].get_left() + LEFT * 0.06
            arr = Arrow(src, dst, color=GRAY, stroke_width=1.8,
                        max_tip_length_to_length_ratio=0.20, buff=0)
            arrows_cnn.append(arr)

        self.play(
            LaggedStart(
                *[AnimationGroup(FadeIn(lyr, scale=0.9), FadeIn(lbl))
                  for lyr, lbl in zip(layers, lbl_mobs)],
                lag_ratio=0.25
            ),
            run_time=T_MEDIUM,
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_cnn], lag_ratio=0.2),
            run_time=T_FAST,
        )
        self.wait(0.4)

        # Highlight Conv2 (index 2) — surge + bounding box
        hl_box = SurroundingRectangle(
            layers[2], color=VECTOR_COLOR, stroke_width=2.5, buff=0.12
        )
        hl_lbl = MathTex(r"\text{Conv Layer}", font_size=15,
                         color=VECTOR_COLOR)
        hl_lbl.next_to(hl_box, UP, buff=0.12)

        self.play(Create(hl_box), FadeIn(hl_lbl), run_time=T_FAST)
        self.play(Indicate(layers[2], scale_factor=1.06, color=VECTOR_COLOR))
        self.wait(0.5)

        # Fade out CNN pipeline
        cnn_group = VGroup(*layers, *lbl_mobs, *arrows_cnn, hl_box, hl_lbl)
        self.play(
            FadeOut(VGroup(sub2, cat_icon, cnn_group)),
            run_time=T_FAST,
        )

        # ══════════════════════════════════════════════════════════════════════
        # [1:55–2:10]  BÓC TÁCH TENSOR W ∈ R^{64×3×7×7}
        #
        # Chiến lược: xây khối tensor 4D từng chiều, mỗi chiều = 1 beat
        #   Beat A: C_out = 64 — lưới 8×8 filter icons (LEFT)
        #   Beat B: C_in  = 3  — zoom vào 1 filter, tách 3 RGB channel (LEFT)
        #   Beat C: K_H × K_W = 7×7 — kernel grid trên channel (LEFT)
        #   Beat D: phép tính + formula (RIGHT + BOTTOM)
        # ══════════════════════════════════════════════════════════════════════
        sub3 = make_sub(
            r"\text{Inside the layer: Weight Tensor }\ "
            r"\mathcal{W} \in \mathbb{R}^{C_{out} \times C_{in} \times K_H \times K_W}"
        )
        self.play(FadeIn(sub3), run_time=T_FAST)

        # RIGHT taxonomy panel — sẽ build dần
        tax_title = MathTex(r"\text{4 dimensions of}\ \mathcal{W}",
                            font_size=18, color=HIGHLIGHT_COLOR)
        tax_title.move_to(at(X_RIGHT, Y_BODY + 1.60))

        self.play(FadeIn(tax_title), run_time=T_FAST)

        # ─── BEAT A: C_out = 64 ───────────────────────────────────────────────
        # LEFT: lưới 8×8 vuông nhỏ — mỗi ô = 1 filter
        FSIZE = 0.24   # kích thước mỗi ô filter
        FGAP  = 0.06
        filters_grp = VGroup()
        for r in range(8):
            for c in range(8):
                shade = interpolate_color(BLUE_E, BLUE_B, (r * 8 + c) / 63.0)
                sq = Square(
                    side_length=FSIZE,
                    fill_color=shade, fill_opacity=0.80,
                    stroke_color=BLUE_C, stroke_width=0.8,
                ).move_to(at(X_LEFT, Y_BODY)
                           + RIGHT * (c - 3.5) * (FSIZE + FGAP)
                           + UP    * (r - 3.5) * (FSIZE + FGAP))
                filters_grp.add(sq)

        cout_lbl = MathTex(
            r"C_{out} = 64\ \text{filters}",
            font_size=18, color=BLUE_B
        ).move_to(at(X_LEFT, Y_BODY + 1.30))

        # Taxonomy line A (RIGHT)
        tax_a = MathTex(
            r"\bullet\ C_{out} = 64\ \text{— 64 pattern detectors}",
            font_size=16, color=BLUE_B
        ).move_to(at(X_RIGHT, Y_BODY + 0.90))

        self.play(
            LaggedStart(*[FadeIn(f, scale=0.5) for f in filters_grp], lag_ratio=0.01),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(cout_lbl), Write(tax_a), run_time=T_FAST)
        self.wait(0.6)

        # ─── BEAT B: C_in = 3 (RGB) ───────────────────────────────────────────
        # Zoom vào 1 filter (filters_grp[0]), tách thành 3 channel stacked
        # Mờ 63 filter còn lại
        self.play(filters_grp[1:].animate.set_opacity(0.12), run_time=T_FAST)

        RGB_COLS  = [RED_D, GREEN_D, BLUE_D]
        rgb_names = [r"\text{R}", r"\text{G}", r"\text{B}"]
        CHAN_W = 1.05
        CHAN_H = 1.05

        channels = VGroup()
        for i, (col, nm) in enumerate(zip(RGB_COLS, rgb_names)):
            ch = Rectangle(
                width=CHAN_W, height=CHAN_H,
                fill_color=col, fill_opacity=0.55,
                stroke_color=col, stroke_width=2,
            ).move_to(at(X_LEFT, Y_BODY)
                      + i * (RIGHT * 0.28 + UP * 0.18)
                      + LEFT * 0.28)
            ch_lbl = MathTex(nm, font_size=16, color=col)
            ch_lbl.move_to(ch.get_corner(UL) + RIGHT * 0.18 + DOWN * 0.18)
            channels.add(ch, ch_lbl)

        cin_lbl = MathTex(
            r"C_{in} = 3\ \text{(RGB channels)}",
            font_size=16, color=RED_C,
        ).move_to(at(X_LEFT, Y_BODY - 0.90))

        tax_b = MathTex(
            r"\bullet\ C_{in} = 3\ \text{— sees in RGB, not grayscale}",
            font_size=16, color=RED_C,
        ).move_to(at(X_RIGHT, Y_BODY + 0.30))

        self.play(
            ReplacementTransform(filters_grp[0].copy(), channels),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(cin_lbl), Write(tax_b), run_time=T_FAST)
        self.wait(0.5)

        # ─── BEAT C: K_H × K_W = 7×7 (per channel + sum) ─────────────────────────

        KCELL = 0.13

        kernel_groups = VGroup()

        for ch_idx in range(3):
            ch_rect = channels[ch_idx * 2]  # lấy RECT, bỏ label
            ch_pos = ch_rect.get_corner(DL)

            kg = VGroup()

            for kr in range(7):
                for kc in range(7):
                    is_center = (2 <= kr <= 4 and 2 <= kc <= 4)

                    kx = ch_pos[0] + (kc + 0.5) * KCELL
                    ky = ch_pos[1] + (7 - kr - 0.5) * KCELL

                    # giảm density cho G, B
                    opacity = 0.75 if ch_idx == 0 else 0.18

                    cell = Square(
                        side_length=KCELL * 0.9,
                        fill_color=GOLD_D if is_center else BLUE_E,
                        fill_opacity=opacity,
                        stroke_color=GOLD_C if is_center else GRAY,
                        stroke_width=0.6,
                    ).move_to(at(kx, ky))

                    kg.add(cell)

            kernel_groups.add(kg)

        # ── Animation: hiện từng channel ──
        self.play(FadeIn(kernel_groups[0], scale=0.8), run_time=0.5)
        self.play(FadeIn(kernel_groups[1], scale=0.8), run_time=0.4)
        self.play(FadeIn(kernel_groups[2], scale=0.8), run_time=0.4)

        # ── SUM node (thay dấu +) ──
        sum_circle = Circle(radius=0.28, color=WHITE, stroke_width=2)
        sum_circle.move_to(kernel_groups.get_right() + RIGHT * 1.2)

        sum_text = MathTex(r"\sum", font_size=22).move_to(sum_circle)

        # arrows từ từng channel → sum
        arrows = VGroup()
        for kg in kernel_groups:
            arr = Arrow(
                kg.get_right(),
                sum_circle.get_left(),
                buff=0.15,
                stroke_width=1.8
            )
            arrows.add(arr)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
            FadeIn(sum_circle),
            FadeIn(sum_text),
            run_time=0.8
        )

        # ── OUTPUT feature ──
        output = Square(
            side_length=0.5,
            fill_color=VECTOR_COLOR,
            fill_opacity=0.85,
            stroke_color=VECTOR_COLOR
        ).next_to(sum_circle, RIGHT, buff=0.5)

        out_lbl = MathTex(
            r"\text{1 feature}",
            font_size=14,
            color=VECTOR_COLOR
        ).next_to(output, DOWN, buff=0.1)

        arrow_out = Arrow(
            sum_circle.get_right(),
            output.get_left(),
            buff=0.1,
            stroke_width=2
        )

        self.play(
            GrowArrow(arrow_out),
            FadeIn(output, scale=0.8),
            FadeIn(out_lbl),
            run_time=0.6
        )

        # ── Labels ──
        kernel_lbl = MathTex(
            r"K_H \times K_W = 7 \times 7\ \text{per channel}",
            font_size=15,
            color=GOLD_C,
        ).move_to(at(X_LEFT, Y_BODY - 1.45))

        tax_c = MathTex(
            r"\bullet\ 7{\times}7\ \text{applied per channel → summed}",
            font_size=16,
            color=GOLD_C,
        ).move_to(at(X_RIGHT, Y_BODY - 0.30))

        self.play(FadeIn(kernel_lbl), Write(tax_c), run_time=T_FAST)
        self.wait(0.5)

        # ─── BEAT D: Phép tính → 9,408 ───────────────────────────────────────
        # Fade mờ LEFT visuals, focus vào RIGHT panel + BOTTOM formula
        left_visuals = VGroup(filters_grp, channels, kernel_groups,
                              cout_lbl, cin_lbl, kernel_lbl)
        self.play(left_visuals.animate.set_opacity(0.18), run_time=T_FAST)

        # Phép tính từng bước — xuất hiện theo thứ tự
        calc = MathTex(
            r"64", r"\times", r"3", r"\times",
            r"(7 \times 7)", r"=", r"9{,}408",
            font_size=38,
        ).move_to(at(X_RIGHT, Y_BODY - 1.10))

        calc[0].set_color(BLUE_B)     # C_out
        calc[2].set_color(RED_C)      # C_in
        calc[4].set_color(GOLD_C)     # K_H × K_W
        calc[5].set_color(WHITE)
        calc[6].set_color(VECTOR_COLOR)

        # Xuất hiện từng phần tử
        for part in calc:
            self.play(FadeIn(part, scale=1.2), run_time=0.18)

        self.play(Indicate(calc[6], scale_factor=1.15, color=VECTOR_COLOR))

        # Bottom note
        note_final = make_note(
            r"\approx 10{,}000\ \text{numbers — for just}\ \textbf{one}\ \text{layer.}"
            r"\ \ \text{A full VGG-16 has 13 conv layers.}",
            color=SUBTITLE_COLOR,
        )
        self.play(Write(note_final), run_time=T_MEDIUM)

        # Taxonomy summary (dòng cuối RIGHT panel)
        tax_d = MathTex(
            r"\Rightarrow\ \mathcal{W} \in \mathbb{R}^{64 \times 3 \times 7 \times 7}",
            font_size=20, color=MATH_COLOR,
        ).move_to(at(X_RIGHT, Y_BODY - 0.85))
        self.play(Write(tax_d), run_time=T_FAST)
        self.wait(T_SLOW)

        # ── Fade out toàn bộ ─────────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(
                title, sub3,
                tax_title, tax_a, tax_b, tax_c, tax_d,
                left_visuals,
                calc, note_final,
            )),
            run_time=T_MEDIUM,
        )
