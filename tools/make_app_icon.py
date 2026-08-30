from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT / "assets"
ICONSET_DIR = ASSET_DIR / "Folimeld.iconset"
ICONSET_DIR.mkdir(parents=True, exist_ok=True)

sizes = [16, 32, 64, 128, 256, 512, 1024]

# Build a simple PDF-style icon: white page with blue accent and folded corner.
for size in sizes:
    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    page_margin = max(2, size // 16)
    page_color = (255, 255, 255, 255)
    accent_color = (27, 117, 219, 255)
    shadow_color = (220, 230, 245, 255)

    # paper shadow
    draw.rounded_rectangle(
        [page_margin + 2, page_margin + 2, size - page_margin + 2, size - page_margin + 2],
        radius=max(8, size // 12),
        fill=shadow_color,
    )
    # paper body
    draw.rounded_rectangle(
        [page_margin, page_margin, size - page_margin, size - page_margin],
        radius=max(8, size // 12),
        fill=page_color,
    )
    # folded corner
    draw.polygon(
        [
            (size - page_margin - size // 6, page_margin),
            (size - page_margin, page_margin),
            (size - page_margin, page_margin + size // 6),
        ],
        fill=accent_color,
    )
    # lower accent bar
    bar_height = max(8, size // 10)
    draw.rounded_rectangle(
        [page_margin + size // 8, size - page_margin - bar_height - size // 12, size - page_margin - size // 8, size - page_margin - size // 12],
        radius=max(4, size // 20),
        fill=accent_color,
    )
    # horizontal lines to mimic PDF page content
    for offset in range(3):
        y = page_margin + size // 8 + offset * (size // 14)
        draw.rounded_rectangle(
            [page_margin + size // 6, y, size - page_margin - size // 6, y + max(2, size // 60)],
            radius=2,
            fill=(210, 218, 232, 255),
        )

    file_name = f"icon_{size}x{size}.png"
    image.save(ICONSET_DIR / file_name)

# Store a 1024x1024 icon for fallback if needed
cover = ICONSET_DIR / "icon_1024x1024.png"
if not cover.exists():
    image = Image.new("RGBA", (1024, 1024), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([60, 60, 964, 964], radius=100, fill=(255, 255, 255, 255))
    draw.polygon([(754, 60), (964, 60), (964, 180)], fill=(27, 117, 219, 255))
    draw.rounded_rectangle([150, 760, 850, 850], radius=50, fill=(27, 117, 219, 255))
    for offset in range(3):
        y = 180 + offset * 120
        draw.rounded_rectangle([180, y, 840, y + 20], radius=10, fill=(210, 218, 232, 255))
    image.save(cover)

print(f"Created icon set at {ICONSET_DIR}")
