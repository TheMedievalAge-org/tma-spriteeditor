#!/usr/bin/env python3
"""
validate_palette.py — Verifica se um sprite usa apenas cores da paleta aprovada.

Uso:
  python validate_palette.py sprite.png
  python validate_palette.py sprite.png --tolerance 5 --palette palette.json
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import typer
from PIL import Image

PALETTE_PATH = Path(__file__).parent / "palette.json"


@dataclass
class Violation:
    color: tuple
    count: int
    closest_approved: str
    distance: int


@dataclass
class ValidationResult:
    passed: bool
    violations: list = field(default_factory=list)
    total_pixels: int = 0
    opaque_pixels: int = 0

    def __str__(self) -> str:
        if self.passed:
            return f"PASS — {self.opaque_pixels} opaque pixels, all within approved palette"
        lines = [f"FAIL — {len(self.violations)} unapproved color(s) found:"]
        for v in self.violations[:10]:
            lines.append(
                f"  rgb{v.color} x {v.count}px — closest: {v.closest_approved} (delta{v.distance})"
            )
        if len(self.violations) > 10:
            lines.append(f"  ... and {len(self.violations) - 10} more")
        return "\n".join(lines)


def load_palette(palette_path: Path = PALETTE_PATH) -> dict:
    """Load approved palette as dict of name -> (r, g, b)."""
    with open(palette_path) as f:
        data = json.load(f)
    result = {}
    for name, hex_color in data["colors"].items():
        if not hex_color or len(hex_color) < 7 or hex_color == "#00000000":
            continue
        h = hex_color.lstrip("#")[:6]
        result[name] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return result


def color_distance(c1: tuple, c2: tuple) -> int:
    """Max-channel color distance (fast approximation)."""
    return max(abs(c1[0]-c2[0]), abs(c1[1]-c2[1]), abs(c1[2]-c2[2]))


def find_closest(color: tuple, palette: dict) -> tuple:
    """Find closest palette color name and distance."""
    best_name, best_dist = "", 999
    for name, approved in palette.items():
        d = color_distance(color, approved)
        if d < best_dist:
            best_dist, best_name = d, name
    return best_name, best_dist


def validate(
    image_path: Path,
    palette_path: Path = PALETTE_PATH,
    tolerance: int = 5,
) -> ValidationResult:
    """Validate that all opaque pixels use approved palette colors."""
    palette = load_palette(palette_path)
    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())

    unapproved: dict = {}
    opaque = 0

    for r, g, b, a in pixels:
        if a < 128:
            continue
        opaque += 1
        color = (r, g, b)
        _, dist = find_closest(color, palette)
        if dist > tolerance:
            unapproved[color] = unapproved.get(color, 0) + 1

    violations = []
    for color, count in unapproved.items():
        closest, dist = find_closest(color, palette)
        violations.append(Violation(color=color, count=count,
                                     closest_approved=closest, distance=dist))
    violations.sort(key=lambda v: v.count, reverse=True)

    return ValidationResult(
        passed=len(violations) == 0,
        violations=violations,
        total_pixels=len(pixels),
        opaque_pixels=opaque,
    )


app = typer.Typer()

@app.command()
def main(
    image: Path = typer.Argument(..., help="PNG sprite to validate"),
    palette: Path = typer.Option(PALETTE_PATH, help="palette.json path"),
    tolerance: int = typer.Option(5, help="Max color distance allowed"),
    strict: bool = typer.Option(False, help="Exit code 1 on failure"),
):
    """Validate sprite palette against approved TMA colors."""
    result = validate(image, palette, tolerance)
    typer.echo(str(result))
    if strict and not result.passed:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
