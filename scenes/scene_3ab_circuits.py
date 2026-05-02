"""
scenes/scene_3ab_circuits_v2.py
────────────────────────────────────────────────────────────────────────────
SCENE 3A + 3B: Tensor Circuits & Sum-Product Networks  (5:00 – 6:30, ≈ 90s)

STORY ARC:
  3A [0–45s]  Tensor → Circuit
    Beat 1: Khối Dot-grid xuất hiện. Sub: "Tensor không chỉ lưu dữ liệu."
    Beat 2: Block tan rã → DAG (3 input, 2 prod, 1 sum, 1 output).
            Chú thích × / + xuất hiện bên cạnh, có Line trỏ vào đúng node.
    Beat 3: Pulse data chạy từ input → prod (flash đỏ) → sum (flash xanh) → output.

  3B [45–90s]  Shallow vs Deep
    Beat 4: Left = Shallow (1 prod rộng, 6 input). Right = Deep (binary tree, 4 layer).
            Deep circuit nằm trong Y_BODY .. Y_BODY+2.4 — không vượt Y_SUB.
    Beat 5: Label O(n^k) đỏ vs O(k·n) xanh.
            Mũi tên dọc từ O(n^k) xuống O(k·n) với nhãn "tiết kiệm hơn!".
    Beat 6: Stamp "Độ sâu + Tensor = Sức mạnh AI" viết bằng Write — không crash.

FIX LOG (so với bản gốc):
  ✓ stamp LaTeX vỡ (\text{ thiếu mở) → dùng words() thay MathTex phức hợp
  ✓ DAG căn giữa màn hình (block và DAG cùng center at(0, Y_BODY))
  ✓ prod_caption / sum_caption có Line trỏ thẳng vào node, không đặt tùy tiện
  ✓ saving_arrow dọc (top→bottom) thay nằm ngang — không che circuit
  ✓ saving_lbl thay bằng text có nghĩa: "Tiết kiệm tham số mũ!"
  ✓ deep_inp[4] bỏ opacity trick — node thứ 5 được nối edge thật sự vào dp1[1]
  ✓ deep_out hạ xuống Y_BODY + 2.20 — không vượt Y_SUB = 2.60
  ✓ Shallow circuit X căn đối xứng quanh X_LEFT_CENTER
  ✓ sub_3b FadeOut trước stamp
  ✓ clear_3a dùng VGroup tường minh thay list comprehension
"""

from manim import *

# ── Palette ───────────────────────────────────────────────────────────────
BG_COLOR        = "#0d0d0d"
HIGHLIGHT_COLOR = YELLOW
SUBTITLE_COLOR  = GREY_B

SUM_COL   = "#2979FF"   # xanh dương
PROD_COL  = "#FF5252"   # đỏ
INPUT_COL = "#F5A623"   # amber
OUT_COL   = YELLOW

# ── Layout ────────────────────────────────────────────────────────────────
Y_TITLE =  3.40  
Y_SUB   =  2.75  
Y_BODY  = -0.40  
Y_NOTE  = -3.50  

# Tâm của 2 circuit bên 3B (Giữ nguyên)
SH_CX = -3.40   # shallow center-x
DP_CX =  2.80   # deep center-x
def at(x, y): return np.array([x, y, 0])

def tx(s, sz=28, col=WHITE):
    return MathTex(s, font_size=sz, color=col)

def words(s, sz=26, col=WHITE):
    return Text(s, font_size=sz, color=col)


# ── Node factories ────────────────────────────────────────────────────────
def sum_node(pos, r=0.26):
    c = Circle(radius=r, fill_color=SUM_COL,  fill_opacity=0.92, stroke_width=0)
    t = tx(r"+",      24, WHITE).move_to(c)
    return VGroup(c, t).move_to(pos)

def prod_node(pos, r=0.26):
    c = Circle(radius=r, fill_color=PROD_COL, fill_opacity=0.92, stroke_width=0)
    t = tx(r"\times", 20, WHITE).move_to(c)
    return VGroup(c, t).move_to(pos)

def input_node(pos, label, r=0.22):
    c = Circle(radius=r, fill_color=INPUT_COL, fill_opacity=0.82, stroke_width=0)
    t = tx(label, 17, WHITE).move_to(c)
    return VGroup(c, t).move_to(pos)

def make_edge(a_mob, b_mob, col=GREY_C, alpha=0.55, sw=1.4):
    return Line(a_mob.get_center(), b_mob.get_center(),
                color=col, stroke_width=sw, stroke_opacity=alpha)


# ── Tensor helper ─────────────────────────────────────────────────────────
def dot_field(rows, cols, dot_r, col, alpha, h_gap, v_gap):
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            d = Dot(radius=dot_r, color=col, fill_opacity=alpha)
            d.move_to(RIGHT * c * h_gap + DOWN * r * v_gap)
            g.add(d)
    return g

