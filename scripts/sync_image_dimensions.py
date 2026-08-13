"""Synchronize local raster <img> dimensions to prevent layout shifts."""

from pathlib import Path

from image_dimensions import sync_html_image_dimensions


ROOT = Path(__file__).resolve().parents[1]

changed = 0
for page in sorted(ROOT.rglob("*.html")):
    if ".git" in page.parts:
        continue
    original = page.read_text(encoding="utf-8")
    updated = sync_html_image_dimensions(original, ROOT)
    if updated != original:
        page.write_text(updated, encoding="utf-8")
        changed += 1

print(f"Synchronized image dimensions in {changed} HTML files")
