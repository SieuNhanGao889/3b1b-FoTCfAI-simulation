"""
utils/tensor_objects.py
─────────────────────────────────────────────────────────────────────────────
Reusable 3D-looking Mobjects used across all Part-1 scenes.

Key classes
  Tensor3D       – isometric wireframe block with gradient face
  FiberHighlight – animated colored line running along one axis
  SliceHighlight – animated colored plane cutting the block on one axis
  IndexLabel     – Python/math-style index annotation (e.g. X[:,0,0])
─────────────────────────────────────────────────────────────────────────────
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


# ── Isometric projection helpers ─────────────────────────────────────────────
#
# Trục quy ước (nhìn từ góc trên-phải-trước):
#   x  → sang PHẢI (axis 0 / cols)
#   y  → lên TRÊN  (axis 1 / rows)          ← đây là trục "height" màn hình
#   z  → vào TRONG-TRÁI-XUỐNG (depth)
#
# Cabinet oblique projection:
#   screen_x =  x  - z * cos45° * 0.5   →  sang phải, lùi dần sang trái
#   screen_y =  y  - z * sin45° * 0.4   →  lên cao,   lùi dần xuống thấp
#
# Kết quả: khối nhìn từ góc trên-trái, mặt trước (z=0) ở phía trước,
# mặt trên (y=ny) ở trên, mặt phải (x=nx) ở bên phải — đúng không gian 3B1B.

def iso(x: float, y: float, z: float) -> np.ndarray:
    """Cabinet oblique: x→right, y→up, z→back-left-down."""
    sx = x        - z * 0.5    # depth đẩy sang trái
    sy = y        - z * 0.35   # depth đẩy xuống dưới (không phải lên trên!)
    return np.array([sx, sy, 0])


# ── Tensor3D ─────────────────────────────────────────────────────────────────

class Tensor3D(VGroup):
    """
    A 3-D rectangular cuboid rendered in isometric-style 2-D.

    Parameters
    ----------
    nx, ny, nz   : int   – number of cells along each axis
    cell_size    : float – pixel size of one cell
    face_color   : str   – fill colour for the three visible faces
    edge_color   : str   – stroke colour
    fill_opacity : float
    """

    def __init__(
        self,
        nx: int = 5,
        ny: int = 4,
        nz: int = 6,
        cell_size: float = 0.35,
        face_color: str = TENSOR_COLOR,
        edge_color: str = TENSOR_EDGE_COLOR,
        fill_opacity: float = 0.55,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.cell_size = cell_size
        self.face_color = face_color
        self.edge_color = edge_color

        cs = cell_size

        # Painter's algorithm: vẽ mặt xa trước, gần sau
        # ── Back-left face (x=0, y along Y, z along Z) – mặt trái ────────
        left = self._make_face(
            [(iso(0, j * cs, k * cs), iso(0, (j+1)*cs, k*cs),
              iso(0, (j+1)*cs, (k+1)*cs), iso(0, j*cs, (k+1)*cs))
             for j in range(ny) for k in range(nz)],
            face_color, edge_color, fill_opacity * 0.45,
        )

        # ── Top face (y=ny, x along X, z along Z) ─────────────────────────
        top = self._make_face(
            [(iso(i*cs, ny*cs, k*cs), iso((i+1)*cs, ny*cs, k*cs),
              iso((i+1)*cs, ny*cs, (k+1)*cs), iso(i*cs, ny*cs, (k+1)*cs))
             for i in range(nx) for k in range(nz)],
            face_color, edge_color, fill_opacity * 0.70,
        )

        # ── Front face (z=0, x along X, y along Y) – mặt trước ───────────
        front = self._make_face(
            [(iso(i*cs, j*cs, 0), iso((i+1)*cs, j*cs, 0),
              iso((i+1)*cs, (j+1)*cs, 0), iso(i*cs, (j+1)*cs, 0))
             for i in range(nx) for j in range(ny)],
            face_color, edge_color, fill_opacity,
        )

        # ── Right face (x=nx, y along Y, z along Z) ───────────────────────
        right = self._make_face(
            [(iso(nx*cs, j*cs, k*cs), iso(nx*cs, (j+1)*cs, k*cs),
              iso(nx*cs, (j+1)*cs, (k+1)*cs), iso(nx*cs, j*cs, (k+1)*cs))
             for j in range(ny) for k in range(nz)],
            face_color, edge_color, fill_opacity * 0.55,
        )

        # Thêm theo thứ tự painter: trái → top → phải → trước
        self.add(left, top, right, front)
        self.center()

    @staticmethod
    def _make_face(quads, face_color, edge_color, opacity):
        group = VGroup()
        for pts in quads:
            poly = Polygon(*pts, color=edge_color, fill_color=face_color,
                           fill_opacity=opacity, stroke_width=0.8)
            group.add(poly)
        return group

    # Convenience: world-space position of cell centre (i,j,k)
    def cell_center(self, i: int, j: int, k: int) -> np.ndarray:
        cs = self.cell_size
        raw = iso((i + 0.5) * cs, (j + 0.5) * cs, (k + 0.5) * cs)
        return raw + self.get_center() - iso(
            self.nx * cs / 2, self.ny * cs / 2, self.nz * cs / 2
        )


# ── FiberHighlight ────────────────────────────────────────────────────────────

class FiberHighlight(VGroup):
    """
    Highlights a single fiber in a Tensor3D.

    A fiber is obtained by fixing all but ONE index.
    mode = 0 → varies along nx  (row fiber)
    mode = 1 → varies along ny  (column fiber)
    mode = 2 → varies along nz  (tube/depth fiber)

    The math annotation X[fixed_i, fixed_j, :] etc. is shown next to it.
    """

    def __init__(
        self,
        tensor: Tensor3D,
        mode: int = 2,           # which axis is FREE
        fixed: tuple = (0, 0),   # the two FIXED indices
        color: str = VECTOR_COLOR,
        label: bool = True,
    ):
        super().__init__()
        self.tensor = tensor
        self.mode = mode
        self.color = color

        dots = VGroup()
        lines = VGroup()
        nx, ny, nz = tensor.nx, tensor.ny, tensor.nz

        if mode == 0:           # free along x
            fi, fj = fixed[0], fixed[1]   # fixed y, z
            pts = [tensor.cell_center(i, fi, fj) for i in range(nx)]
            py_idx   = f"X[:, {fi}, {fj}]"
        elif mode == 1:         # free along y
            fi, fk = fixed[0], fixed[1]   # fixed x, z
            pts = [tensor.cell_center(fi, j, fk) for j in range(ny)]
            py_idx   = f"X[{fi}, :, {fk}]"
        else:                   # free along z  (tube)
            fi, fj = fixed[0], fixed[1]   # fixed x, y
            pts = [tensor.cell_center(fi, fj, k) for k in range(nz)]
            py_idx   = f"X[{fi}, {fj}, :]"

        for p in pts:
            dots.add(Dot(p, color=color, radius=0.07))
        for p, q in zip(pts[:-1], pts[1:]):
            lines.add(Line(p, q, color=color, stroke_width=3))

        self.add(lines, dots)

        if label:
            # Dùng Text (không cần LaTeX) để tránh lỗi trên Windows/macOS thiếu TeX
            lbl = Text(py_idx, font="Monospace", font_size=16, color=color)
            lbl.next_to(dots[-1], RIGHT, buff=0.15)
            self.add(lbl)
            self.label = lbl

    def creation_animation(self, run_time: float = 1.2):
        return LaggedStart(
            *[GrowFromCenter(d) for d in self[1]],
            *[Create(l) for l in self[0]],
            lag_ratio=0.15,
            run_time=run_time,
        )


# ── SliceHighlight ────────────────────────────────────────────────────────────

class SliceHighlight(VGroup):
    """
    Highlights a 2-D slice of a Tensor3D (fixes ONE index, both others are free).

    mode = 0 → frontal slice  (fixed x)
    mode = 1 → horizontal slice (fixed y)
    mode = 2 → lateral slice   (fixed z)
    """

    def __init__(
        self,
        tensor: Tensor3D,
        mode: int = 2,
        fixed_idx: int = 0,
        color: str = MATRIX_COLOR,
        fill_opacity: float = 0.45,
        label: bool = True,
    ):
        super().__init__()
        cs = tensor.cell_size
        nx, ny, nz = tensor.nx, tensor.ny, tensor.nz

        if mode == 0:           # fix x=fixed_idx  →  mặt dọc trái
            k = fixed_idx
            corners = [
                iso(k*cs,  0,       0),
                iso(k*cs,  ny*cs,   0),
                iso(k*cs,  ny*cs,   nz*cs),
                iso(k*cs,  0,       nz*cs),
            ]
            py_idx = f"X[{k}, :, :]"
        elif mode == 1:         # fix y=fixed_idx  →  mặt nằm ngang
            j = fixed_idx
            corners = [
                iso(0,      j*cs,  0),
                iso(nx*cs,  j*cs,  0),
                iso(nx*cs,  j*cs,  nz*cs),
                iso(0,      j*cs,  nz*cs),
            ]
            py_idx = f"X[:, {j}, :]"
        else:                   # fix z=fixed_idx  →  mặt trước/sau
            z = fixed_idx
            corners = [
                iso(0,      0,      z*cs),
                iso(nx*cs,  0,      z*cs),
                iso(nx*cs,  ny*cs,  z*cs),
                iso(0,      ny*cs,  z*cs),
            ]
            py_idx = f"X[:, :, {z}]"

        # Translate corners relative to tensor centre
        offset = (
            tensor.get_center()
            - iso(nx * cs / 2, ny * cs / 2, nz * cs / 2)
        )
        corners = [c + offset for c in corners]

        plane = Polygon(
            *corners,
            fill_color=color,
            fill_opacity=fill_opacity,
            stroke_color=color,
            stroke_width=2,
        )
        self.add(plane)

        if label:
            lbl = Text(py_idx, font="Monospace", font_size=16, color=color)
            lbl.next_to(plane, LEFT, buff=0.18)
            self.add(lbl)


# ── IndexLabel ────────────────────────────────────────────────────────────────

class IndexLabel(VGroup):
    """
    Hai dòng annotation: Python index + ký hiệu toán học (dạng text).
    Không dùng MathTex → không cần LaTeX cài sẵn.
    """

    def __init__(self, python_str: str, math_str: str, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        py  = Text(python_str, font="Monospace", font_size=18, color=color)
        mth = Text(math_str,   font="Monospace", font_size=16, color=color,
                   fill_opacity=0.8)
        mth.next_to(py, DOWN, buff=0.08)
        self.add(py, mth)
