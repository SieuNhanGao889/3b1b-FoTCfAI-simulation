# Tensor in AI – Manim Animation (Part 1)

**Style:** 3Blue1Brown-inspired
**Duration:** ~1:30

---

## Project Structure

```
tensor_animation/
├── README.md
├── main.py                  # Entry point – renders all scenes in order
├── config.py                # Global color palette, timing constants
├── media/                   # Auto-generated outputs (images, videos, LaTeX, text)
├── scenes/
│   ├── scene_1a_point_to_block.py   # Scalar → Vector → Matrix → Tensor
│   ├── scene_1b_recommender.py      # Recommendation system example
│   ├── scene_1c_data_explosion.py   # Data growth → Low-rank motivation
│   └── __init__.py
├── utils/
│   ├── tensor_objects.py    # Reusable 3D tensor components
│   └── __init__.py
└── assets/                  # (optional) custom SVGs / fonts
```

---

## Setup

### Prerequisites

**Ubuntu / Debian**

```bash
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg texlive
```

**macOS**

```bash
brew install cairo pango ffmpeg
```

**Install Manim**

```bash
pip install manim
```

---

## Usage

### Render Individual Scenes

**Low quality (fast preview)**

```bash
manim -pql scenes/scene_1a_point_to_block.py PointToBlock
manim -pql scenes/scene_1b_recommender.py RecommenderTensor
manim -pql scenes/scene_1c_data_explosion.py DataExplosion
```

**High quality (1080p)**

```bash
manim -pqh scenes/scene_1a_point_to_block.py PointToBlock
```

---

### Render Full Animation (All Scenes)

```bash
manim -pqh main.py TensorPart1
```

---

## Media Output

All rendered outputs are stored automatically in:

```
media/
├── images/      # Frame images
├── videos/      # Final and partial renders
├── Tex/         # LaTeX intermediates
└── texts/       # SVG text renders
```

---

## Color Palette (3B1B-inspired)

| Role              | Hex                 |
| ----------------- | ------------------- |
| Background        | `#0d0d0d`           |
| Tensor (3D block) | `#1e90ff → #00bfff` |
| Vector            | `#ffaa33`           |
| Matrix            | `#66cc88`           |
| Sum node (+)      | `#55aaff`           |
| Product node (×)  | `#ff6633`           |
| Math text         | `#ffffff`           |
| Highlight / glow  | `#ffe066`           |

---

## Notes

* The `media/` folder can grow very large due to partial renders.
* You can safely delete `media/videos/*/partial_movie_files/` if you only need final outputs.
* Structure is modular: scenes are independent and reusable.
