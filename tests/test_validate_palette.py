import pytest
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import validate_palette as vp

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURES.mkdir(exist_ok=True)

def test_valid_sprite_passes():
    """Sprite using only approved palette colors should pass."""
    img = Image.new("RGBA", (64, 64), (120, 112, 104, 255))  # stone_gray
    img.save(FIXTURES / "valid_sprite.png")
    result = vp.validate(FIXTURES / "valid_sprite.png")
    assert result.passed is True
    assert len(result.violations) == 0

def test_invalid_palette_fails():
    """Sprite with unapproved color should fail."""
    img = Image.new("RGBA", (64, 64), (255, 0, 128, 255))  # hot pink
    img.save(FIXTURES / "invalid_palette.png")
    result = vp.validate(FIXTURES / "invalid_palette.png")
    assert result.passed is False
    assert len(result.violations) > 0
    assert (255, 0, 128) in [v.color for v in result.violations]

def test_transparent_pixels_are_ignored():
    """Fully transparent pixels should not trigger violations."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    img.save(FIXTURES / "transparent.png")
    result = vp.validate(FIXTURES / "transparent.png")
    assert result.passed is True

def test_tolerance_allows_near_matches():
    """Colors within tolerance=5 of an approved color should pass."""
    # stone_gray is (120, 112, 104) — (122, 112, 104) is within tolerance 5
    img = Image.new("RGBA", (64, 64), (122, 112, 104, 255))
    img.save(FIXTURES / "near_match.png")
    result = vp.validate(FIXTURES / "near_match.png", tolerance=5)
    assert result.passed is True
