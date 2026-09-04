"""Build platform icon assets from the Folimeld chroma-key artwork."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT / "assets"
SOURCE = ASSET_DIR / "Folimeld-icon-source.png"
MASTER = ASSET_DIR / "Folimeld-icon-master.png"
ICONSET_DIR = ASSET_DIR / "Folimeld.iconset"
MSIX_ASSET_DIR = ROOT / "packaging" / "msix" / "Assets"
PNG_SIZES = (16, 32, 64, 128, 256, 512, 1024)


def remove_green_background(image: Image.Image) -> Image.Image:
    """Turn the generated green backdrop into alpha and suppress green spill."""
    source = image.convert("RGB")
    output = Image.new("RGBA", source.size)
    converted: list[tuple[int, int, int, int]] = []

    pixels = source.load()
    for y in range(source.height):
        for x in range(source.width):
            red, green, blue = pixels[x, y]
            green_excess = green - max(red, blue)
            alpha = round(255 * (1 - max(0, min(1, (green_excess - 35) / 100))))
            if alpha == 0:
                converted.append((0, 0, 0, 0))
                continue

            fraction = alpha / 255
            clean_red = min(255, round(red / fraction))
            clean_blue = min(255, round(blue / fraction))
            clean_green = min(255, max(0, round((green - (1 - fraction) * 255) / fraction)))
            converted.append((clean_red, clean_green, clean_blue, alpha))

    output.putdata(converted)
    return output


def build_icons() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Icon source not found: {SOURCE}")

    ICONSET_DIR.mkdir(parents=True, exist_ok=True)
    MSIX_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    master = remove_green_background(Image.open(SOURCE))
    master.save(MASTER, optimize=True)

    rendered: dict[int, Image.Image] = {}
    for size in PNG_SIZES:
        icon = master.resize((size, size), Image.Resampling.LANCZOS)
        rendered[size] = icon
        icon.save(ICONSET_DIR / f"icon_{size}x{size}.png", optimize=True)

    rendered[256].save(
        ASSET_DIR / "Folimeld.ico",
        format="ICO",
        sizes=[(size, size) for size in (16, 32, 48, 64, 128, 256)],
    )
    master.save(
        ASSET_DIR / "Folimeld.icns",
        format="ICNS",
        sizes=[(size, size) for size in PNG_SIZES],
    )
    for filename, size in {
        "StoreLogo.png": (50, 50),
        "Square44x44Logo.png": (44, 44),
        "Square71x71Logo.png": (71, 71),
        "Square150x150Logo.png": (150, 150),
        "Wide310x150Logo.png": (310, 150),
        "Square310x310Logo.png": (310, 310),
    }.items():
        contained = Image.new("RGBA", size, (0, 0, 0, 0))
        icon_size = min(size)
        icon = master.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        contained.alpha_composite(icon, ((size[0] - icon_size) // 2, 0))
        contained.save(MSIX_ASSET_DIR / filename, optimize=True)
    print(f"Created transparent icon assets from {SOURCE}")


if __name__ == "__main__":
    build_icons()
