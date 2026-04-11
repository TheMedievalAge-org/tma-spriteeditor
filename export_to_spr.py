#!/usr/bin/env python3
"""
export_to_spr.py — Exporta PNGs para formato .spr do OTClient.
Suporta sprites 64x64. Compatible com OTClient Redemption Rev 2.760 com sprite-size=64.

Uso:
  python export_to_spr.py sprite1.png sprite2.png --output Tibia.spr
  python export_to_spr.py sprites/*.png --output Tibia.spr
"""
from __future__ import annotations
import struct
from pathlib import Path
from typing import Sequence
import typer
from PIL import Image

SPRITE_SIZE = 64


def encode_sprite_rle(rgba_data: bytes) -> bytes:
    """Encode sprite using OTClient RLE: pairs of (transparent_count, colored_count, rgb_bytes...)"""
    pixels = [(rgba_data[i], rgba_data[i+1], rgba_data[i+2], rgba_data[i+3])
               for i in range(0, len(rgba_data), 4)]
    encoded = bytearray()
    i = 0
    while i < len(pixels):
        transparent = 0
        while i < len(pixels) and pixels[i][3] == 0:
            transparent += 1
            i += 1
        colored = []
        while i < len(pixels) and pixels[i][3] > 0:
            colored.append(pixels[i])
            i += 1
        encoded += struct.pack("<H", transparent)
        encoded += struct.pack("<H", len(colored))
        for r, g, b, a in colored:
            encoded += struct.pack("<BBB", r, g, b)
    return bytes(encoded)


def sprite_to_bytes(image_path: Path) -> bytes:
    """Convert a PNG sprite to OTClient .spr entry bytes."""
    img = Image.open(image_path).convert("RGBA")
    if img.size != (SPRITE_SIZE, SPRITE_SIZE):
        raise ValueError(f"{image_path}: expected {SPRITE_SIZE}x{SPRITE_SIZE}, got {img.size}")
    encoded = encode_sprite_rle(img.tobytes())
    # Header: colorKey (1B) + always-opaque (1B) + reserved (1B) + data_size (2B)
    header = struct.pack("<BBBH", 0x00, 0xFF, 0x00, len(encoded))
    return header + encoded


def export(sprite_paths: Sequence[Path], output_path: Path) -> None:
    """Write a .spr file from a list of PNG sprite files."""
    sprite_data_list = [sprite_to_bytes(p) for p in sprite_paths]
    count = len(sprite_data_list)
    base_offset = 4 + 4 + (4 * count)
    offsets = []
    current = base_offset
    for data in sprite_data_list:
        offsets.append(current)
        current += len(data)
    with open(output_path, "wb") as f:
        f.write(struct.pack("<I", 0x00000000))
        f.write(struct.pack("<I", count))
        for offset in offsets:
            f.write(struct.pack("<I", offset))
        for data in sprite_data_list:
            f.write(data)


app = typer.Typer()

@app.command()
def main(
    images: list[Path] = typer.Argument(..., help="PNG sprites to export"),
    output: Path = typer.Option("Tibia.spr", "--output", "-o", help="Output .spr file"),
):
    """Export PNG sprites to OTClient .spr format."""
    typer.echo(f"Exporting {len(images)} sprite(s) to {output}...")
    export(images, output)
    size_kb = output.stat().st_size / 1024
    typer.echo(f"Done — {output} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    app()
