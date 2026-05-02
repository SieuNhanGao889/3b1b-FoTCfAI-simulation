"""
scenes/scene_2c_lora.py
────────────────────────────────────────────────────────────────────────────
SCENE 2C: LoRA — Fine-tuning the Giants   (3:20 – 4:00,  ≈ 40 giây)

STORY ARC (Show Don't Tell):
  Beat 1  [0–10s]  PROBLEM  — Ma trận W khổng lồ đổ xuống. GPU icon "khuỵu".
                             16M params hiện ra → viewer cảm nhận sức nặng.

  Beat 2  [10–25s] INSIGHT  — W "nứt vỡ". Hai tấm mỏng A (r×n) và B (n×r)
                             trượt ra, đối xứng trái-phải. Ký hiệu ΔW = B·A
                             và bottleneck corridor hình hoá rank-r.

  Beat 3  [25–40s] PAYOFF   — Hai panel dot-grid: 900 chấm đỏ (16M) vs
                             25 chấm xanh (65K). Stamp "256×" đập xuống.
"""

from manim import *

# ── Palette ───────────────────────────────────────────────────────────────
BG_COLOR        = "#0d0d0d"
HIGHLIGHT_COLOR = YELLOW
SUBTITLE_COLOR  = GREY_B
PRODUCT_COLOR   = "#FF6B35"

# ── Layout zones ──────────────────────────────────────────────────────────
Y_TITLE =  3.30   # Title cố định — không có gì được đặt đây ngoài title
Y_SUB   =  2.60   # Sub-title / phase label
Y_BODY  =  0.10   # Trung tâm visual chính
Y_NOTE  = -3.10   # Ghi chú / công thức phụ (bottom)

X_LEFT  = -3.20   # Panel trái (Beat 3)
X_RIGHT =  3.20   # Panel phải (Beat 3)

def at(x, y): return np.array([x, y, 0])

def tx(s, sz=28, col=WHITE):
    return MathTex(s, font_size=sz, color=col)

def words(s, sz=26, col=WHITE):
    return Text(s, font_size=sz, color=col)


# ── Visual helpers ────────────────────────────────────────────────────────
def matrix_rect(w, h, fc, ec, alpha=0.88, sw=1.8):
    return Rectangle(
        width=w, height=h,
        fill_color=fc, fill_opacity=alpha,
        stroke_color=ec, stroke_width=sw,
    )


def grid_lines_inside(rect, nx, ny, col=GREY_D, alpha=0.35):
    """Lưới mờ bên trong rect — biểu thị 'rất nhiều tham số'."""
    w, h = rect.width, rect.height
    cx, cy = rect.get_center()[:2]
    lines = VGroup()
    for i in range(1, nx):
        x = cx - w / 2 + i * w / nx
        lines.add(Line([x, cy - h/2, 0], [x, cy + h/2, 0],
                       stroke_color=col, stroke_width=0.5, stroke_opacity=alpha))
    for j in range(1, ny):
        y = cy - h / 2 + j * h / ny
        lines.add(Line([cx - w/2, y, 0], [cx + w/2, y, 0],
                       stroke_color=col, stroke_width=0.5, stroke_opacity=alpha))
    return lines


def dot_field(rows, cols, dot_r, col, alpha, h_gap, v_gap):
    """Lưới Dot — phong cách scene_1a."""
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=dot_r, color=col, fill_opacity=alpha)
            d.move_to(RIGHT * c * h_gap + DOWN * r * v_gap)
            g.add(d)
    return g


