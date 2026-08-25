#!/usr/bin/env python3
"""Attach responsive image candidates to hand-authored site pages."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images"
IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
WEBP_SRC = re.compile(r'src="/assets/images/([^"?]+\.webp)"', re.IGNORECASE)
RESPONSIVE_ATTRS = re.compile(r'\s+srcset="[^"]*"\s+sizes="[^"]*"', re.IGNORECASE)
HAND_AUTHORED = {
    "index.html",
    "creditos-imagenes/index.html",
    "modelos/index.html",
    "modelos/toyota-fortuner/index.html",
    "modelos/toyota-hilux/index.html",
    "modelos/toyota-prado/index.html",
    "servicios/index.html",
}


def sizes_for(relative: str, filename: str) -> str:
    if relative == "index.html":
        if filename == "toyo-hero-toyota.webp":
            return "100vw"
        if filename == "feature-craftsmanship-toyota.webp":
            return "(max-width: 850px) calc(100vw - 40px), 50vw"
        return "(max-width: 700px) calc(100vw - 40px), (max-width: 1100px) 46vw, 360px"
    if relative == "servicios/index.html":
        return "(max-width: 850px) calc(100vw - 40px), 260px"
    if relative == "modelos/index.html":
        return "(max-width: 700px) calc(100vw - 40px), 360px"
    if relative.startswith("modelos/toyota-"):
        return "(max-width: 720px) calc(100vw - 40px), 920px"
    if relative == "creditos-imagenes/index.html":
        return "220px"
    return "(max-width: 720px) calc(100vw - 40px), 920px"


def add_candidates(tag: str, relative: str) -> str:
    tag = RESPONSIVE_ATTRS.sub("", tag)
    match = WEBP_SRC.search(tag)
    if not match:
        return tag
    filename = match.group(1)
    source = IMAGES / filename
    if not source.exists():
        return tag
    with Image.open(source) as image:
        original_width = image.width
    stem = source.stem
    candidates = [
        f"/assets/images/{stem}-{width}w.webp {width}w"
        for width in (400, 640, 960, 1120, 1440)
        if width < original_width and source.with_name(f"{stem}-{width}w.webp").exists()
    ]
    if not candidates:
        return tag
    candidates.append(f"/assets/images/{filename} {original_width}w")
    attrs = f' srcset="{", ".join(candidates)}" sizes="{sizes_for(relative, filename)}"'
    return tag[: match.end()] + attrs + tag[match.end() :]


def main() -> int:
    changed = 0
    for page in ROOT.rglob("index.html"):
        if any(part.startswith(".") for part in page.relative_to(ROOT).parts):
            continue
        relative = page.relative_to(ROOT).as_posix()
        if relative not in HAND_AUTHORED:
            continue
        original = page.read_text(encoding="utf-8")
        updated = IMG_TAG.sub(lambda match: add_candidates(match.group(0), relative), original)
        if updated != original:
            page.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
    print(f"Updated responsive markup in {changed} hand-authored pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
