#!/usr/bin/env python3
"""Gera módulos de parede de casa para The Medieval Age."""
from pathlib import Path
from PIL import Image, ImageDraw
from _template import new_sprite, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "constructions"

STONE_WALL = {
    "north_light":  (168, 158, 148),   # lit face
    "north_base":   (140, 130, 120),
    "north_shadow": (112, 102, 92),
    "west_light":   (140, 130, 120),   # side face
    "west_base":    (112, 102, 92),
    "west_shadow":  (88,  78,  68),
    "mortar":       (88,  72,  56),    # mortar lines
    "window_dark":  (24,  20,  18),    # window interior
    "window_frame": (96,  80,  64),    # window wood frame
}

def draw_stone_blocks(img: Image.Image, draw: ImageDraw.ImageDraw,
                       x0: int, y0: int, width: int, height: int,
                       base_color: tuple, shadow_color: tuple,
                       mortar_color: tuple) -> None:
    """Draw stone block pattern with mortar lines."""
    # Fill area with base color
    draw.rectangle([x0, y0, x0+width-1, y0+height-1], fill=base_color)

    # Horizontal mortar lines every 12px
    for y in range(y0, y0+height, 12):
        if y0 < y < y0+height:
            draw.line([(x0, y), (x0+width-1, y)], fill=mortar_color)

    # Vertical mortar (alternating rows for brick pattern)
    block_height = 12
    for row, y in enumerate(range(y0, y0+height, block_height)):
        offset = 9 if row % 2 == 0 else 0
        for x in range(x0 + offset, x0+width, 18):
            draw.line([(x, y), (x, min(y+block_height, y0+height))], fill=mortar_color)

    # Bottom shadow
    if y0+height < SPRITE_SIZE:
        draw.line([(x0, y0+height-1), (x0+width-1, y0+height-1)], fill=shadow_color)


def make_house_wall_n() -> Image.Image:
    """North-facing wall — receives most light."""
    img = new_sprite()
    draw = ImageDraw.Draw(img)

    # North wall occupies bottom 40px of sprite, full width
    wall_y0 = 24
    wall_height = 40

    draw_stone_blocks(img, draw, 0, wall_y0, SPRITE_SIZE, wall_height,
                       STONE_WALL["north_base"], STONE_WALL["north_shadow"],
                       STONE_WALL["mortar"])

    # Top edge highlight (roof line)
    draw.line([(0, wall_y0), (SPRITE_SIZE-1, wall_y0)],
               fill=STONE_WALL["north_light"])
    draw.line([(0, wall_y0+1), (SPRITE_SIZE-1, wall_y0+1)],
               fill=STONE_WALL["north_base"])

    return img


def make_house_wall_w() -> Image.Image:
    """West-facing wall — lateral light, slightly darker."""
    img = new_sprite()
    draw = ImageDraw.Draw(img)

    wall_y0 = 24
    wall_height = 40

    draw_stone_blocks(img, draw, 0, wall_y0, SPRITE_SIZE, wall_height,
                       STONE_WALL["west_base"], STONE_WALL["west_shadow"],
                       STONE_WALL["mortar"])

    draw.line([(0, wall_y0), (SPRITE_SIZE-1, wall_y0)],
               fill=STONE_WALL["west_light"])

    return img


def make_house_wall_window_n() -> Image.Image:
    """North wall with window opening."""
    img = make_house_wall_n()
    draw = ImageDraw.Draw(img)

    # Window: centered, 16×20px, positioned mid-wall
    wx0, wy0 = 24, 28
    ww, wh = 16, 20

    # Window interior (dark)
    draw.rectangle([wx0, wy0, wx0+ww-1, wy0+wh-1], fill=STONE_WALL["window_dark"])

    # Window frame (wood)
    draw.rectangle([wx0-2, wy0-2, wx0+ww+1, wy0+wh+1],
                    outline=STONE_WALL["window_frame"], width=2)

    # Window sill
    draw.rectangle([wx0-3, wy0+wh, wx0+ww+2, wy0+wh+3],
                    fill=STONE_WALL["north_light"])

    return img


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    make_house_wall_n().save(OUTPUT / "house_wall_n.png")
    print("✅ house_wall_n.png")
    make_house_wall_w().save(OUTPUT / "house_wall_w.png")
    print("✅ house_wall_w.png")
    make_house_wall_window_n().save(OUTPUT / "house_wall_window_n.png")
    print("✅ house_wall_window_n.png")
