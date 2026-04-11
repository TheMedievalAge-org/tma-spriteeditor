#!/usr/bin/env python3
"""
validate_sprite.py — Checklist técnico completo para sprites TMA.
Verifica: tamanho 64×64, canal alpha, sem fringe colorido, uso de canvas.

Uso: python validate_sprite.py sprite.png
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import typer
from PIL import Image

SPRITE_SIZE = 64
FRINGE_ALPHA_MIN = 64
FRINGE_ALPHA_MAX = 127
FRINGE_COLOR_RANGE = 100


@dataclass
class SpriteValidationResult:
    size_ok: bool
    has_alpha: bool
    no_fringe: bool
    canvas_usage: float
    warnings: list = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.size_ok and self.has_alpha and self.no_fringe

    def __str__(self) -> str:
        icon = "✅" if self.passed else "❌"
        lines = [f"{icon} Sprite validation:"]
        lines.append(f"  Size 64×64:    {'✅' if self.size_ok else '❌'}")
        lines.append(f"  Alpha channel: {'✅' if self.has_alpha else '❌'}")
        lines.append(f"  No fringe:     {'✅' if self.no_fringe else '❌'}")
        lines.append(f"  Canvas usage:  {self.canvas_usage:.0%}")
        for w in self.warnings:
            lines.append(f"  ⚠️  {w}")
        return "\n".join(lines)


def validate(image_path: Path) -> SpriteValidationResult:
    img = Image.open(image_path)
    warnings = []

    size_ok = img.size == (SPRITE_SIZE, SPRITE_SIZE)
    if not size_ok:
        warnings.append(f"Size is {img.size}, expected ({SPRITE_SIZE}, {SPRITE_SIZE})")

    has_alpha = img.mode == "RGBA"
    if not has_alpha:
        warnings.append(f"Mode is {img.mode}, expected RGBA")

    no_fringe = True
    if has_alpha:
        for r, g, b, a in img.convert("RGBA").getdata():
            if FRINGE_ALPHA_MIN < a <= FRINGE_ALPHA_MAX:
                # Fringe: either colorful semi-transparent pixel, or bright semi-transparent pixel
                colorful = max(r, g, b) - min(r, g, b) > FRINGE_COLOR_RANGE
                bright = max(r, g, b) > FRINGE_COLOR_RANGE
                if colorful or bright:
                    no_fringe = False
                    warnings.append("Fringe detected: semi-transparent colored pixels found")
                    break

    opaque = 0
    total = SPRITE_SIZE * SPRITE_SIZE
    if has_alpha:
        for _, _, _, a in img.convert("RGBA").getdata():
            if a >= 128:
                opaque += 1
    canvas_usage = opaque / total
    if canvas_usage < 0.1:
        warnings.append(f"Only {canvas_usage:.0%} canvas used — sprite may be too small")
    elif canvas_usage > 0.95:
        warnings.append("95%+ canvas used — may lack breathing room")

    return SpriteValidationResult(
        size_ok=size_ok,
        has_alpha=has_alpha,
        no_fringe=no_fringe,
        canvas_usage=canvas_usage,
        warnings=warnings,
    )


app = typer.Typer()

@app.command()
def main(
    image: Path = typer.Argument(..., help="PNG sprite to validate"),
    strict: bool = typer.Option(False, help="Exit code 1 on failure"),
):
    """Run full technical checklist on a sprite."""
    result = validate(image)
    typer.echo(str(result))
    if strict and not result.passed:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
