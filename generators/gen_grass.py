#!/usr/bin/env python3
"""Gera sprites de grama para The Medieval Age."""
import random
from pathlib import Path
from PIL import Image, ImageDraw
from _template import new_sprite, FOREST, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "terrain"

# Grass-specific colors
GRASS = {
    "top_light":  (90,  144, 80),   # NW highlight
    "top_base":   (74,  120, 64),   # base green
    "top_shadow": (56,  96,  48),   # SE shadow
    "left_wall":  (50,  85,  42),   # left face (85% brightness)
    "right_wall": (38,  65,  32),   # right face (65% brightness)
    "tuft_light": (106, 172, 96),   # individual grass tufts
    "tuft_dark":  (58,  100, 50),
    "outline":    (30,  50,  24),
}

def make_grass_dense(seed: int = 42) -> Image.Image:
    random.seed(seed)
    img = new_sprite()
    draw = ImageDraw.Draw(img)

    # --- TOP FACE (diamond) ---
    # Fill with gradient: NW lighter, SE darker
    # Approximate gradient by filling rows of the diamond
    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            # Check if pixel is inside the diamond
            # Diamond: vertices at (32,0), (63,16), (32,32), (0,16)
            # Use barycentric test via edge functions
            dx = x - 32
            dy = y - 16
            # Simplified: in diamond if |dx|/2 + |dy| <= 16
            if abs(dx) / 2 + abs(dy) <= 16:
                # Gradient based on position
                t = (x + y) / (SPRITE_SIZE * 2)  # 0=NW, 1=SE
                r = int(GRASS["top_light"][0] * (1-t) + GRASS["top_shadow"][0] * t)
                g_val = int(GRASS["top_light"][1] * (1-t) + GRASS["top_shadow"][1] * t)
                b = int(GRASS["top_light"][2] * (1-t) + GRASS["top_shadow"][2] * t)
                img.putpixel((x, y), (r, g_val, b, 255))

    # --- GRASS TUFTS at diamond edges ---
    # Generate tufts along the top edges (NW and NE edges of diamond)
    # NW edge: from (32,0) to (0,16) — left side
    for i in range(8):
        t = i / 7
        base_x = int(32 - 32 * t)
        base_y = int(16 * t)
        # Tuft: 1-3 pixels upward
        height = random.randint(1, 3)
        color = GRASS["tuft_light"] if random.random() > 0.4 else GRASS["tuft_dark"]
        for h in range(height):
            if 0 <= base_x < SPRITE_SIZE and 0 <= base_y - h < SPRITE_SIZE:
                img.putpixel((base_x, base_y - h), color + (255,))

    # NE edge: from (32,0) to (63,16) — right side
    for i in range(8):
        t = i / 7
        base_x = int(32 + 31 * t)
        base_y = int(16 * t)
        height = random.randint(1, 2)
        color = GRASS["tuft_dark"]  # NE side in shadow
        for h in range(height):
            if 0 <= base_x < SPRITE_SIZE and 0 <= base_y - h < SPRITE_SIZE:
                img.putpixel((base_x, base_y - h), color + (255,))

    return img


def make_grass_sparse(seed: int = 99) -> Image.Image:
    """Variação mais clara e rala."""
    random.seed(seed)
    img = new_sprite()

    SPARSE = {
        "top_light":  (106, 160, 96),
        "top_base":   (90, 136, 80),
        "top_shadow": (70, 108, 60),
    }

    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            dx = x - 32
            dy = y - 16
            if abs(dx) / 2 + abs(dy) <= 16:
                t = (x + y) / (SPRITE_SIZE * 2)
                r = int(SPARSE["top_light"][0] * (1-t) + SPARSE["top_shadow"][0] * t)
                g_val = int(SPARSE["top_light"][1] * (1-t) + SPARSE["top_shadow"][1] * t)
                b = int(SPARSE["top_light"][2] * (1-t) + SPARSE["top_shadow"][2] * t)
                img.putpixel((x, y), (r, g_val, b, 255))

    return img


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)

    dense = make_grass_dense()
    dense.save(OUTPUT / "grass_dense.png")
    print(f"✅ grass_dense.png saved to {OUTPUT}")

    sparse = make_grass_sparse()
    sparse.save(OUTPUT / "grass_sparse.png")
    print(f"✅ grass_sparse.png saved to {OUTPUT}")
