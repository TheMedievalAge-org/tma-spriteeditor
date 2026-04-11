#!/usr/bin/env python3
"""
Template para scripts de geração de sprites TMA.
Cada gerador cria um ou mais sprites PNG 64x64 RGBA.
"""
from pathlib import Path
from PIL import Image, ImageDraw

SPRITE_SIZE = 64
OUTPUT_DIR = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites"

# Paleta aprovada — subsets por material
STONE = {
    "highlight": (160, 152, 144),
    "base":      (120, 112, 104),
    "shadow":    (88,  80,  72),
    "deep":      (56,  48,  40),
    "outline":   (26,  20,  16),
}
EARTH = {
    "highlight": (160, 120, 72),
    "base":      (138, 104, 64),
    "shadow":    (106, 80,  48),
    "deep":      (74,  56,  32),
}
FOREST = {
    "highlight": (90,  144, 80),
    "base":      (74,  120, 64),
    "shadow":    (56,  96,  48),
    "deep":      (40,  72,  32),
}
WATER = {
    "highlight": (128, 184, 224),
    "base":      (32,  96,  160),
    "shadow":    (16,  56,  128),
    "deep":      (10,  32,  96),
}

def new_sprite() -> Image.Image:
    """Create blank 64x64 RGBA sprite."""
    return Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))

def draw_contact_shadow(img: Image.Image, center_x: int, base_y: int,
                         width: int = 20, height: int = 6) -> None:
    """Draw contact shadow ellipse at base of object."""
    draw = ImageDraw.Draw(img)
    x0 = center_x - width // 2
    x1 = center_x + width // 2
    y0 = base_y - height // 2
    y1 = base_y + height // 2
    draw.ellipse([x0, y0, x1, y1], fill=(13, 13, 20, 128))

def iso_top_face(img: Image.Image, color_top: tuple, color_edge: tuple,
                  y_offset: int = 0) -> None:
    """Draw the top face of an isometric tile (diamond shape)."""
    draw = ImageDraw.Draw(img)
    # Diamond: top(32,0+y), right(64,16+y), bottom(32,32+y), left(0,16+y)
    points = [
        (32, y_offset),
        (63, 16 + y_offset),
        (32, 32 + y_offset),
        (0,  16 + y_offset),
    ]
    draw.polygon(points, fill=color_top, outline=color_edge)
