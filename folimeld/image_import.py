"""Image inventory and isolated PDF conversion (no Qt dependencies)."""
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image, ImageOps


EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


@dataclass(frozen=True)
class ImageEntry:
    path: Path
    created: float | None
    modified: float | None


def inventory(folder):
    entries = []
    for path in Path(folder).iterdir():
        if path.suffix.lower() not in EXTENSIONS or not path.is_file():
            continue
        try:
            stat = path.stat()
            created = getattr(stat, 'st_birthtime', None)
            if created is None and sys.platform == 'win32':
                created = stat.st_ctime
            modified = stat.st_mtime
        except OSError:
            created = modified = None
        entries.append(ImageEntry(path, created, modified))
    return entries


def name_key(entry):
    return (tuple((0, int(part)) if part.isdigit() else (1, part.casefold())
                  for part in re.split(r'(\d+)', entry.path.name)), entry.path.name)


def sort_entries(entries, field='name', descending=False):
    ordered = sorted(entries, key=name_key)
    if field == 'name':
        return list(reversed(ordered)) if descending else ordered
    known = [entry for entry in ordered if getattr(entry, field) is not None]
    missing = [entry for entry in ordered if getattr(entry, field) is None]
    return sorted(known, key=lambda entry: getattr(entry, field), reverse=descending) + missing


def convert_images(paths, destination, page_size='image', progress=None):
    """Build a PDF one frame at a time; callers own temporary-file cleanup."""
    with fitz.open() as document:
        for index, path in enumerate(paths):
            try:
                with Image.open(path) as source:
                    if source.format == 'WEBP' and getattr(source, 'is_animated', False):
                        raise ValueError('Animated WebP is not supported')
                    frames = getattr(source, 'n_frames', 1) if source.format == 'TIFF' else 1
                    for frame in range(frames):
                        source.seek(frame)
                        dpi = source.info.get('dpi', (300, 300))
                        try:
                            dx, dy = (float(value) for value in dpi)
                            if not (36 <= dx <= 1200 and 36 <= dy <= 1200):
                                dx = dy = 300
                        except (TypeError, ValueError):
                            dx = dy = 300
                        image = ImageOps.exif_transpose(source)
                        if source.getexif().get(274, 1) in (5, 6, 7, 8):
                            dx, dy = dy, dx
                        rgba = image.convert('RGBA')
                        rgb = Image.new('RGB', rgba.size, 'white')
                        rgb.paste(rgba, mask=rgba.getchannel('A'))
                        width, height = rgb.width * 72 / dx, rgb.height * 72 / dy
                        if page_size == 'a4':
                            width, height = fitz.paper_size('a4')
                        page = document.new_page(width=width, height=height)
                        with io.BytesIO() as buffer:
                            rgb.save(buffer, format='PNG')
                            page.insert_image(page.rect, stream=buffer.getvalue(), keep_proportion=True)
                if progress:
                    progress(index + 1)
            except Exception as exc:
                raise ValueError(f'{Path(path).name}: {exc}') from exc
        if not document.page_count:
            raise ValueError('No images selected')
        document.save(str(destination), deflate=True)


def conversion_worker(paths, destination, page_size, connection):
    try:
        convert_images(paths, destination, page_size, lambda count: connection.send(('progress', count)))
        connection.send(('done', None))
    except Exception as exc:
        connection.send(('error', str(exc)))
    finally:
        connection.close()
