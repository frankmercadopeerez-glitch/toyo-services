#!/usr/bin/env python3
"""Validación SEO y de integridad para el sitio estático de Toyo Services.

No requiere dependencias externas. Devuelve código 0 cuando todo pasa y 1
cuando encuentra errores, por lo que puede ejecutarse localmente o en CI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urljoin, urlparse


SITE_ORIGIN = "https://toyoservicescartagena.com"
SITE_HOST = "toyoservicescartagena.com"
EXPECTED_SITEMAP = f"{SITE_ORIGIN}/sitemap.xml"
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build"}
ASSET_LINK_RELS = {
    "apple-touch-icon",
    "icon",
    "manifest",
    "modulepreload",
    "preload",
    "stylesheet",
}
BROKEN_ENCODING_MARKERS = (
    "\ufffd",
    "Ã",
    "Â",
    "â€",
    "â€™",
    "â€œ",
    "â€",
    "â€“",
    "ï»¿",
)
BROKEN_WORD_RE = re.compile(
    r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]\?[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]"
)
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
POSITIVE_INTEGER_RE = re.compile(r"^[1-9]\d*$")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def type_includes(value: Any, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list):
        return expected in value
    return False


@dataclass(frozen=True)
class Issue:
    code: str
    source: str
    message: str


@dataclass
class Reference:
    value: str
    line: int
    kind: str


@dataclass
class ImageTag:
    src: str
    width: str
    height: str
    line: int


@dataclass
class Page:
    file: Path
    relative: str
    route: str
    titles: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    robots: list[str] = field(default_factory=list)
    h1s: list[str] = field(default_factory=list)
    canonicals: list[str] = field(default_factory=list)
    jsonld_raw: list[tuple[str, int]] = field(default_factory=list)
    jsonld: list[Any] = field(default_factory=list)
    links: list[Reference] = field(default_factory=list)
    assets: list[Reference] = field(default_factory=list)
    images: list[ImageTag] = field(default_factory=list)
    ids: set[str] = field(default_factory=set)
    visible_faqs: list[tuple[str, str]] = field(default_factory=list)
    text_for_encoding: list[str] = field(default_factory=list)

    @property
    def indexable(self) -> bool:
        return not any("noindex" in value.lower() for value in self.robots)


class SiteHTMLParser(HTMLParser):
    """Extrae señales SEO, enlaces, assets y FAQ sin dependencias externas."""

    def __init__(self, page: Page) -> None:
        super().__init__(convert_charrefs=True)
        self.page = page
        self._title_buffer: list[str] | None = None
        self._h1_buffer: list[str] | None = None
        self._jsonld_buffer: list[str] | None = None
        self._jsonld_line = 0
        self._skip_text_depth = 0
        self._detail: dict[str, Any] | None = None
        self._in_summary = False

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        line = self.getpos()[0]
        data = {key.lower(): value or "" for key, value in attrs}

        if data.get("id"):
            self.page.ids.add(data["id"])
        if tag == "a" and data.get("name"):
            self.page.ids.add(data["name"])

        if tag == "title":
            self._title_buffer = []
        elif tag == "h1":
            self._h1_buffer = []

        if tag in {"script", "style", "noscript"}:
            self._skip_text_depth += 1

        if tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self._jsonld_buffer = []
            self._jsonld_line = line

        if tag == "meta":
            name = data.get("name", "").lower()
            prop = data.get("property", "").lower()
            content = data.get("content", "")
            if name == "description":
                self.page.descriptions.append(content)
            elif name == "robots":
                self.page.robots.append(content)
            if name in {"description", "twitter:title", "twitter:description"} or prop in {
                "og:title",
                "og:description",
            }:
                self.page.text_for_encoding.append(content)
            if name == "twitter:image" or prop == "og:image":
                self.page.assets.append(Reference(content, line, f"meta {name or prop}"))

        if tag == "link":
            rels = set(data.get("rel", "").lower().split())
            href = data.get("href", "")
            if "canonical" in rels:
                self.page.canonicals.append(href)
            elif href and rels.intersection(ASSET_LINK_RELS):
                self.page.assets.append(Reference(href, line, "link"))

        if tag in {"a", "area"} and data.get("href"):
            self.page.links.append(Reference(data["href"], line, tag))

        direct_assets = {
            "audio": "src",
            "embed": "src",
            "iframe": "src",
            "img": "src",
            "object": "data",
            "script": "src",
            "source": "src",
            "track": "src",
            "video": "src",
        }
        attr = direct_assets.get(tag)
        if attr and data.get(attr):
            self.page.assets.append(Reference(data[attr], line, f"{tag}[{attr}]"))

        if tag in {"img", "source"} and data.get("srcset"):
            for candidate in data["srcset"].split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.page.assets.append(Reference(url, line, f"{tag}[srcset]"))

        if tag == "img":
            self.page.images.append(
                ImageTag(
                    src=data.get("src", ""),
                    width=data.get("width", ""),
                    height=data.get("height", ""),
                    line=line,
                )
            )

        for match in CSS_URL_RE.finditer(data.get("style", "")):
            self.page.assets.append(Reference(match.group(2), line, "style[url]"))

        for key in ("alt", "aria-label", "title"):
            if data.get(key):
                self.page.text_for_encoding.append(data[key])

        if tag == "details":
            self._detail = {"question": [], "answer": []}
        elif tag == "summary" and self._detail is not None:
            self._in_summary = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._title_buffer is not None:
            self.page.titles.append(clean_text("".join(self._title_buffer)))
            self._title_buffer = None
        elif tag == "h1" and self._h1_buffer is not None:
            self.page.h1s.append(clean_text("".join(self._h1_buffer)))
            self._h1_buffer = None
        elif tag == "script" and self._jsonld_buffer is not None:
            self.page.jsonld_raw.append(("".join(self._jsonld_buffer).strip(), self._jsonld_line))
            self._jsonld_buffer = None

        if tag in {"script", "style", "noscript"} and self._skip_text_depth:
            self._skip_text_depth -= 1

        if tag == "summary":
            self._in_summary = False
        elif tag == "details" and self._detail is not None:
            self.page.visible_faqs.append(
                (
                    clean_text("".join(self._detail["question"])),
                    clean_text("".join(self._detail["answer"])),
                )
            )
            self._detail = None

    def handle_data(self, data: str) -> None:
        if self._title_buffer is not None:
            self._title_buffer.append(data)
        if self._h1_buffer is not None:
            self._h1_buffer.append(data)
        if self._jsonld_buffer is not None:
            self._jsonld_buffer.append(data)

        if self._detail is not None:
            key = "question" if self._in_summary else "answer"
            self._detail[key].append(data)

        if not self._skip_text_depth:
            self.page.text_for_encoding.append(data)


def route_from_file(root: Path, file: Path) -> str:
    relative = file.relative_to(root).as_posix()
    if file.name.lower() == "index.html":
        parent = file.parent.relative_to(root).as_posix()
        return "/" if parent == "." else f"/{parent.strip('/')}/"
    return f"/{relative}"


def public_html_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for file in root.rglob("*.html"):
        relative_parts = file.relative_to(root).parts
        if any(part in SKIP_DIRS or part.startswith(".") for part in relative_parts):
            continue
        files.append(file)
    return sorted(files)


def parse_page(root: Path, file: Path, issues: list[Issue]) -> Page | None:
    relative = file.relative_to(root).as_posix()
    try:
        raw = file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        issues.append(Issue("ENCODING_UTF8", relative, str(exc)))
        return None

    page = Page(file=file, relative=relative, route=route_from_file(root, file))
    parser = SiteHTMLParser(page)
    try:
        parser.feed(raw)
        parser.close()
    except Exception as exc:  # HTMLParser es tolerante; esto captura fallos reales.
        issues.append(Issue("HTML_PARSE", relative, str(exc)))
        return page

    if raw.startswith("\ufeff"):
        issues.append(Issue("ENCODING_BOM", relative, "El HTML comienza con BOM UTF-8."))

    for match in re.finditer(r"<img\b[^>]*\s/\s+(?=(?:width|height)=)", raw, flags=re.IGNORECASE):
        line = raw.count("\n", 0, match.start()) + 1
        issues.append(
            Issue(
                "HTML_IMG_CLOSING",
                relative,
                f"Línea {line}: el cierre de <img> aparece antes de width/height.",
            )
        )

    encoding_text = " ".join(page.text_for_encoding)
    markers = sorted({marker for marker in BROKEN_ENCODING_MARKERS if marker in encoding_text})
    if markers:
        issues.append(
            Issue("ENCODING_BROKEN", relative, f"Secuencias sospechosas: {', '.join(repr(x) for x in markers)}")
        )
    if BROKEN_WORD_RE.search(encoding_text):
        issues.append(Issue("ENCODING_QUESTION_MARK", relative, "Hay un signo ? dentro de una palabra visible."))

    for raw_json, line in page.jsonld_raw:
        if not raw_json:
            issues.append(Issue("JSONLD_EMPTY", relative, f"JSON-LD vacío en línea {line}."))
            continue
        try:
            page.jsonld.append(json.loads(raw_json))
        except json.JSONDecodeError as exc:
            issues.append(
                Issue("JSONLD_INVALID", relative, f"Línea {line}: {exc.msg} (posición {exc.pos}).")
            )
    return page


def walk_json(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_json(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_json(value)


def schema_faqs(page: Page) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for document in page.jsonld:
        for node in walk_json(document):
            if not type_includes(node.get("@type"), "FAQPage"):
                continue
            entities = node.get("mainEntity", [])
            if isinstance(entities, dict):
                entities = [entities]
            if not isinstance(entities, list):
                continue
            for entity in entities:
                if not isinstance(entity, dict):
                    continue
                answer = entity.get("acceptedAnswer", {})
                if isinstance(answer, list):
                    answer = answer[0] if answer else {}
                result.append(
                    (
                        clean_text(str(entity.get("name", ""))),
                        clean_text(str(answer.get("text", ""))) if isinstance(answer, dict) else "",
                    )
                )
    return result


def validate_page_seo(page: Page, issues: list[Issue]) -> None:
    if page.indexable:
        required = (
            ("TITLE_COUNT", "title", page.titles),
            ("META_DESCRIPTION_COUNT", "meta description", page.descriptions),
            ("H1_COUNT", "H1", page.h1s),
            ("CANONICAL_COUNT", "canonical", page.canonicals),
        )
        for code, label, values in required:
            if len(values) != 1:
                issues.append(
                    Issue(code, page.relative, f"Debe existir exactamente un {label}; encontrados: {len(values)}.")
                )

        if len(page.canonicals) == 1:
            canonical = urlparse(page.canonicals[0])
            if canonical.scheme != "https" or canonical.netloc != SITE_HOST:
                issues.append(
                    Issue("CANONICAL_DOMAIN", page.relative, f"Canonical fuera de {SITE_ORIGIN}: {page.canonicals[0]}")
                )
            if canonical.query or canonical.fragment:
                issues.append(Issue("CANONICAL_CLEAN", page.relative, "El canonical contiene query o fragmento."))
            if unquote(canonical.path or "/") != page.route:
                issues.append(
                    Issue(
                        "CANONICAL_ROUTE",
                        page.relative,
                        f"Canonical {canonical.path or '/'} no coincide con la ruta {page.route}.",
                    )
                )

    expected_faqs = schema_faqs(page)
    if expected_faqs and expected_faqs != page.visible_faqs:
        issues.append(
            Issue(
                "FAQ_MISMATCH",
                page.relative,
                f"FAQ visible ({len(page.visible_faqs)}) no coincide exactamente con schema ({len(expected_faqs)}).",
            )
        )


def internal_target(reference: str, source_route: str) -> tuple[str, str] | None:
    value = reference.strip()
    if not value or value.startswith(("data:", "mailto:", "tel:", "javascript:")):
        return None
    absolute = urlparse(urljoin(f"{SITE_ORIGIN}{source_route}", value))
    if absolute.scheme not in {"http", "https"} or absolute.netloc != SITE_HOST:
        return None
    return unquote(absolute.path or "/"), unquote(absolute.fragment)


def file_for_url_path(root: Path, path: str) -> Path:
    path = path.split("?", 1)[0].split("#", 1)[0]
    candidate = root / path.lstrip("/")
    if path.endswith("/"):
        return candidate / "index.html"
    if candidate.is_dir() or not candidate.suffix:
        return candidate / "index.html"
    return candidate


def validate_whatsapp(page: Page, issues: list[Issue]) -> None:
    for ref in page.links:
        parsed = urlparse(ref.value)
        host = parsed.netloc.lower().split(":", 1)[0]
        if host not in {"wa.me", "www.wa.me"}:
            continue
        number = parsed.path.strip("/")
        if not re.fullmatch(r"\d{8,15}", number):
            issues.append(
                Issue(
                    "WHATSAPP_NUMBER",
                    page.relative,
                    f"Línea {ref.line}: URL wa.me sin número válido: {ref.value}",
                )
            )


def validate_links_and_assets(root: Path, pages: list[Page], issues: list[Issue]) -> None:
    route_map = {page.route: page for page in pages}
    seen: set[tuple[str, str, str, int]] = set()

    for page in pages:
        validate_whatsapp(page, issues)

        for ref in page.links:
            target = internal_target(ref.value, page.route)
            if target is None:
                continue
            path, fragment = target
            key = (page.relative, "link", ref.value, ref.line)
            if key in seen:
                continue
            seen.add(key)
            target_file = file_for_url_path(root, path)
            if not target_file.exists():
                issues.append(
                    Issue("LINK_BROKEN", page.relative, f"Línea {ref.line}: no existe {ref.value}")
                )
                continue
            if fragment:
                target_page = route_map.get(path)
                if target_page is None and target_file.suffix.lower() == ".html":
                    target_page = next((item for item in pages if item.file == target_file), None)
                if target_page is not None and fragment not in target_page.ids:
                    issues.append(
                        Issue(
                            "LINK_FRAGMENT",
                            page.relative,
                            f"Línea {ref.line}: #{fragment} no existe en {path}",
                        )
                    )

        for ref in page.assets:
            target = internal_target(ref.value, page.route)
            if target is None:
                continue
            path, _ = target
            key = (page.relative, "asset", ref.value, ref.line)
            if key in seen:
                continue
            seen.add(key)
            if not file_for_url_path(root, path).exists():
                issues.append(
                    Issue(
                        "ASSET_MISSING",
                        page.relative,
                        f"Línea {ref.line}: no existe {ref.kind} {ref.value}",
                    )
                )

        for image in page.images:
            if internal_target(image.src, page.route) is None:
                continue
            if not POSITIVE_INTEGER_RE.fullmatch(image.width) or not POSITIVE_INTEGER_RE.fullmatch(image.height):
                issues.append(
                    Issue(
                        "IMAGE_DIMENSIONS",
                        page.relative,
                        f"Línea {image.line}: imagen local sin width/height numéricos positivos: {image.src}",
                    )
                )

        for document in page.jsonld:
            for node in walk_json(document):
                for key in ("contentUrl", "image", "logo", "thumbnailUrl"):
                    value = node.get(key)
                    values = value if isinstance(value, list) else [value]
                    for asset in values:
                        if isinstance(asset, dict):
                            asset = asset.get("url") or asset.get("contentUrl")
                        if not isinstance(asset, str):
                            continue
                        target = internal_target(asset, page.route)
                        if target is None:
                            continue
                        path, _ = target
                        if not file_for_url_path(root, path).exists():
                            issues.append(
                                Issue("JSONLD_ASSET", page.relative, f"JSON-LD referencia un asset inexistente: {asset}")
                            )


def validate_css_assets(root: Path, issues: list[Issue]) -> None:
    for css_file in sorted(root.rglob("*.css")):
        if any(part in SKIP_DIRS or part.startswith(".") for part in css_file.relative_to(root).parts):
            continue
        relative = css_file.relative_to(root).as_posix()
        try:
            raw = css_file.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            issues.append(Issue("ENCODING_UTF8", relative, str(exc)))
            continue
        source_url = f"{SITE_ORIGIN}/{relative}"
        for line_number, line in enumerate(raw.splitlines(), 1):
            for match in CSS_URL_RE.finditer(line):
                value = match.group(2).strip()
                if not value or value.startswith("data:"):
                    continue
                parsed = urlparse(urljoin(source_url, value))
                if parsed.netloc != SITE_HOST:
                    continue
                path = unquote(parsed.path or "/")
                if not file_for_url_path(root, path).exists():
                    issues.append(
                        Issue("CSS_ASSET", relative, f"Línea {line_number}: no existe {value}")
                    )


def load_sitemap(root: Path, issues: list[Issue]) -> set[str]:
    file = root / "sitemap.xml"
    if not file.exists():
        issues.append(Issue("SITEMAP_MISSING", "sitemap.xml", "No existe sitemap.xml."))
        return set()
    try:
        tree = ET.parse(file)
    except (ET.ParseError, UnicodeDecodeError) as exc:
        issues.append(Issue("SITEMAP_PARSE", "sitemap.xml", str(exc)))
        return set()

    routes: set[str] = set()
    locs = [clean_text(node.text or "") for node in tree.findall(".//{*}loc")]
    for loc in locs:
        parsed = urlparse(loc)
        if parsed.scheme != "https" or parsed.netloc != SITE_HOST:
            issues.append(Issue("SITEMAP_DOMAIN", "sitemap.xml", f"URL fuera del dominio: {loc}"))
            continue
        if parsed.query or parsed.fragment:
            issues.append(Issue("SITEMAP_CLEAN", "sitemap.xml", f"URL con query o fragmento: {loc}"))
        route = unquote(parsed.path or "/")
        if route in routes:
            issues.append(Issue("SITEMAP_DUPLICATE", "sitemap.xml", f"URL duplicada: {loc}"))
        routes.add(route)
    return routes


def validate_robots(root: Path, issues: list[Issue]) -> None:
    file = root / "robots.txt"
    if not file.exists():
        issues.append(Issue("ROBOTS_MISSING", "robots.txt", "No existe robots.txt."))
        return
    try:
        raw = file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        issues.append(Issue("ENCODING_UTF8", "robots.txt", str(exc)))
        return
    sitemap_lines = re.findall(r"^\s*Sitemap\s*:\s*(\S+)\s*$", raw, re.IGNORECASE | re.MULTILINE)
    if EXPECTED_SITEMAP not in sitemap_lines:
        issues.append(
            Issue(
                "ROBOTS_SITEMAP",
                "robots.txt",
                f"Debe apuntar exactamente a {EXPECTED_SITEMAP}; encontrados: {sitemap_lines or 'ninguno'}",
            )
        )


def validate_sitemap_parity(pages: list[Page], sitemap_routes: set[str], issues: list[Issue]) -> None:
    indexable_routes = {page.route for page in pages if page.indexable}
    for route in sorted(indexable_routes - sitemap_routes):
        issues.append(Issue("SITEMAP_MISSING_ROUTE", "sitemap.xml", f"Falta ruta indexable: {route}"))
    for route in sorted(sitemap_routes - indexable_routes):
        issues.append(Issue("SITEMAP_EXTRA_ROUTE", "sitemap.xml", f"Sobra ruta no indexable o inexistente: {route}"))


def run(root: Path) -> tuple[list[Page], list[Issue], set[str]]:
    issues: list[Issue] = []
    pages = [page for file in public_html_files(root) if (page := parse_page(root, file, issues)) is not None]
    for page in pages:
        validate_page_seo(page, issues)
    validate_links_and_assets(root, pages, issues)
    validate_css_assets(root, issues)
    sitemap_routes = load_sitemap(root, issues)
    validate_robots(root, issues)
    validate_sitemap_parity(pages, sitemap_routes, issues)
    return pages, issues, sitemap_routes


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida SEO, enlaces, assets, schema, sitemap y robots del sitio.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Raíz del sitio (por defecto, el repositorio que contiene este script).",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    pages, issues, sitemap_routes = run(root)
    indexable = sum(page.indexable for page in pages)

    print("Toyo Services - validación SEO global")
    print(f"Raíz: {root}")
    print(f"HTML: {len(pages)} | Indexables: {indexable} | Sitemap: {len(sitemap_routes)}")

    if issues:
        grouped: dict[str, list[Issue]] = {}
        for issue in sorted(issues, key=lambda item: (item.code, item.source, item.message)):
            grouped.setdefault(issue.code, []).append(issue)
        print(f"Resultado: ERROR ({len(issues)} hallazgos en {len(grouped)} categorías)")
        for code, entries in grouped.items():
            print(f"\n[{code}] {len(entries)}")
            for issue in entries:
                print(f"- {issue.source}: {issue.message}")
        return 1

    print("Resultado: OK (sin hallazgos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