def stacked_tensor(n_layers, rows, cols, dot_r, col_list, alpha,
                   h_gap, v_gap, dx=0.18, dy=0.15):
    layers = VGroup()
    for i in range(n_layers):
        col = col_list[min(i, len(col_list) - 1)]
        g = dot_field(rows, cols, dot_r, col, max(alpha - i * 0.06, 0.3), h_gap, v_gap)
        g.shift(RIGHT * i * dx + UP * i * dy)
        layers.add(g)
    return layers


# ══════════════════════════════════════════════════════════════════════════
class CircuitsAndSPN(Scene):
# ══════════════════════════════════════════════════════════════════════════
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ── Title cố định ─────────────────────────────────────────────────
        title = words("Tensor Factorization as Computational Circuits", 28, HIGHLIGHT_COLOR)
        title.move_to(at(0, Y_TITLE))
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)

        # ════════════════════════════════════════════════════════════════
        # SCENE 3A — BEAT 1: Tensor block
        # ════════════════════════════════════════════════════════════════
        sub_3a = words("Tensor is not just data — it is computation", 24, SUBTITLE_COLOR)
        sub_3a.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_3a), run_time=0.45)

        block = stacked_tensor(
            n_layers=3, rows=5, cols=5,
            dot_r=0.07, col_list=[BLUE_E, BLUE_D, BLUE_C],
            alpha=0.88, h_gap=0.28, v_gap=0.28,
        )
        # Căn giữa màn hình
        block.move_to(at(0, Y_BODY + 0.20))
        block_lbl = tx(r"\mathcal{X}", 36, BLUE_C).next_to(block, UP, buff=0.16)

        self.play(
            LaggedStart(*[FadeIn(l, scale=0.85) for l in block], lag_ratio=0.20),
            FadeIn(block_lbl),
            run_time=0.90,
        )
        self.wait(0.50)

        # ── BEAT 2: Block tan rã → DAG ────────────────────────────────────
        # DAG căn giữa màn hình, trải đều Y_BODY-2.0 .. Y_BODY+2.0
        # 3 input / 2 prod / 1 sum / 1 output
        inp = [
            input_node(at(-1.80, Y_BODY - 2.00), r"x_1"),
            input_node(at( 0.00, Y_BODY - 2.00), r"x_2"),
            input_node(at( 1.80, Y_BODY - 2.00), r"x_3"),
        ]
        prods = [
            prod_node(at(-0.90, Y_BODY - 0.65)),
            prod_node(at( 0.90, Y_BODY - 0.65)),
        ]
        sums = [sum_node(at(0.00, Y_BODY + 0.75))]
        out_dot = Dot(at(0.00, Y_BODY + 1.95), color=OUT_COL, radius=0.18)
        out_lbl = tx(r"y", 28, OUT_COL).next_to(out_dot, UP, buff=0.10)

        edges_dag = VGroup(
            make_edge(inp[0], prods[0]),
            make_edge(inp[1], prods[0]),
            make_edge(inp[1], prods[1]),
            make_edge(inp[2], prods[1]),
            make_edge(prods[0], sums[0]),
            make_edge(prods[1], sums[0]),
            make_edge(sums[0], out_dot),
        )
        dag_nodes = VGroup(*inp, *prods, *sums, out_dot, out_lbl)

        # Tan rã block
        self.play(
            block.animate.set_opacity(0.0).scale(0.08),
            FadeOut(block_lbl),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*[Create(e) for e in edges_dag], lag_ratio=0.10),
            LaggedStart(*[GrowFromCenter(n) for n in dag_nodes], lag_ratio=0.07),
            run_time=1.20,
        )

        # ── Chú thích × và + có Line trỏ vào đúng node ───────────────────
        # Label đặt bên phải màn hình, Line nối về node
        prod_lbl = words("× = COMBINE features", 19, PROD_COL)
        prod_lbl.move_to(at(3.80, Y_BODY - 0.65))   # cùng Y với prod nodes
        prod_arrow = Line(
            prod_lbl.get_left() + LEFT * 0.05,
            prods[1].get_right() + RIGHT * 0.05,
            color=PROD_COL, stroke_width=1.4, stroke_opacity=0.70,
        )

        sum_lbl = words("+ = MIX options", 19, SUM_COL)
        sum_lbl.move_to(at(3.80, Y_BODY + 0.75))    # cùng Y với sum node
        sum_arrow = Line(
            sum_lbl.get_left() + LEFT * 0.05,
            sums[0].get_right() + RIGHT * 0.05,
            color=SUM_COL, stroke_width=1.4, stroke_opacity=0.70,
        )

        self.play(
            FadeIn(prod_lbl), Create(prod_arrow),
            FadeIn(sum_lbl),  Create(sum_arrow),
            run_time=0.75,
        )
        self.wait(0.80)

        # ── BEAT 3: Pulse data flow ───────────────────────────────────────
        # Dot chạy từ input → prod → flash → sum → flash → output → flash
        pulse_a = Dot(inp[0].get_center(), color=INPUT_COL, radius=0.10)
        pulse_b = Dot(inp[2].get_center(), color=INPUT_COL, radius=0.10)
        self.play(FadeIn(pulse_a), FadeIn(pulse_b), run_time=0.18)
        self.play(
            pulse_a.animate.move_to(prods[0].get_center()),
            pulse_b.animate.move_to(prods[1].get_center()),
            run_time=0.75,
        )
        self.play(
            Flash(prods[0], color=PROD_COL, line_length=0.28, num_lines=8),
            Flash(prods[1], color=PROD_COL, line_length=0.28, num_lines=8),
            FadeOut(pulse_a), FadeOut(pulse_b),
            run_time=0.45,
        )

        pulse_c = Dot(prods[0].get_center(), color=PROD_COL, radius=0.10)
        pulse_d = Dot(prods[1].get_center(), color=PROD_COL, radius=0.10)
        self.play(FadeIn(pulse_c), FadeIn(pulse_d), run_time=0.15)
        self.play(
            pulse_c.animate.move_to(sums[0].get_center()),
            pulse_d.animate.move_to(sums[0].get_center()),
            run_time=0.65,
        )
        self.play(
            Flash(sums[0], color=SUM_COL, line_length=0.28, num_lines=8),
            FadeOut(pulse_c), FadeOut(pulse_d),
            run_time=0.40,
        )

        pulse_e = Dot(sums[0].get_center(), color=SUM_COL, radius=0.10)
        self.play(FadeIn(pulse_e), run_time=0.15)
        self.play(pulse_e.animate.move_to(out_dot.get_center()), run_time=0.55)
        self.play(
            Flash(out_dot, color=OUT_COL, line_length=0.42, num_lines=12),
            FadeOut(pulse_e),
            run_time=0.45,
        )

        note_3a = words("Each Tensor split = a computational circuit", 20, SUBTITLE_COLOR)
        note_3a.move_to(at(0, Y_NOTE + 0.55))
        self.play(FadeIn(note_3a), run_time=0.45)
        self.wait(1.50)

        # ── Xóa 3A tường minh, giữ title ─────────────────────────────────
        group_3a = VGroup(
            sub_3a, *[block], block_lbl,
            edges_dag, dag_nodes,
            prod_lbl, prod_arrow, sum_lbl, sum_arrow,
            note_3a,
        )
        self.play(FadeOut(group_3a), run_time=0.55)

        # ════════════════════════════════════════════════════════════════
        # SCENE 3B — BEAT 4: Shallow vs Deep
        # ════════════════════════════════════════════════════════════════
        sub_3b = words("The deeper the circuit = The stronger the AI, with fewer parameters", 24, HIGHLIGHT_COLOR)
        sub_3b.move_to(at(0, Y_SUB))
        self.play(FadeIn(sub_3b), run_time=0.45)

        # ── LEFT: Shallow circuit ─────────────────────────────────────────
        # 6 input căn đều quanh SH_CX, 1 prod rộng, 1 sum, 1 output
        # Span ngang = 5 * 0.65 = 3.25 → từ SH_CX - 1.625 đến SH_CX + 1.625
        n_sh_inp = 6
        sh_inp = VGroup(*[
            input_node(
                at(SH_CX - 1.625 + i * 0.65, Y_BODY - 2.00),
                rf"x_{{{i+1}}}", r=0.18
            )
            for i in range(n_sh_inp)
        ])
        sh_prod = prod_node(at(SH_CX, Y_BODY - 0.55))
        sh_sum  = sum_node( at(SH_CX, Y_BODY + 0.55))
        sh_out  = Dot(at(SH_CX, Y_BODY + 1.55), color=OUT_COL, radius=0.15)

        sh_edges = VGroup(
            *[make_edge(n, sh_prod) for n in sh_inp],
            make_edge(sh_prod, sh_sum),
            make_edge(sh_sum,  sh_out),
        )

        sh_label = words("Shallow", 20, SUBTITLE_COLOR)
        sh_label.move_to(at(SH_CX, Y_NOTE + 0.3))

        # O(n^k) — đỏ, dưới label
        sh_count = tx(r"\mathcal{O}(n^k)\ \text{parameters}", 21, RED_C)
        sh_count.next_to(sh_label, DOWN, buff=0.16)

        self.play(
            LaggedStart(*[Create(e) for e in sh_edges], lag_ratio=0.06),
            LaggedStart(*[GrowFromCenter(n) for n in sh_inp],   lag_ratio=0.07),
            GrowFromCenter(sh_prod),
            GrowFromCenter(sh_sum),
            GrowFromCenter(sh_out),
            run_time=1.10,
        )
        self.play(FadeIn(sh_label), FadeIn(sh_count), run_time=0.40)

        # ── RIGHT: Deep circuit (binary-tree, 4 layer) ────────────────────
        # Y range: Y_BODY-2.00 .. Y_BODY+2.20 — an toàn dưới Y_SUB=2.60
        # 4 input (dùng 4, không có node thừa không nối)
        deep_inp = VGroup(*[
            input_node(
                at(DP_CX - 0.90 + i * 0.60, Y_BODY - 2.00),
                rf"x_{{{i+1}}}", r=0.18
            )
            for i in range(4)
        ])
        # Layer 1: 2 prod
        dp1 = VGroup(
            prod_node(at(DP_CX - 0.55, Y_BODY - 0.85)),
            prod_node(at(DP_CX + 0.55, Y_BODY - 0.85)),
        )
        # Layer 2: 1 sum
        dp2 = sum_node( at(DP_CX, Y_BODY + 0.20))
        # Layer 3: 1 prod
        dp3 = prod_node(at(DP_CX, Y_BODY + 1.10))
        # Layer 4 = output
        deep_out = Dot(at(DP_CX, Y_BODY + 2.10), color=OUT_COL, radius=0.15)
        deep_out_lbl = tx(r"y", 22, OUT_COL).next_to(deep_out, UP, buff=0.08)

        deep_edges = VGroup(
            make_edge(deep_inp[0], dp1[0]),
            make_edge(deep_inp[1], dp1[0]),
            make_edge(deep_inp[2], dp1[1]),
            make_edge(deep_inp[3], dp1[1]),
            make_edge(dp1[0], dp2),
            make_edge(dp1[1], dp2),
            make_edge(dp2,    dp3),
            make_edge(dp3,    deep_out),
        )

        deep_label = words("Deep", 20, HIGHLIGHT_COLOR)
        deep_label.move_to(at(DP_CX, Y_NOTE + 0.3))

        deep_count = tx(r"\mathcal{O}(k \cdot n)\ \text{parameters}", 21, GREEN_C)
        deep_count.next_to(deep_label, DOWN, buff=0.16)

        deep_nodes = VGroup(*deep_inp, *dp1, dp2, dp3, deep_out, deep_out_lbl)

        self.play(
            LaggedStart(*[Create(e) for e in deep_edges], lag_ratio=0.07),
            LaggedStart(*[GrowFromCenter(n) for n in deep_nodes], lag_ratio=0.07),
            run_time=1.20,
        )
        self.play(FadeIn(deep_label), FadeIn(deep_count), run_time=0.40)

        # ── BEAT 5: Mũi tên DỌC nối 2 count label ────────────────────────
        # Mũi tên đứng, đặt chính giữa 2 circuit (x = 0)
        # Từ dòng sh_count xuống dòng deep_count (cùng Y nhưng x khác nhau)
        # → dùng mũi tên từ sh_count xuống deep_count theo đường chéo ngắn,
        #    đặt ở vùng trống giữa 2 panel
        mid_x = (SH_CX + DP_CX) / 2   # ≈ -0.3

        save_arrow = Arrow(
            at(mid_x, sh_count.get_top()[1] + 0.05),
            at(mid_x, deep_count.get_bottom()[1] - 0.05),
            buff=0.0,
            color=HIGHLIGHT_COLOR, stroke_width=2.4,
            max_tip_length_to_length_ratio=0.14,
        )
        save_lbl = words("Save Space!", 20, HIGHLIGHT_COLOR)
        save_lbl.next_to(save_arrow, RIGHT, buff=0.12)

        self.play(GrowArrow(save_arrow), FadeIn(save_lbl), run_time=0.70)
        self.wait(1.00)

        # ── BEAT 6: Stamp kết ─────────────────────────────────────────────
        # FadeOut sub_3b trước để vùng Y_SUB sạch
        self.play(FadeOut(sub_3b), run_time=0.35)

        stamp = words("The depth  +  Tensor  =  AI Power", 28, HIGHLIGHT_COLOR)
        stamp.move_to(at(0, Y_SUB - 0.10))   # dùng vùng Y_SUB vừa được dọn

        self.play(Write(stamp), run_time=0.90)
        self.wait(2.00)

        # ── Outro ──────────────────────────────────────────────────────────
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.80)