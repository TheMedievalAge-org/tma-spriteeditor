# tma-spriteeditor

Ferramentas de validação e exportação de sprites para **The Medieval Age** (OTClient 64×64 + TFS).

## Instalação

```bash
pip install -r requirements.txt
```

## Ferramentas

### validate_palette.py
Verifica se um sprite usa apenas cores da paleta aprovada.
```bash
python validate_palette.py meu_sprite.png
python validate_palette.py meu_sprite.png --tolerance 5 --strict
```

### validate_sprite.py
Checklist técnico: tamanho 64×64, canal alpha, sem fringe colorido.
```bash
python validate_sprite.py meu_sprite.png
```

### export_to_spr.py
Converte PNGs para formato `.spr` do OTClient (RLE encoding).
```bash
python export_to_spr.py sprites/*.png --output Tibia.spr
```

### batch_validate.py
Valida todos os sprites de um diretório de uma vez.
```bash
python batch_validate.py sprites/
python batch_validate.py sprites/ --strict
```

## Testes

```bash
pytest tests/ -v
```

## Para subagents (Codex/Gemini)

Contexto comprimido para incluir em prompts:

```
TMA SPRITE RULES:
- Canvas: 64×64px RGBA PNG
- Style: painterly pixel art, isometric 2:1
- Light: NW source — top=100%, left=85%, right=65%
- Contact shadow: dark ellipse (rgba 0,0,0,128) at base
- Validate: python validate_palette.py <file> && python validate_sprite.py <file>
- Palette: see palette.json (67 approved colors)
```

## Paleta

Ver `palette.json` para lista completa de 67 cores aprovadas.
Ver `palette.gpl` para importar no GIMP ou Aseprite.
