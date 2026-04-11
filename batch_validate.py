#!/usr/bin/env python3
"""
batch_validate.py — Roda todos os validators em um diretório de sprites.

Uso:
  python batch_validate.py sprites/
  python batch_validate.py sprites/ --strict
"""
from pathlib import Path
import typer
import validate_palette
import validate_sprite

app = typer.Typer()

@app.command()
def main(
    directory: Path = typer.Argument(..., help="Directory with PNG sprites"),
    strict: bool = typer.Option(False, help="Exit 1 if any sprite fails"),
    tolerance: int = typer.Option(5, help="Palette tolerance"),
):
    """Validate all PNG sprites in a directory."""
    pngs = sorted(directory.glob("*.png"))
    if not pngs:
        typer.echo(f"No PNG files found in {directory}")
        raise typer.Exit(0)

    passed = failed = 0
    for png in pngs:
        pal = validate_palette.validate(png, tolerance=tolerance)
        spr = validate_sprite.validate(png)
        ok = pal.passed and spr.passed
        icon = "✅" if ok else "❌"
        typer.echo(f"{icon} {png.name}")
        if not ok:
            if not pal.passed:
                for v in pal.violations[:3]:
                    typer.echo(f"   palette: rgb{v.color} (×{v.count}px)")
            for w in spr.warnings:
                typer.echo(f"   sprite:  {w}")
            failed += 1
        else:
            passed += 1

    typer.echo(f"\n{'='*40}")
    typer.echo(f"Results: {passed} passed, {failed} failed out of {len(pngs)} sprites")

    if strict and failed > 0:
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
