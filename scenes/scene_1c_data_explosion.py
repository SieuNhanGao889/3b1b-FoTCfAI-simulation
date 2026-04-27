"""
scenes/scene_1c_data_explosion.py
─────────────────────────────────────────────────────────────────────────────
SCENE 1C: Data Explosion & System Overload (1:10 - 1:30)

LAYOUT ZONES (Consistent with Scene 1A):
  ZONE TOP    (y =  3.40) -> Main Title
  ZONE SUB    (y =  2.72) -> Subtitle / Current Step
  ZONE LEFT   (x = -3.70) -> Visuals (Expanding Tensor Cloud)
  ZONE RIGHT  (x =  3.10) -> Concepts / Parameter Counter
  ZONE BOTTOM (y = -3.30) -> Questions / The Magic Solution
"""

from manim import *

class DataExplosion(Scene):
    def construct(self):
        # ==========================================================
        # 0. CONFIGURATION & ZONES
        # ==========================================================
        Z_TOP = UP * 3.40
        Z_SUB = UP * 2.72
        Z_LEFT = LEFT * 3.70
        Z_RIGHT = RIGHT * 3.10
        Z_BOTTOM = DOWN * 3.30

        COLOR_NORMAL = BLUE_C
        COLOR_WARN = RED_A
        COLOR_ANSWER = YELLOW_C

        # Helper to create a faux 3D grid of dots
        def create_tensor_cloud(size, dot_radius=0.06, spacing=0.2, color=COLOR_NORMAL, center_pos=ORIGIN):
            tensor_group = VGroup()
            for z in range(size):
                layer = VGroup()
                for y in range(size):
                    row = VGroup(*[Dot(radius=dot_radius, color=color) for _ in range(size)]).arrange(RIGHT, buff=spacing)
                    layer.add(row)
                layer.arrange(DOWN, buff=spacing)
                # Offset to create faux 3D depth
                layer.shift(UR * spacing * 0.7 * z)
                layer.set_color(interpolate_color(color, BLACK, z / (size + 1)))
                tensor_group.add(layer)
            return tensor_group.move_to(center_pos)

        # Main fixed title
        title = MathTex(r"\text{The Foundation: Tensors in AI}", font_size=42).move_to(Z_TOP)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        # ==========================================================
        # PHASE 1: THE DATA EXPLOSION
        # ==========================================================
        sub_title = MathTex(r"\text{The AI Scaling Wall: Data Explosion}", font_size=32, color=COLOR_WARN).move_to(Z_SUB)
        self.play(FadeIn(sub_title))

        # Start with a modest 3x3x3 tensor on the LEFT
        tensor_small = create_tensor_cloud(size=3, center_pos=Z_LEFT)
        self.play(FadeIn(tensor_small))

        # Setup the exponential counter on the RIGHT
        counter_tracker = ValueTracker(1000)
        
        # Redraw the counter dynamically
        counter_label = always_redraw(
            lambda: MathTex(
                r"\text{Parameters: } " + f"{int(counter_tracker.get_value()):,}", 
                font_size=36, 
                color=WHITE if counter_tracker.get_value() < 500000 else COLOR_WARN
            ).move_to(Z_RIGHT + UP*0.5)
        )
        
        note_counter = MathTex(r"\text{Growing exponentially...}", font_size=28, color=LIGHT_GREY).next_to(counter_label, DOWN, buff=0.5)

        self.play(FadeIn(counter_label), FadeIn(note_counter))
        self.wait(0.5)

        # Growth 1: 3x3x3 -> 6x6x6
        tensor_mid = create_tensor_cloud(size=6, dot_radius=0.05, spacing=0.18, center_pos=Z_LEFT)
        self.play(
            ReplacementTransform(tensor_small, tensor_mid),
            counter_tracker.animate.set_value(100000),
            run_time=1.5,
            rate_func=rate_functions.smooth
        )

        # Growth 2: 6x6x6 -> 10x10x10 (Massive cloud)
        tensor_massive = create_tensor_cloud(size=10, dot_radius=0.04, spacing=0.15, center_pos=Z_LEFT)
        self.play(
            ReplacementTransform(tensor_mid, tensor_massive),
            counter_tracker.animate.set_value(1000000000), # 1 Billion
            run_time=1.5,
            rate_func=rate_functions.ease_in_expo
        )
        self.wait(0.5)

        # ==========================================================
        # PHASE 2: SYSTEM OVERLOAD (FIXED)
        # ==========================================================
        # BÍ QUYẾT FIX LỖI: Tạo một Text TĨNH hoàn toàn thay cho always_redraw
        static_counter = MathTex(r"\text{Parameters: } 1,000,000,000", font_size=36, color=COLOR_WARN).move_to(Z_RIGHT + UP*0.5)

        tensor_overload = tensor_massive.copy().set_color(COLOR_WARN)
        warning_note = MathTex(r"\textbf{SYSTEM OVERLOAD}", font_size=32, color=COLOR_WARN).move_to(note_counter.get_center())
        warning_flash = FullScreenRectangle(color=RED, fill_opacity=0.15)
        
        self.play(
            ReplacementTransform(tensor_massive, tensor_overload),
            ReplacementTransform(note_counter, warning_note),
            ReplacementTransform(counter_label, static_counter), # <--- Tráo đổi sang tĩnh ở đây!
            FadeIn(warning_flash),
            run_time=0.5
        )
        
        # Bây giờ Wiggle trên static_counter sẽ an toàn 100%
        self.play(
            Wiggle(static_counter, scale_value=1.1, run_time=1),
            Wiggle(warning_note, run_time=1),
            Wiggle(tensor_overload, run_time=1), 
            FadeOut(warning_flash, run_time=1)
        )

        # ==========================================================
        # PHASE 3: THE QUESTION & THE MAGIC SOLUTION
        # ==========================================================
        question = MathTex(r"\text{How can we compress this massive data without losing information?}", font_size=32, color=WHITE).move_to(Z_BOTTOM)
        self.play(Write(question))
        self.wait(1)

        # The Magic Reveal
        answer = MathTex(r"\textbf{LOW-RANK FACTORIZATION}", font_size=46, color=COLOR_ANSWER).move_to(Z_BOTTOM)

        glow = answer.copy().set_stroke(COLOR_ANSWER, 10, opacity=0.5)
        answer_group = VGroup(glow, answer)

        self.play(
            tensor_overload.animate.set_opacity(0.15),
            static_counter.animate.set_opacity(0.3),  # Dùng tên biến tĩnh ở đây
            warning_note.animate.set_opacity(0.3),
            ReplacementTransform(question, answer_group),
            run_time=1.5
        )
        self.play(FocusOn(answer_group))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(Group(*self.mobjects)))