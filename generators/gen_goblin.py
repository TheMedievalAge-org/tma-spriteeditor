#!/usr/bin/env python3
"""Gera sprites de goblin para The Medieval Age."""
from pathlib import Path
from PIL import Image, ImageDraw
from _template import new_sprite, draw_contact_shadow, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "monsters"

G = {
    "skin_light":   (100, 130, 72),   # greenish skin highlight
    "skin_base":    (80,  110, 56),   # base goblin skin
    "skin_shadow":  (60,  85,  40),   # shadow
    "skin_deep":    (40,  60,  26),
    "cloth_base":   (90,  64,  40),   # ragged cloth
    "cloth_shadow": (68,  48,  28),
    "eye_red":      (204, 32,  32),   # menacing red eyes
    "eye_white":    (232, 200, 160),
    "tooth":        (220, 210, 180),
    "outline":      (26,  36,  16),
}

def draw_goblin_south(img: Image.Image, crouched: bool = False) -> None:
    draw = ImageDraw.Draw(img)
    cx = 32
    y_offset = 2 if crouched else 0  # slight crouch animation

    draw_contact_shadow(img, cx, 58 + y_offset, width=18, height=5)

    # FEET — stubby
    draw.rectangle([cx-9, 50+y_offset, cx-3, 57+y_offset], fill=G["skin_shadow"])
    draw.rectangle([cx+3, 50+y_offset, cx+9, 57+y_offset], fill=G["skin_shadow"])

    # LEGS — short
    draw.rectangle([cx-8, 39+y_offset, cx-2, 51+y_offset], fill=G["cloth_shadow"])
    draw.rectangle([cx+2, 39+y_offset, cx+8, 51+y_offset], fill=G["cloth_shadow"])

    # BODY — hunched, wider at bottom
    draw.polygon([
        (cx-12, 22+y_offset),
        (cx+12, 22+y_offset),
        (cx+14, 39+y_offset),
        (cx-14, 39+y_offset),
    ], fill=G["cloth_base"])
    draw.line([(cx-12, 22+y_offset), (cx+12, 22+y_offset)], fill=G["skin_light"])

    # ARMS — long, hanging
    # Left arm (lit)
    draw.rectangle([cx-18, 24+y_offset, cx-10, 46+y_offset], fill=G["skin_base"])
    draw.rectangle([cx-18, 24+y_offset, cx-18, 46+y_offset], fill=G["skin_light"])
    # Claws
    for i in range(3):
        draw.rectangle([cx-18+i*2, 44+y_offset, cx-17+i*2, 48+y_offset], fill=G["outline"])

    # Right arm (shadow)
    draw.rectangle([cx+10, 24+y_offset, cx+18, 46+y_offset], fill=G["skin_shadow"])
    for i in range(3):
        draw.rectangle([cx+10+i*2, 44+y_offset, cx+11+i*2, 48+y_offset], fill=G["outline"])

    # HEAD — large, round
    draw.ellipse([cx-12, 8+y_offset, cx+12, 26+y_offset], fill=G["skin_base"])
    draw.arc([cx-12, 8+y_offset, cx+12, 26+y_offset], 180, 360, fill=G["skin_light"], width=2)

    # EARS — large pointy ears going up
    # Left ear
    draw.polygon([
        (cx-12, 12+y_offset),
        (cx-20, 4+y_offset),
        (cx-8, 10+y_offset),
    ], fill=G["skin_base"])
    draw.polygon([
        (cx-12, 12+y_offset),
        (cx-20, 4+y_offset),
        (cx-8, 10+y_offset),
    ], outline=G["outline"])
    # Right ear
    draw.polygon([
        (cx+12, 12+y_offset),
        (cx+20, 4+y_offset),
        (cx+8, 10+y_offset),
    ], fill=G["skin_shadow"])
    draw.polygon([
        (cx+12, 12+y_offset),
        (cx+20, 4+y_offset),
        (cx+8, 10+y_offset),
    ], outline=G["outline"])

    # EYES — red and menacing
    draw.ellipse([cx-8, 14+y_offset, cx-3, 18+y_offset], fill=G["eye_red"])
    draw.ellipse([cx+3, 14+y_offset, cx+8, 18+y_offset], fill=G["eye_red"])
    # Eye shine
    draw.point((cx-6, 15+y_offset), fill=(255, 200, 200))
    draw.point((cx+5, 15+y_offset), fill=(255, 200, 200))

    # MOUTH — toothy grin
    draw.line([(cx-6, 21+y_offset), (cx+6, 21+y_offset)], fill=G["outline"])
    draw.rectangle([cx-4, 21+y_offset, cx-2, 23+y_offset], fill=G["tooth"])
    draw.rectangle([cx+2, 21+y_offset, cx+4, 23+y_offset], fill=G["tooth"])


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Idle frame 0 (normal)
    img0 = new_sprite()
    draw_goblin_south(img0, crouched=False)
    img0.save(OUTPUT / "goblin_idle_s_0.png")
    print("✅ goblin_idle_s_0.png")

    # Idle frame 1 (slightly crouched — breathing animation)
    img1 = new_sprite()
    draw_goblin_south(img1, crouched=True)
    img1.save(OUTPUT / "goblin_idle_s_1.png")
    print("✅ goblin_idle_s_1.png")