# ══════════════════════════════════════════════════════════════════════════
class LoRAScene(Scene):
# ══════════════════════════════════════════════════════════════════════════
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title cố định suốt scene ──────────────────────────────────────
        title = words("LoRA: Fine-tuning the Giants", 32, HIGHLIGHT_COLOR)
        title.move_to(at(0, Y_TITLE))
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.6)

        # ════════════════════════════════════════════════════════════════
        # BEAT 1: SỨC NẶNG CỦA W
        # Visual: W đổ từ trên xuống → GPU icon khuỵu
        # ════════════════════════════════════════════════════════════════
        sub_1 = words("Full Weight Matrix", 24, SUBTITLE_COLOR)
        sub_1.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_1), run_time=0.45)

        # W: to, lạnh, nặng nề — căn giữa màn hình
        W_r = matrix_rect(5.2, 4.4, "#1a2a4a", GREY_C, alpha=0.94, sw=2.0)
        W_r.move_to(at(0, Y_BODY))
        gl = grid_lines_inside(W_r, 10, 8)

        W_lbl = tx(r"\mathbf{W}", 64, GREY_C).move_to(W_r.get_center() + UP * 0.35)
        W_dim = tx(r"4096 \times 4096", 22, GREY_B).move_to(W_r.get_center() + DOWN * 0.55)
        W_group = VGroup(W_r, gl, W_lbl, W_dim)
        W_group.shift(UP * 9)   # off-screen top

        # W rơi xuống
        self.play(
            W_group.animate.shift(DOWN * 9),
            rate_func=rate_functions.ease_in_out_cubic,
            run_time=1.1,
        )

        # GPU icon — bên trái dưới, trong màn hình
        gpu_body = RoundedRectangle(
            corner_radius=0.10, width=1.30, height=0.60,
            fill_color="#003300", fill_opacity=0.95,
            stroke_color=GREEN_C, stroke_width=1.5,
        )
        gpu_text = words("GPU", 16, GREEN_C).move_to(gpu_body)
        gpu_group = VGroup(gpu_body, gpu_text).move_to(at(-4.0, -2.60))

        self.play(FadeIn(gpu_group), run_time=0.35)
        self.play(
            gpu_group.animate.shift(DOWN * 0.22).scale(0.80),
            W_group.animate.shift(DOWN * 0.08),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=0.80,
        )

        # Số params — ở Y_NOTE (KHÔNG đè title)
        count_lbl = tx(r"16{,}777{,}216\ \text{parameters}", 28, RED_C)
        count_lbl.move_to(at(0, Y_NOTE + 0.55))
        self.play(Write(count_lbl), run_time=0.65)
        self.wait(1.6)

        # ════════════════════════════════════════════════════════════════
        # BEAT 2: VỠ — Bottleneck rank-r
        # Visual: W nứt → A (ngang, vàng, r×4096) và B (dọc, xanh, 4096×r)
        #         trượt ra đối xứng. Ký hiệu × ở giữa. Bottleneck hình hoá.
        #
        # Quy ước LoRA:   ΔW = B · A
        #   A ∈ R^{r×n}   (hàng mỏng — DOWN, vàng)   → chiếu xuống rank-r
        #   B ∈ R^{n×r}   (cột mỏng — trái, xanh)     → kéo lên lại
        # ════════════════════════════════════════════════════════════════

        # -- Công thức sub (thay sub_1) --
        sub_2 = tx(r"\Delta W \approx B \cdot A \quad (r \ll n)", 28, HIGHLIGHT_COLOR)
        sub_2.move_to(at(0, Y_SUB))

        # Crack line dọc qua giữa W
        crack = Line(
            W_r.get_center() + UP * 2.4,
            W_r.get_center() + DOWN * 2.4,
            stroke_color=YELLOW, stroke_width=3.0,
        )
        self.play(FadeOut(count_lbl), Create(crack), run_time=0.50)
        self.play(
            crack.animate.set_stroke(WHITE, width=7),
            run_time=0.18, rate_func=there_and_back,
        )

        # -- Định vị cuối cùng của A và B --
        # B: dọc (4096×r) — bên TRÁI, căn giữa theo Y_BODY
        A_FINAL_X = -2.80
        A_FINAL_Y =  Y_BODY + 0.15

        # A: ngang (r×4096) — bên PHẢI, cùng trục Y
        B_FINAL_X =  2.80
        B_FINAL_Y =  Y_BODY + 0.15

        # Trung tâm: ký hiệu ×
        MID_X     =  0.00
        MID_Y     =  Y_BODY + 0.15

        # B (dọc, xanh — 4096×r)
        B_r   = matrix_rect(0.32, 3.80, BLUE_C, BLUE_B, alpha=0.92)
        B_dim = tx(r"4096 \times r", 17, BLUE_B)
        B_tag = tx(r"B", 34, BLUE_C)

        B_group = VGroup(B_r)
        B_group.move_to(W_r.get_center())   # bắt đầu từ giữa W

        B_dim.next_to(B_r, DOWN, buff=0.13)
        B_tag.next_to(B_r, UP,   buff=0.12)
        B_full = VGroup(B_group, B_dim, B_tag)

        # A (ngang, vàng — r×4096)
        A_r   = matrix_rect(3.80, 0.32, GOLD, GOLD_A, alpha=0.92)
        A_dim = tx(r"r \times 4096", 17, GOLD_A)
        A_tag = tx(r"A", 34, GOLD)

        A_group = VGroup(A_r)
        A_group.move_to(W_r.get_center())   # bắt đầu từ giữa W

        A_dim.next_to(A_r, DOWN, buff=0.13)
        A_tag.next_to(A_r, UP,   buff=0.12)
        A_full = VGroup(A_group, A_dim, A_tag)

        # W mờ đi, A và B tách ra
        self.play(
            W_group.animate.set_opacity(0.10),
            FadeOut(crack),
            ReplacementTransform(sub_1, sub_2),
            run_time=0.55,
        )
        self.play(
            B_full.animate.move_to(at(A_FINAL_X, A_FINAL_Y)),
            A_full.animate.move_to(at(B_FINAL_X, B_FINAL_Y)),
            rate_func=rate_functions.ease_out_cubic,
            run_time=1.25,
        )

        # Ký hiệu × ở chính giữa A và B (cùng trục Y)
        times_sym = tx(r"\times", 40, PRODUCT_COLOR)
        times_sym.move_to(at(MID_X, MID_Y))
        self.play(GrowFromCenter(times_sym), run_time=0.40)

        # Bottleneck arrows — từ mép phải B đến × rồi × đến mép trái A
        left_edge  = at(A_FINAL_X + 0.16,  MID_Y)   # mép phải B_r
        right_edge = at(B_FINAL_X - 1.90,  MID_Y)   # mép trái A_r (ngang dài 3.8/2)
        neck       = at(MID_X,             MID_Y)

        bottleneck = VGroup(
            Arrow(left_edge,  neck,       buff=0.08,
                  color=HIGHLIGHT_COLOR, stroke_width=2.0,
                  max_tip_length_to_length_ratio=0.12),
            Arrow(neck,       right_edge, buff=0.08,
                  color=HIGHLIGHT_COLOR, stroke_width=2.0,
                  max_tip_length_to_length_ratio=0.12),
        )
        self.play(LaggedStart(*[GrowArrow(a) for a in bottleneck], lag_ratio=0.2),
                  run_time=0.65)

        # r badge — Y_NOTE + 0.80 (trên)
        r_badge = VGroup(
            tx(r"r = 8", 36, HIGHLIGHT_COLOR),
            tx(r"\ll 4096", 22, SUBTITLE_COLOR),
        ).arrange(RIGHT, buff=0.16)
        r_badge.move_to(at(MID_X, Y_NOTE + 0.80))
        self.play(FadeIn(r_badge, scale=1.15), run_time=0.50)

        # note frozen — Y_NOTE + 0.10 (dưới r_badge, không chồng)
        note_frozen = tx(
            r"W_0\ \text{frozen} \quad \text{only train}\ A,\ B",
            22, SUBTITLE_COLOR,
        )
        note_frozen.move_to(at(0, Y_NOTE + 0.10))
        self.play(FadeIn(note_frozen), run_time=0.50)
        self.wait(2.0)

        # ════════════════════════════════════════════════════════════════
        # BEAT 3: PAYOFF — So sánh dot-grid + Stamp 256×
        # Xóa Beat 2 trước, rồi build 2 panel
        # ════════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(
                W_group, gpu_group, sub_2,
                B_full, A_full, times_sym,
                bottleneck, r_badge, note_frozen,
            )),
            run_time=0.55,
        )

        # Sub mới
        sub_3 = tx(r"\text{Comparing Parameter Counts}", 26, SUBTITLE_COLOR)
        sub_3.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_3), run_time=0.35)

        # -- Panel trái: W (16M) --
        panel_L = matrix_rect(4.10, 4.10, "#1a0000", RED_C, alpha=0.50, sw=1.5)
        panel_L.move_to(at(X_LEFT, Y_BODY))

        dots_W = dot_field(30, 30, 0.025, RED_C, 0.82, 0.118, 0.118)
        dots_W.move_to(panel_L.get_center())

        lbl_W_top = tx(r"W:\ 4096 \times 4096", 20, RED_C)
        lbl_W_top.next_to(panel_L, UP, buff=0.18)

        lbl_W_bot = tx(r"16{,}777{,}216\ \text{parameters}", 18, RED_C)
        lbl_W_bot.next_to(panel_L, DOWN, buff=0.16)

        # -- Panel phải: LoRA (65K) --
        panel_R = matrix_rect(4.10, 4.10, "#001a00", GREEN_C, alpha=0.50, sw=1.5)
        panel_R.move_to(at(X_RIGHT, Y_BODY))

        # 65536 / 16777216 ≈ 1/256 → dùng 5×5=25 chấm vs 30×30=900
        dots_LR = dot_field(5, 5, 0.075, GREEN_C, 0.95, 0.26, 0.26)
        dots_LR.move_to(panel_R.get_center())

        lbl_R_top = tx(r"A + B\ \text{(LoRA)}", 20, GREEN_C)
        lbl_R_top.next_to(panel_R, UP, buff=0.18)

        lbl_R_bot = tx(r"65{,}536\ \text{parameters}", 18, GREEN_C)
        lbl_R_bot.next_to(panel_R, DOWN, buff=0.16)

        # -- Hiện 2 panel cùng lúc --
        self.play(
            FadeIn(panel_L), FadeIn(lbl_W_top),
            FadeIn(panel_R), FadeIn(lbl_R_top),
            run_time=0.50,
        )

        # Đổ chấm đỏ vào panel trái (density = sức nặng)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_W], lag_ratio=0.004),
            run_time=1.55,
        )
        self.play(FadeIn(lbl_W_bot), run_time=0.30)

        # Vài chấm xanh vào panel phải — khoảng trống chính là lập luận
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.8) for d in dots_LR], lag_ratio=0.07),
            run_time=0.60,
        )
        self.play(FadeIn(lbl_R_bot), run_time=0.30)
        self.wait(0.8)

        # -- Stamp 256× -- xuất hiện TRÊN 2 panel, đủ cao để không che label
        stamp_ring = Circle(
            radius=1.35,
            stroke_color=HIGHLIGHT_COLOR, stroke_width=4,
            fill_color=BG_COLOR, fill_opacity=0.96,
        )
        stamp_num  = tx(r"256\times", 50, HIGHLIGHT_COLOR)
        stamp_note = tx(r"\text{fewer parameters!}", 19, HIGHLIGHT_COLOR)
        stamp_note.next_to(stamp_num, DOWN, buff=0.14)

        stamp = VGroup(stamp_ring, stamp_num, stamp_note)
        stamp.move_to(at(0, Y_BODY + 0.40))   # giữa màn hình, cao hơn trục
        stamp.scale(2.6)                        # phình to rồi bounce về

        self.play(
            stamp.animate.scale(1 / 2.6),
            rate_func=rate_functions.ease_out_bounce,
            run_time=0.65,
        )

        # Dòng kết — Y_NOTE (dưới cùng, đủ xa stamp và lbl_bot)
        final = tx(r"\text{Fine-tune only with a regular laptop!}", 24, GREEN_C)
        final.move_to(at(0, Y_NOTE + 0.40))
        self.play(Write(final), run_time=0.80)
        self.wait(2.5)

        # ── Outro ─────────────────────────────────────────────────────────
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.80)