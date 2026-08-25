#!/usr/bin/env python3
"""Create responsive WebP variants for images used by the public site."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images"
WIDTHS = (400, 640, 960, 1120, 1440)
IMAGE_PATTERN = re.compile(r'/assets/images/([^"?]+\.webp)', re.IGNORECASE)


def referenced_images() -> set[str]:
    names: set[str] = set()
    for page in ROOT.rglob("index.html"):
        if any(part.startswith(".") for part in page.relative_to(ROOT).parts):
            continue
        names.update(IMAGE_PATTERN.findall(page.read_text(encoding="utf-8")))
    return names


def variant_path(source: Path, width: int) -> Path:
    return source.with_name(f"{source.stem}-{width}w.webp")


def main() -> int:
    generated = 0
    for name in sorted(referenced_images()):
        source = IMAGES / name
        if not source.exists() or re.search(r"-\d+w$", source.stem):
            continue
        with Image.open(source) as image:
            for width in WIDTHS:
                if image.width <= width:
                    continue
                height = round(image.height * width / image.width)
                resized = image.resize((width, height), Image.Resampling.LANCZOS)
                resized.save(
                    variant_path(source, width),
                    "WEBP",
                    quality=76,
                    method=6,
                    exact=True,
                )
                generated += 1
    print(f"Generated {generated} responsive image variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
