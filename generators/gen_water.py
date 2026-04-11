#!/usr/bin/env python3
"""Gera sprites de água animada para The Medieval Age."""
from pathlib import Path
from PIL import Image
from _template import new_sprite, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "terrain"

WATER = {
    "highlight": (128, 184, 224),
    "base":      (32,  96,  160),
    "mid":       (22,  76,  136),
    "shadow":    (16,  56,  128),
    "deep":      (10,  32,  96),
}

def lerp(a, b, t):
    return int(a * (1-t) + b * t)

def lerp_color(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))

def make_water_frame(frame: int) -> Image.Image:
    """
    frame 0-3: highlight position shifts 0→8→16→8 px rightward
    ripple lines shift position each frame
    """
    img = new_sprite()
    highlight_offset = [0, 8, 16, 8][frame]

    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            dx = x - 32
            dy = y - 16
            if abs(dx) / 2 + abs(dy) <= 16:
                # Base gradient: dark center to medium
                dist_from_center = ((dx**2) + (dy*2)**2) ** 0.5
                t = min(dist_from_center / 24, 1.0)
                base = lerp_color(WATER["mid"], WATER["shadow"], t)

                # Ripple lines: horizontal within diamond
                ripple_y = (y + frame * 4) % 10  # shift each frame
                if ripple_y < 2:
                    base = lerp_color(base, WATER["highlight"], 0.3)

                # Moving highlight spot
                hx = 32 + highlight_offset
                hy = 14
                dist_to_highlight = abs(x - hx) + abs(y - hy) * 2
                if dist_to_highlight < 8:
                    strength = 1 - dist_to_highlight / 8
                    base = lerp_color(base, WATER["highlight"], strength * 0.6)

                img.putpixel((x, y), base + (255,))

    return img

if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for i in range(4):
        frame = make_water_frame(i)
        path = OUTPUT / f"water_frame_{i}.png"
        frame.save(path)
        print(f"✅ water_frame_{i}.png")
