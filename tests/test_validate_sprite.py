import pytest
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import validate_sprite as vs

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURES.mkdir(exist_ok=True)

def make_valid_sprite(path: Path) -> None:
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    for y in range(10, 54):
        for x in range(20, 44):
            img.putpixel((x, y), (120, 112, 104, 255))
    for x in range(22, 42):
        img.putpixel((x, 58), (13, 13, 20, 128))
    img.save(path)

def test_valid_sprite_passes_all_checks():
    path = FIXTURES / "valid_full.png"
    make_valid_sprite(path)
    result = vs.validate(path)
    assert result.size_ok is True
    assert result.has_alpha is True
    assert result.no_fringe is True

def test_wrong_size_fails():
    img = Image.new("RGBA", (32, 32), (120, 112, 104, 255))
    path = FIXTURES / "wrong_size.png"
    img.save(path)
    result = vs.validate(path)
    assert result.size_ok is False

def test_no_alpha_channel_fails():
    img = Image.new("RGB", (64, 64), (120, 112, 104))
    path = FIXTURES / "no_alpha.png"
    img.save(path)
    result = vs.validate(path)
    assert result.has_alpha is False

def test_color_fringe_detected():
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    img.putpixel((32, 32), (255, 255, 255, 96))
    path = FIXTURES / "fringe.png"
    img.save(path)
    result = vs.validate(path)
    assert result.no_fringe is False
