#!/usr/bin/env python3
"""Generate and validate Toyo Services' XML sitemap from indexable HTML pages."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


BASE_URL = "https://toyoservicescartagena.com"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = PROJECT_ROOT / "sitemap.xml"


class PageMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.robots = ""
        self.canonical = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.robots = values.get("content", "").lower()
        if tag.lower() == "link":
            rel_tokens = values.get("rel", "").lower().split()
            if "canonical" in rel_tokens:
                self.canonical = values.get("href", "")


def route_for(page: Path) -> str:
    relative = page.relative_to(PROJECT_ROOT)
    if relative == Path("index.html"):
        return "/"
    return f"/{relative.parent.as_posix()}/"


def discover_indexable_pages() -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for page in sorted(PROJECT_ROOT.rglob("index.html")):
        relative = page.relative_to(PROJECT_ROOT)
        if any(part.startswith(".") or part in {"output", "scripts", "tests", "node_modules"} for part in relative.parts):
            continue

        parser = PageMetadataParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if "noindex" in {token.strip() for token in parser.robots.split(",")}:
            continue

        route = route_for(page)
        expected_canonical = f"{BASE_URL}{route}"
        if parser.canonical != expected_canonical:
            raise ValueError(
                f"Canonical incorrecto en {relative.as_posix()}: "
                f"esperado {expected_canonical!r}, encontrado {parser.canonical!r}"
            )
        pages[expected_canonical] = page
    return pages


def existing_lastmods() -> dict[str, str]:
    if not SITEMAP_PATH.exists():
        return {}
    root = ET.parse(SITEMAP_PATH).getroot()
    namespace = {"sm": SITEMAP_NS}
    values: dict[str, str] = {}
    for entry in root.findall("sm:url", namespace):
        loc = entry.findtext("sm:loc", default="", namespaces=namespace)
        lastmod = entry.findtext("sm:lastmod", default="", namespaces=namespace)
        if loc and lastmod:
            values[loc] = lastmod
    return values


def changed_files() -> set[str]:
    commands = [
        ["git", "diff", "--name-only", "HEAD", "--"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    changed: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        changed.update(line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip())
    return changed


def priority_for(route: str) -> str:
    if route == "/":
        return "1.0"
    if route in {"/blog/", "/servicios/", "/modelos/"}:
        return "0.9"
    if route in {"/legal/", "/privacidad/"}:
        return "0.5"
    if route in {"/nosotros/", "/preguntas-frecuentes/"}:
        return "0.7"
    return "0.8"


def build_xml(date: str) -> tuple[str, set[str]]:
    pages = discover_indexable_pages()
    previous_dates = existing_lastmods()
    modified = changed_files()

    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for loc, page in sorted(pages.items()):
        route = route_for(page)
        relative = page.relative_to(PROJECT_ROOT).as_posix()
        lastmod = date if relative in modified or loc not in previous_dates else previous_dates[loc]

        entry = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(entry, f"{{{SITEMAP_NS}}}loc").text = loc
        ET.SubElement(entry, f"{{{SITEMAP_NS}}}lastmod").text = lastmod
        ET.SubElement(entry, f"{{{SITEMAP_NS}}}priority").text = priority_for(route)

    ET.indent(urlset, space="  ")
    xml = ET.tostring(urlset, encoding="unicode", xml_declaration=True)
    return f"{xml}\n", set(pages)


def sitemap_urls(xml: str) -> set[str]:
    root = ET.fromstring(xml)
    namespace = {"sm": SITEMAP_NS}
    return {
        entry.findtext("sm:loc", default="", namespaces=namespace)
        for entry in root.findall("sm:url", namespace)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Fecha YYYY-MM-DD para páginas nuevas o modificadas",
    )
    parser.add_argument("--check", action="store_true", help="Validar sin modificar sitemap.xml")
    args = parser.parse_args()

    try:
        dt.date.fromisoformat(args.date)
        expected_xml, indexable = build_xml(args.date)
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.check:
        current_xml = SITEMAP_PATH.read_text(encoding="utf-8") if SITEMAP_PATH.exists() else ""
        if current_xml != expected_xml:
            print("sitemap.xml no coincide con el estado indexable actual", file=sys.stderr)
            return 1
    else:
        SITEMAP_PATH.write_text(expected_xml, encoding="utf-8", newline="\n")

    actual = sitemap_urls(expected_xml if not args.check else SITEMAP_PATH.read_text(encoding="utf-8"))
    if actual != indexable:
        print(
            f"Error de correspondencia: indexables={len(indexable)}, sitemap={len(actual)}",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {len(indexable)} páginas indexables y {len(actual)} URLs en sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
