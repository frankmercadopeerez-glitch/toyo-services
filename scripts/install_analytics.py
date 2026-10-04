from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ID = "G-H76912PXD3"
MARKER = "<!-- Google tag: Toyo Services -->"
TAG = f'''{MARKER}
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{MEASUREMENT_ID}');
</script>'''


def install(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    html = re.sub(r"/assets/js/main\.js\?v=\d+", "/assets/js/main.js?v=23", html)
    if MARKER in html:
        if html != original:
            path.write_text(html, encoding="utf-8")
            return True
        return False
    if "<head>" not in html:
        raise ValueError(f"Missing <head> in {path.relative_to(ROOT)}")
    path.write_text(html.replace("<head>", f"<head>\n{TAG}", 1), encoding="utf-8")
    return True


if __name__ == "__main__":
    excluded = {".git", "tmp", "output", "qa-seo-pages"}
    pages = [path for path in ROOT.rglob("*.html") if not excluded.intersection(path.relative_to(ROOT).parts)]
    changed = sum(install(path) for path in pages)
    print(f"Google Analytics {MEASUREMENT_ID}: {changed} updated, {len(pages) - changed} already configured")
