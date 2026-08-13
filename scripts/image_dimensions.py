"""Read raster image dimensions with the Python standard library."""

from pathlib import Path
import struct
import re


def image_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()

    if data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])

    if data[:2] == b"\xff\xd8":
        position = 2
        while position + 9 < len(data):
            if data[position] != 0xFF:
                position += 1
                continue
            marker = data[position + 1]
            position += 2
            if marker in {0xD8, 0xD9}:
                continue
            length = struct.unpack(">H", data[position : position + 2])[0]
            if marker in {
                0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
            }:
                height, width = struct.unpack(">HH", data[position + 3 : position + 7])
                return width, height
            position += length

    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X":
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return width, height
        if chunk == b"VP8L" and data[20] == 0x2F:
            b0, b1, b2, b3 = data[21:25]
            width = 1 + (b0 | ((b1 & 0x3F) << 8))
            height = 1 + ((b1 >> 6) | (b2 << 2) | ((b3 & 0x0F) << 10))
            return width, height
        if chunk == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
            width, height = struct.unpack("<HH", data[26:30])
            return width & 0x3FFF, height & 0x3FFF

    raise ValueError(f"Unsupported or malformed image: {path}")


IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
SRC = re.compile(r"\bsrc=[\"']([^\"']+)", re.IGNORECASE)
WIDTH = re.compile(r"\bwidth=[\"']\d+[\"']", re.IGNORECASE)
HEIGHT = re.compile(r"\bheight=[\"']\d+[\"']", re.IGNORECASE)


def sync_html_image_dimensions(markup: str, root: Path) -> str:
    """Return HTML with actual width and height for every local raster image."""

    def update_tag(match: re.Match[str]) -> str:
        tag = match.group(0)
        source_match = SRC.search(tag)
        if not source_match:
            return tag
        source = source_match.group(1).split("?", 1)[0]
        if not source.startswith("/") or source.lower().endswith(".svg"):
            return tag
        path = root / source.lstrip("/")
        if not path.is_file():
            return tag
        width, height = image_dimensions(path)
        closing = " />" if re.search(r"/\s*>$", tag) else ">"
        tag = re.sub(r"\s*/?\s*>$", "", tag)
        tag = re.sub(r"\s*/\s*(?=width=[\"'])", " ", tag)
        if WIDTH.search(tag):
            tag = WIDTH.sub(f'width="{width}"', tag, count=1)
        else:
            tag = tag.rstrip() + f' width="{width}"'
        if HEIGHT.search(tag):
            tag = HEIGHT.sub(f'height="{height}"', tag, count=1)
        else:
            tag = tag.rstrip() + f' height="{height}"'
        return tag + closing

    return IMG_TAG.sub(update_tag, markup)
