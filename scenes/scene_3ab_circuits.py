"""
scenes/scene_3ab_circuits.py
─────────────────────────────────────────────────────────────────────────────
SCENE 3A  "Sinh ra một mạch"  (5:00 – 5:45)
SCENE 3B  "Sum-Product Networks"  (5:45 – 6:30)

- Tensor phân rã → nodes (+) và (×) → mạch điện toán học
- SPN: DAG với lá, sum nodes, product nodes
- Shallow vs Deep circuit comparison
─────────────────────────────────────────────────────────────────────────────
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from manim import *
from config import *
from utils.tensor_objects import Tensor3D


def sum_node(pos, radius=0.28):
    c = Circle(radius=radius, fill_color=SUM_NODE_COLOR,
               fill_opacity=0.85, stroke_width=0)
    t = Text("+", font_size=22, color=BLACK, weight=BOLD)
    return VGroup(c, t).move_to(pos)


def prod_node(pos, radius=0.28):
    c = Circle(radius=radius, fill_color=PRODUCT_NODE_COLOR,
               fill_opacity=0.85, stroke_width=0)
    t = Text("×", font_size=20, color=BLACK, weight=BOLD)
    return VGroup(c, t).move_to(pos)


def leaf_node(pos, label="x", color=VECTOR_COLOR):
    c = Circle(radius=0.22, fill_color=color, fill_opacity=0.7, stroke_width=0)
    t = Text(label, font_size=18, color=WHITE)
    return VGroup(c, t).move_to(pos)


def connect(a, b, color=SUBTITLE_COLOR):
    return Line(a.get_center(), b.get_center(),
                color=color, stroke_width=1.5,
                stroke_opacity=0.7)


class CircuitsAndSPN(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ════════════════════════════════════════════════════════════════
        # SCENE 3A
        # ════════════════════════════════════════════════════════════════

        title3a = Text("Tensor phân tách = Mạch tính toán",
                       font_size=22, color=HIGHLIGHT_COLOR, weight=BOLD)
        title3a.to_edge(UP, buff=0.3)

        block = Tensor3D(nx=4, ny=3, nz=5, cell_size=0.26,
                         face_color=TENSOR_COLOR, edge_color=TENSOR_EDGE_COLOR)
        block.shift(LEFT * 4.5)
        self.play(FadeIn(title3a), FadeIn(block, scale=0.8), run_time=T_MEDIUM)

        # Build a small circuit on the right
        # Layout: 3 input layers → 2 product nodes → 1 sum node → output
        inputs = VGroup(
            leaf_node(RIGHT * 0.5 + DOWN * 1.5, r"x_1"),
            leaf_node(RIGHT * 0.5 + DOWN * 0.5, r"x_2"),
            leaf_node(RIGHT * 0.5 + UP * 0.5,   r"x_3"),
            leaf_node(RIGHT * 0.5 + UP * 1.5,   r"x_4"),
        )
        prods = VGroup(
            prod_node(RIGHT * 2.2 + DOWN * 0.6),
            prod_node(RIGHT * 2.2 + UP * 0.6),
        )
        sums = VGroup(
            sum_node(RIGHT * 3.8 + UP * 0.0),
        )
        out = Dot(RIGHT * 5.0, color=HIGHLIGHT_COLOR, radius=0.18)
        out_lbl = Text("y", font_size=24, color=HIGHLIGHT_COLOR)
        out_lbl.next_to(out, RIGHT, buff=0.1)

        edges = VGroup(
            connect(inputs[0], prods[0]),
            connect(inputs[1], prods[0]),
            connect(inputs[2], prods[1]),
            connect(inputs[3], prods[1]),
            connect(prods[0], sums[0]),
            connect(prods[1], sums[0]),
            Line(sums[0].get_center(), out.get_center(),
                 color=SUBTITLE_COLOR, stroke_width=1.5),
        )

        # Dissolve block → circuit
        self.play(block.animate.set_opacity(0.2), run_time=T_FAST)
        self.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.12),
            LaggedStart(*[GrowFromCenter(n) for n in inputs], lag_ratio=0.15),
            LaggedStart(*[GrowFromCenter(n) for n in prods], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(n) for n in sums], lag_ratio=0.2),
            GrowFromCenter(out), FadeIn(out_lbl),
            FadeOut(block),
            run_time=T_SLOW,
        )

        # Node semantics
        and_txt = Text('× = "CÁI NÀY VÀ CÁI KIA"',
                       font_size=16, color=PRODUCT_NODE_COLOR)
        or_txt  = Text('+ = "CÁI NÀY HOẶC CÁI KIA"',
                       font_size=16, color=SUM_NODE_COLOR)
        and_txt.to_edge(DOWN, buff=0.6)
        or_txt.next_to(and_txt, UP, buff=0.15)
        self.play(FadeIn(and_txt), FadeIn(or_txt), run_time=T_FAST)
        self.wait(0.8)

        circuit_3a = VGroup(inputs, prods, sums, edges, out, out_lbl)
        self.play(FadeOut(VGroup(circuit_3a, title3a, and_txt, or_txt)),
                  run_time=T_FAST)

        # ════════════════════════════════════════════════════════════════
        # SCENE 3B – Sum-Product Networks
        # ════════════════════════════════════════════════════════════════

        title3b = Text("Sum-Product Networks (SPN)",
                       font_size=22, color=HIGHLIGHT_COLOR, weight=BOLD)
        title3b.to_edge(UP, buff=0.3)
        self.play(FadeIn(title3b), run_time=T_FAST)

        # Full SPN
        spn_leaves = VGroup(
            leaf_node(LEFT * 3.5 + DOWN * 1.6, r"x_1"),
            leaf_node(LEFT * 2.2 + DOWN * 1.6, r"x_2"),
            leaf_node(LEFT * 0.9 + DOWN * 1.6, r"x_3"),
            leaf_node(RIGHT * 0.4 + DOWN * 1.6, r"x_4"),
            leaf_node(RIGHT * 1.7 + DOWN * 1.6, r"x_5"),
        )
        spn_prod1 = VGroup(
            prod_node(LEFT * 2.85 + DOWN * 0.5),
            prod_node(LEFT * 0.25 + DOWN * 0.5),
            prod_node(RIGHT * 1.05 + DOWN * 0.5),
        )
        spn_sum1 = VGroup(
            sum_node(LEFT * 2.0 + UP * 0.5),
            sum_node(RIGHT * 0.4 + UP * 0.5),
        )
        spn_prod2 = prod_node(LEFT * 0.8 + UP * 1.5)
        spn_root  = sum_node(LEFT * 0.8 + UP * 2.4)

        spn_edges = VGroup(
            # leaves → prod1
            connect(spn_leaves[0], spn_prod1[0]),
            connect(spn_leaves[1], spn_prod1[0]),
            connect(spn_leaves[1], spn_prod1[1]),
            connect(spn_leaves[2], spn_prod1[1]),
            connect(spn_leaves[3], spn_prod1[2]),
            connect(spn_leaves[4], spn_prod1[2]),
            # prod1 → sum1
            connect(spn_prod1[0], spn_sum1[0]),
            connect(spn_prod1[1], spn_sum1[0]),
            connect(spn_prod1[1], spn_sum1[1]),
            connect(spn_prod1[2], spn_sum1[1]),
            # sum1 → prod2
            connect(spn_sum1[0], spn_prod2),
            connect(spn_sum1[1], spn_prod2),
            # prod2 → root
            connect(spn_prod2, spn_root),
        )

        self.play(
            LaggedStart(*[Create(e) for e in spn_edges], lag_ratio=0.06),
            LaggedStart(
                *[GrowFromCenter(n) for n in
                  list(spn_leaves) + list(spn_prod1) + list(spn_sum1) +
                  [spn_prod2, spn_root]],
                lag_ratio=0.08,
            ),
            run_time=T_SLOW,
        )
        self.wait(0.5)

        # Data flow animation: values pulse upward
        flow_dots = [
            Dot(leaf.get_center(), color=HIGHLIGHT_COLOR, radius=0.08)
            for leaf in spn_leaves
        ]
        self.play(LaggedStart(*[GrowFromCenter(d) for d in flow_dots],
                               lag_ratio=0.15), run_time=T_FAST)
        self.play(
            *[d.animate.move_to(spn_prod1[min(i // 2, 2)].get_center())
              for i, d in enumerate(flow_dots)],
            run_time=T_MEDIUM,
        )
        self.play(
            *[d.animate.move_to(spn_root.get_center())
              for d in flow_dots],
            run_time=T_MEDIUM,
        )
        self.play(*[FadeOut(d) for d in flow_dots], run_time=T_FAST)

        # ── Shallow vs Deep comparison ────────────────────────────────────
        spn_all = VGroup(spn_leaves, spn_prod1, spn_sum1, spn_prod2,
                         spn_root, spn_edges)
        self.play(spn_all.animate.shift(LEFT * 2.5).scale(0.7), run_time=T_MEDIUM)

        # Shallow circuit (2 layers, wide)
        sh_pos = RIGHT * 2.0
        sh_leaves = VGroup(*[leaf_node(sh_pos + RIGHT * (i-1) * 0.55 + DOWN * 1.2, f"x_{i+1}")
                              for i in range(5)])
        sh_sum    = sum_node(sh_pos + UP * 0.3)
        sh_edges  = VGroup(*[connect(l, sh_sum) for l in sh_leaves])

        sh_lbl = Text("Shallow\n2 layers, rộng", font_size=14,
                      color=SUBTITLE_COLOR, line_spacing=0.4)
        sh_lbl.next_to(sh_leaves, DOWN, buff=0.15)

        deep_lbl = Text("Deep (SPN)\nCàng sâu = càng mạnh\nmà ít params hơn!",
                        font_size=14, color=HIGHLIGHT_COLOR, line_spacing=0.4)
        deep_lbl.next_to(spn_leaves, DOWN, buff=0.15)

        self.play(
            LaggedStart(*[Create(e) for e in sh_edges], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(n) for n in list(sh_leaves) + [sh_sum]],
                        lag_ratio=0.1),
            run_time=T_MEDIUM,
        )
        self.play(FadeIn(sh_lbl), FadeIn(deep_lbl), run_time=T_FAST)
        self.wait(1.0)

        self.play(FadeOut(VGroup(spn_all, sh_leaves, sh_sum, sh_edges,
                                 sh_lbl, deep_lbl, title3b)),
                  run_time=T_MEDIUM)
