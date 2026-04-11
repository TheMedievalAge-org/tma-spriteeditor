#!/usr/bin/env python3
"""
Gera sprites de guerreiro para The Medieval Age.
Personagem 64×64 com armadura de couro tier 1.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from _template import new_sprite, draw_contact_shadow, SPRITE_SIZE

OUTPUT = Path(__file__).parent.parent.parent / "c-tma" / "tma-client" / "data" / "sprites" / "characters"

# Warrior colors (tier 1 — leather)
W = {
    "helm_light":   (110, 110, 120),   # iron helm highlight
    "helm_base":    (104, 104, 112),   # iron base
    "helm_shadow":  (72,  72,  80),    # iron shadow
    "skin_light":   (232, 200, 160),
    "skin_base":    (192, 160, 128),
    "skin_shadow":  (160, 120, 96),
    "armor_light":  (168, 104, 64),    # leather highlight
    "armor_base":   (138, 88,  48),    # leather base
    "armor_shadow": (106, 64,  32),    # leather shadow
    "armor_deep":   (74,  40,  16),    # leather dark
    "boot_base":    (74,  56,  40),    # dark leather boots
    "boot_shadow":  (50,  36,  24),
    "outline":      (30,  22,  14),
}

def draw_warrior_south(img: Image.Image) -> None:
    """Front-facing warrior (south direction)."""
    draw = ImageDraw.Draw(img)
    cx = 32  # center x

    # Contact shadow
    draw_contact_shadow(img, cx, 58, width=24, height=7)

    # BOOTS (feet) — y: 46-57
    draw.rectangle([cx-12, 47, cx-3, 57], fill=W["boot_base"])
    draw.rectangle([cx-12, 47, cx-12, 57], fill=W["boot_shadow"])
    draw.rectangle([cx+3, 47, cx+12, 57], fill=W["boot_base"])
    draw.rectangle([cx+12, 47, cx+12, 57], fill=W["boot_shadow"])

    # LEGS — y: 34-47
    draw.rectangle([cx-10, 34, cx-2, 47], fill=W["armor_shadow"])
    draw.rectangle([cx+2, 34, cx+10, 47], fill=W["armor_shadow"])
    # Belt line
    draw.line([(cx-10, 34), (cx+10, 34)], fill=W["armor_deep"])

    # BODY — y: 16-34
    draw.rectangle([cx-14, 16, cx+14, 34], fill=W["armor_base"])
    # Left shoulder (highlight — receives NW light)
    draw.rectangle([cx-16, 14, cx-8, 22], fill=W["armor_light"])
    # Right shoulder (shadow)
    draw.rectangle([cx+8, 14, cx+16, 22], fill=W["armor_shadow"])
    # Chest detail
    draw.rectangle([cx-4, 20, cx+4, 28], fill=W["armor_shadow"])
    draw.line([(cx-14, 16), (cx+14, 16)], fill=W["armor_light"])

    # LEFT ARM — y: 20-40, x: cx-22 to cx-14
    draw.rectangle([cx-22, 20, cx-14, 40], fill=W["armor_base"])
    draw.rectangle([cx-22, 20, cx-22, 40], fill=W["armor_light"])  # lit edge
    draw.rectangle([cx-14, 20, cx-14, 40], fill=W["armor_shadow"])

    # RIGHT ARM
    draw.rectangle([cx+14, 20, cx+22, 40], fill=W["armor_shadow"])
    draw.rectangle([cx+22, 20, cx+22, 40], fill=W["armor_deep"])

    # NECK — y: 12-16
    draw.rectangle([cx-4, 12, cx+4, 16], fill=W["skin_base"])

    # HEAD — y: 2-12
    draw.ellipse([cx-10, 2, cx+10, 14], fill=W["skin_base"])
    draw.arc([cx-10, 2, cx+10, 14], 0, 180, fill=W["skin_shadow"], width=1)

    # HELM — y: 0-10
    draw.ellipse([cx-11, 0, cx+11, 12], fill=W["helm_base"])
    draw.arc([cx-11, 0, cx+11, 12], 180, 360, fill=W["helm_light"], width=2)
    # Nasal bar
    draw.rectangle([cx-1, 6, cx+1, 12], fill=W["helm_shadow"])

    # Eyes (south face)
    draw.rectangle([cx-6, 7, cx-3, 9], fill=W["armor_deep"])
    draw.rectangle([cx+3, 7, cx+6, 9], fill=W["armor_deep"])


def draw_warrior_north(img: Image.Image) -> None:
    """Back-facing warrior (north direction)."""
    draw = ImageDraw.Draw(img)
    cx = 32

    draw_contact_shadow(img, cx, 58, width=24, height=7)

    # Boots
    draw.rectangle([cx-12, 47, cx-3, 57], fill=W["boot_base"])
    draw.rectangle([cx+3, 47, cx+12, 57], fill=W["boot_base"])
    draw.rectangle([cx+12, 47, cx+12, 57], fill=W["boot_shadow"])

    # Legs
    draw.rectangle([cx-10, 34, cx-2, 47], fill=W["armor_shadow"])
    draw.rectangle([cx+2, 34, cx+10, 47], fill=W["armor_shadow"])

    # Body back
    draw.rectangle([cx-14, 16, cx+14, 34], fill=W["armor_shadow"])
    draw.rectangle([cx-14, 16, cx-14, 34], fill=W["armor_base"])  # left edge lit

    # Shoulders (back — left shoulder now in shadow, right lit from NW)
    draw.rectangle([cx-16, 14, cx-8, 22], fill=W["armor_shadow"])
    draw.rectangle([cx+8, 14, cx+16, 22], fill=W["armor_light"])

    # Arms
    draw.rectangle([cx-22, 20, cx-14, 40], fill=W["armor_shadow"])
    draw.rectangle([cx+14, 20, cx+22, 40], fill=W["armor_base"])
    draw.rectangle([cx+14, 20, cx+14, 40], fill=W["armor_light"])

    # Neck
    draw.rectangle([cx-4, 12, cx+4, 16], fill=W["skin_shadow"])

    # Helm back
    draw.ellipse([cx-11, 0, cx+11, 12], fill=W["helm_shadow"])
    draw.arc([cx-11, 0, cx+11, 12], 180, 360, fill=W["helm_base"], width=2)


def make_warrior_idle(direction: str) -> Image.Image:
    img = new_sprite()
    if direction == "s":
        draw_warrior_south(img)
    elif direction == "n":
        draw_warrior_north(img)
    elif direction in ("e", "w"):
        # East/West: mirror of south with adjusted body
        draw_warrior_south(img)  # simplified — use south as base
        if direction == "w":
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for d in ["n", "e", "s", "w"]:
        sprite = make_warrior_idle(d)
        path = OUTPUT / f"warrior_idle_{d}.png"
        sprite.save(path)
        print(f"✅ warrior_idle_{d}.png")
