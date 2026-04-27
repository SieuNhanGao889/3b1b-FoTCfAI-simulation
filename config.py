"""
config.py – Global palette and timing constants.
Import this in every scene file.
"""

from manim import *

# ── Background ──────────────────────────────────────────────────────────────
BG_COLOR = "#0d0d0d"

# ── Data-structure colors ────────────────────────────────────────────────────
TENSOR_COLOR      = "#1e90ff"   # primary block face
TENSOR_EDGE_COLOR = "#00cfff"   # glowing edges
VECTOR_COLOR      = "#ffaa33"   # warm amber – vectors / fibers
MATRIX_COLOR      = "#66cc88"   # soft green – matrices / slices
SCALAR_COLOR      = "#ffffff"   # white dot for scalar

# ── Circuit node colors ──────────────────────────────────────────────────────
SUM_NODE_COLOR     = "#55aaff"
PRODUCT_NODE_COLOR = "#ff6633"

# ── Text / formula ───────────────────────────────────────────────────────────
MATH_COLOR     = WHITE
SUBTITLE_COLOR = "#cccccc"
HIGHLIGHT_COLOR = "#ffe066"

# ── Timing presets (seconds) ─────────────────────────────────────────────────
T_SLOW   = 2.5   # concept reveal
T_MEDIUM = 1.2   # transitions
T_FAST   = 0.45  # emphasis pulses

# ── Helper: standard 3B1B-style glow stroke ──────────────────────────────────
def glow_stroke(mob: VMobject, color=HIGHLIGHT_COLOR, width: float = 6) -> VMobject:
    """Add a thick, semi-transparent stroke on top of a mobject to simulate glow."""
    glow = mob.copy().set_stroke(color, width=width, opacity=0.35)
    return VGroup(mob, glow)
