#!/usr/bin/env python3
"""Gera tiles de pedra para The Medieval Age."""
import random
from pathlib import Path
from PIL import Image
from _template import new_sprite, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "terrain"

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] * (1-t) + c2[i] * t) for i in range(3))

def add_noise(color, amount=6):
    """Add subtle per-pixel noise to simulate stone granularity."""
    r = max(0, min(255, color[0] + random.randint(-amount, amount)))
    g = max(0, min(255, color[1] + random.randint(-amount, amount)))
    b = max(0, min(255, color[2] + random.randint(-amount, amount)))
    return (r, g, b)

def draw_crack(img, x0, y0, x1, y1, color=(56, 40, 32)):
    """Draw a crack line using Bresenham's algorithm."""
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        if 0 <= x0 < SPRITE_SIZE and 0 <= y0 < SPRITE_SIZE:
            img.putpixel((x0, y0), color + (255,))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def make_stone_floor(seed=10) -> Image.Image:
    random.seed(seed)
    img = new_sprite()
    LIGHT = (160, 152, 144)
    DARK  = (88, 80, 72)

    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            dx = x - 32
            dy = y - 16
            if abs(dx) / 2 + abs(dy) <= 16:
                t = (x + y) / (SPRITE_SIZE * 2)
                base = lerp_color(LIGHT, DARK, t)
                noisy = add_noise(base, 5)
                img.putpixel((x, y), noisy + (255,))

    # Add 2 subtle cracks
    random.seed(seed)
    for _ in range(2):
        # Random crack within diamond bounds
        cx = random.randint(15, 48)
        cy = random.randint(10, 28)
        length = random.randint(6, 14)
        angle_x = random.choice([-1, 1]) * random.randint(3, 8)
        angle_y = random.randint(2, 6)
        draw_crack(img, cx, cy, cx + angle_x, cy + angle_y, (56, 48, 40))

    return img

def make_stone_dungeon(seed=20) -> Image.Image:
    """Darker stone for dungeons with more cracks."""
    random.seed(seed)
    img = new_sprite()
    LIGHT = (88, 80, 72)
    DARK  = (40, 32, 26)

    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            dx = x - 32
            dy = y - 16
            if abs(dx) / 2 + abs(dy) <= 16:
                t = (x + y) / (SPRITE_SIZE * 2)
                base = lerp_color(LIGHT, DARK, t)
                noisy = add_noise(base, 4)
                img.putpixel((x, y), noisy + (255,))

    for _ in range(4):  # more cracks in dungeon
        cx = random.randint(15, 48)
        cy = random.randint(10, 28)
        angle_x = random.choice([-1, 1]) * random.randint(4, 10)
        angle_y = random.randint(1, 5)
        draw_crack(img, cx, cy, cx + angle_x, cy + angle_y, (26, 20, 16))

    return img

if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    make_stone_floor().save(OUTPUT / "stone_floor.png")
    print("✅ stone_floor.png")
    make_stone_dungeon().save(OUTPUT / "stone_dungeon.png")
    print("✅ stone_dungeon.png")
