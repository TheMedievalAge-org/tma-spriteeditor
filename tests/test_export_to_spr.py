import pytest, struct, tempfile
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
import export_to_spr as ex

FIXTURES = Path(__file__).parent / "fixtures"
FIXTURES.mkdir(exist_ok=True)

def test_export_single_sprite():
    """Single 64x64 sprite exports to valid .spr with correct header."""
    img = Image.new("RGBA", (64, 64), (120, 112, 104, 255))
    path = FIXTURES / "export_test.png"
    img.save(path)

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.spr"
        ex.export([path], out)
        assert out.exists()
        assert out.stat().st_size > 0
        data = out.read_bytes()
        # signature (4 bytes) + count (4 bytes)
        count = struct.unpack_from("<I", data, 4)[0]
        assert count == 1

def test_export_preserves_sprite_count():
    """Exporting N sprites produces .spr with N in header count field."""
    sprites = []
    for i in range(5):
        img = Image.new("RGBA", (64, 64), (120 + i * 2, 112, 104, 255))
        p = FIXTURES / f"export_{i}.png"
        img.save(p)
        sprites.append(p)

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "multi.spr"
        ex.export(sprites, out)
        data = out.read_bytes()
        count = struct.unpack_from("<I", data, 4)[0]
        assert count == 5
