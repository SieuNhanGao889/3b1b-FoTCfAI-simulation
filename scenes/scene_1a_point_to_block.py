"""
scenes/scene_1a_point_to_block_extended.py
─────────────────────────────────────────────────────────────────────────────
SCENE 1A: The Full Journey (Context -> The Wall -> Solution -> Point-to-Block)
Duration: ~1:30 - 2:00

LAYOUT ZONES:
  ZONE TOP    (y =  3.40) -> Main Title
  ZONE SUB    (y =  2.72) -> Subtitle / Current Step
  ZONE LEFT   (x = -3.70) -> Main Visuals (3D blocks, grids, dots)
  ZONE RIGHT  (x =  3.10) -> Concepts, Lists, Taxonomy panel
  ZONE BOTTOM (y = -3.30) -> Formulas, Indices, Notes
"""

from manim import *

class PointToBlock(Scene):
    def construct(self):
        # ==========================================================
        # 0. CONFIGURATION & ZONES
        # ==========================================================
        Z_TOP = UP * 3.40
        Z_SUB = UP * 2.72
        Z_LEFT = LEFT * 3.70
        Z_RIGHT = RIGHT * 3.10
        Z_BOTTOM = DOWN * 3.30

        # Monochromatic Blue Palette & Accents
        UCOLS = [BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A]
        C_WARN = [RED_E, RED_D, RED_C, RED_B, RED_A]
        C_HL = YELLOW
        C_SUCCESS = GREEN

        # Main fixed title
        title = MathTex(r"\text{The Foundation: Tensors in AI}", font_size=42).move_to(Z_TOP)
        self.play(FadeIn(title, shift=DOWN * 0.2))

        # ==========================================================
        # PHASE 1: THE CONTEXT & SCALE (Storytelling)
        # ==========================================================
        sub_context = MathTex(r"\text{Context: What powers the most advanced AI?}", font_size=32).move_to(Z_SUB)
        self.play(FadeIn(sub_context))

        # Single parameter
        single_param = Dot(color=UCOLS[0], radius=0.1).move_to(Z_LEFT)
        note_param = MathTex(r"\text{A single parameter = A basic unit of knowledge}", font_size=28).move_to(Z_BOTTOM)
        
        self.play(FadeIn(single_param), FadeIn(note_param))
        self.wait(1)

       # 1. Configuration for size 8
        side_dim = 8
        spacing = 0.14 # Slightly tighter spacing for a bigger cube
        depth_ratio = 0.5 # Keeps it looking like a cube, not a long prism

        # Create the 8x8 base matrix
        matrix_base = VGroup(*[
            VGroup(*[Dot(radius=0.05) for _ in range(side_dim)]).arrange(RIGHT, buff=spacing)
            for _ in range(side_dim)
        ]).arrange(DOWN, buff=spacing).move_to(Z_LEFT)

        massive_tensor = VGroup()
        for i in range(side_dim):
            layer = matrix_base.copy()
            
            # Calculate the gradient: i=0 is front, i=7 is back
            # interpolate_color goes from Start to End based on a 0-1 alpha
            layer_color = interpolate_color(UCOLS[0], UCOLS[4], i / (side_dim - 1))
            layer.set_color(layer_color)
            
            # Solid layers (no transparency)
            layer.set_opacity(1.0)
            
            # Consistent 3D shift
            layer.shift(RIGHT * (spacing * depth_ratio) * i + UP * (spacing * depth_ratio) * i)
            massive_tensor.add(layer)

        # Reverse so the back layers are drawn first and the front is on top
        massive_tensor.submobjects.reverse()
        massive_tensor.move_to(Z_LEFT)
        
        tax_scale = MathTex(r"\text{SOTA models (GPT-4, Gemini)} \\ \textbf{Trillions} \text{ of parameters.}", font_size=30).move_to(Z_RIGHT)

        self.play(
            FadeOut(single_param),
            LaggedStart(*[FadeIn(layer, shift=UR*0.1) for layer in massive_tensor], lag_ratio=0.05),
            run_time=2
        )
        self.play(Write(tax_scale))
        self.play(FadeOut(note_param))
        self.wait(1)

        # ==========================================================
        # PHASE 2: THE AI SCALING WALL
        # ==========================================================
        sub_wall = MathTex(r"\text{The AI Scaling Wall}", font_size=32, color=C_WARN[2]).move_to(Z_SUB)
        self.play(FadeOut(sub_context), FadeIn(sub_wall))

        # Tensor turns red
        massive_tensor_red = massive_tensor.copy()
        # We iterate through the layers (sub-VGroups) to apply the warning gradient
        for i, layer in enumerate(massive_tensor_red):
            # Use the same interpolation logic as your original blue cube
            new_color = interpolate_color(C_WARN[4], C_WARN[0], i / (side_dim - 1))
            layer.set_color(new_color)
        self.play(ReplacementTransform(massive_tensor, massive_tensor_red), run_time=1)

        # List of 3 problems
        probs = VGroup(
            MathTex(r"\bullet\ \text{Models too large (Memory)}", font_size=28, color=WHITE),
            MathTex(r"\bullet\ \text{Inference too slow (Speed)}", font_size=28, color=WHITE),
            MathTex(r"\bullet\ \text{Black-box models (Interpretability)}", font_size=28, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(Z_RIGHT)

        self.play(FadeOut(tax_scale))
        self.play(LaggedStart(*[FadeIn(p, shift=LEFT*0.1) for p in probs], lag_ratio=0.3))
        self.wait(1.5)

        # ==========================================================
        # PHASE 3: THE SOLUTION (Tensor Decomposition)
        # ==========================================================
        sub_sol = MathTex(r"\text{The Operation: Tensor Decomposition}", font_size=32, color=C_HL).move_to(Z_SUB)
        note_sol = MathTex(r"\text{Extract the core essence, discard redundancy.}", font_size=28).move_to(Z_BOTTOM)
        
        self.play(FadeOut(sub_wall), FadeIn(sub_sol), FadeOut(probs), FadeIn(note_sol))

        # Decompose the red block into clean blue components
        core_cube = Cube(side_length=0.8, fill_opacity=0.8, fill_color=UCOLS[4]).move_to(Z_LEFT)
        f1 = Rectangle(height=0.8, width=2.0, fill_opacity=0.8, fill_color=UCOLS[2]).next_to(core_cube, LEFT, buff=0.2)
        f2 = Rectangle(height=2.0, width=0.8, fill_opacity=0.8, fill_color=UCOLS[2]).next_to(core_cube, UP, buff=0.2)
        decomposition_group = VGroup(f1, f2, core_cube)

        eq_sol = MathTex(r"\mathcal{X} \approx \text{Core} \times \text{Factors}", font_size=36, color=C_HL).move_to(Z_RIGHT)

        self.play(ReplacementTransform(massive_tensor_red, decomposition_group), run_time=2)
        self.play(Write(eq_sol))
        self.wait(1.5)

        # ==========================================================
        # PHASE 4: MULTIWAY STRUCTURE (2D vs 3D)
        # ==========================================================
        sub_why = MathTex(r"\text{Why Tensors? Preserving Multiway Structure}", font_size=32).move_to(Z_SUB)
        self.play(
            FadeOut(sub_sol), FadeIn(sub_why),
            FadeOut(decomposition_group), FadeOut(eq_sol), FadeOut(note_sol)
        )

        # 2D Matrix
        matrix_2d = Rectangle(height=1.8, width=2.5, color=UCOLS[2], fill_opacity=0.2).move_to(Z_RIGHT + UP*0.5)
        label_2d = MathTex(r"\text{User} \times \text{Item}", font_size=26).next_to(matrix_2d, UP)
        warn_2d = MathTex(r"\text{Loses Context/Time!}", font_size=24, color=C_WARN[2]).next_to(matrix_2d, DOWN)
        
        # 3D Tensor
        tensor_3d = VGroup(*[
            Rectangle(height=1.8, width=2.5, color=UCOLS[4], fill_opacity=0.4).shift(UR*0.25*i)
            for i in range(3)
        ]).move_to(Z_LEFT + UP*0.5)
        label_3d = MathTex(r"\text{User} \times \text{Item} \times \text{Time}", font_size=26, color=UCOLS[4]).next_to(tensor_3d, DOWN, buff=0.4)

        self.play(FadeIn(matrix_2d), FadeIn(label_2d), FadeIn(warn_2d))
        self.wait(0.5)
        self.play(FadeIn(tensor_3d), FadeIn(label_3d))
        
        note_why = MathTex(r"\text{Tensors natively exploit multi-dimensional correlations.}", font_size=28, color=C_HL).move_to(Z_BOTTOM)
        self.play(FadeIn(note_why))
        self.wait(2)

        # ==========================================================
        # PHASE 5: THE TAXONOMY (Point to Block - Deep Dive)
        # ==========================================================
        sub_tax = MathTex(r"\text{Formalizing the Structure: Point to Block}", font_size=32).move_to(Z_SUB)
        self.play(
            FadeOut(sub_why), FadeIn(sub_tax),
            FadeOut(matrix_2d), FadeOut(label_2d), FadeOut(warn_2d),
            FadeOut(tensor_3d), FadeOut(label_3d), FadeOut(note_why)
        )

        # Prepare right panel placeholders
        tax_panel = VGroup(
            MathTex(r"\bullet\ \text{rank-0}: x \in \mathbb{R} \quad \text{(Scalar)}", font_size=28, color=UCOLS[0]),
            MathTex(r"\bullet\ \text{rank-1}: \mathbf{v} \in \mathbb{R}^{n} \quad \text{(Vector)}", font_size=28, color=UCOLS[1]),
            MathTex(r"\bullet\ \text{rank-2}: \mathbf{M} \in \mathbb{R}^{m \times n} \quad \text{(Matrix)}", font_size=28, color=UCOLS[2]),
            MathTex(r"\bullet\ \text{rank-}d: \mathcal{X} \in \mathbb{R}^{n_1 \times \cdots \times n_d} \quad \text{(Tensor)}", font_size=28, color=UCOLS[4])
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(Z_RIGHT)

        # --- STEP 5.1: SCALAR ---
        v_scalar = Dot(color=UCOLS[0], radius=0.15).move_to(Z_LEFT)
        note_scalar = MathTex(r"\text{A single value. No indices needed.}", font_size=28).move_to(Z_BOTTOM)
        
        self.play(FadeIn(v_scalar), Write(tax_panel[0]), FadeIn(note_scalar))
        self.wait(1.5)

        # --- STEP 5.2: VECTOR ---
        v_vector = VGroup(*[Dot(color=UCOLS[1], radius=0.12) for _ in range(5)]).arrange(DOWN, buff=0.3).move_to(Z_LEFT)
        note_vector = MathTex(r"\text{1D Array. Accessed by 1 index: } v_i", font_size=28).move_to(Z_BOTTOM)
        
        self.play(
            ReplacementTransform(v_scalar, v_vector[0]),
            LaggedStart(*[FadeIn(d, shift=DOWN*0.1) for d in v_vector[1:]], lag_ratio=0.2),
            FadeOut(note_scalar)
        )
        self.play(Write(tax_panel[1]), FadeIn(note_vector))
        self.wait(1.5)

        # --- STEP 5.3: MATRIX ---
        v_matrix = VGroup(*[
            VGroup(*[Dot(color=UCOLS[2], radius=0.1) for _ in range(5)]).arrange(DOWN, buff=0.3)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.3).move_to(Z_LEFT)
        note_matrix = MathTex(r"\text{2D Array. Accessed by 2 indices: } M_{i,j}", font_size=28).move_to(Z_BOTTOM)

        self.play(
            ReplacementTransform(v_vector, v_matrix[0]),
            LaggedStart(*[FadeIn(col, shift=RIGHT*0.1) for col in v_matrix[1:]], lag_ratio=0.2),
            FadeOut(note_vector)
        )
        self.play(Write(tax_panel[2]), FadeIn(note_matrix))
        self.wait(1.5)

        # --- STEP 5.4: TENSOR (3D+) ---
        v_tensor = VGroup()
        for i in range(4):
            layer = v_matrix.copy().set_color(UCOLS[min(i+2, 4)]).set_opacity(1 - i*0.2)
            layer.shift(UR * 0.2 * i)
            v_tensor.add(layer)
        v_tensor.move_to(Z_LEFT)
        
        note_tensor = MathTex(r"\text{Multiway Array. Accessed by } d \text{ indices: } \mathcal{X}_{i,j,k}", font_size=28, color=C_HL).move_to(Z_BOTTOM)

        self.play(
            ReplacementTransform(v_matrix, v_tensor[0]),
            LaggedStart(*[FadeIn(layer, shift=UR*0.1) for layer in v_tensor[1:]], lag_ratio=0.3),
            FadeOut(note_matrix)
        )
        self.play(Write(tax_panel[3]), FadeIn(note_tensor))
        self.wait(1)

        # --- STEP 5.5: DRAWING AXES (Modes) ---
        axes = VGroup(
            Arrow(start=v_tensor.get_corner(DL) + DL*0.2, end=v_tensor.get_corner(DL) + RIGHT*2.5, buff=0, color=WHITE), # Mode 2
            Arrow(start=v_tensor.get_corner(DL) + DL*0.2, end=v_tensor.get_corner(DL) + UP*2.5, buff=0, color=WHITE),    # Mode 1
            Arrow(start=v_tensor.get_corner(DL) + DL*0.2, end=v_tensor.get_corner(DL) + UR*2.0, buff=0, color=WHITE)     # Mode 3
        )
        mode_labels = VGroup(
            MathTex(r"\text{Mode 2 } (j)", font_size=20).next_to(axes[0], RIGHT),
            MathTex(r"\text{Mode 1 } (i)", font_size=20).next_to(axes[1], UP),
            MathTex(r"\text{Mode 3 } (k)", font_size=20).next_to(axes[2], UR)
        )

        self.play(Create(axes), FadeIn(mode_labels))
        self.wait(2)

        # ==========================================================
        # OUTRO / CLEANUP
        # ==========================================================
        self.play(FadeOut(Group(*self.mobjects)))