from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "qa-seo-pages"
OUT.mkdir(exist_ok=True)
PAGES = ["", "modelos/", "modelos/toyota-corolla/", "modelos/toyota-rav4/", "servicios/latoneria-pintura/", "servicios/ppf/", "blog/precio-ppf-completo-toyota-cartagena/"]
ROOT = Path(__file__).resolve().parents[1]
server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=ROOT))
Thread(target=server.serve_forever, daemon=True).start()
base_url = f"http://127.0.0.1:{server.server_port}/"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    for width, height in ((390, 844), (1366, 768), (1920, 900)):
        page = browser.new_page(viewport={"width": width, "height": height})
        for path in PAGES:
            page.goto(base_url + path, wait_until="networkidle")
            overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if overflow:
                raise AssertionError(f"Horizontal overflow: {path or '/'} at {width}px")
            name = path.strip("/").replace("/", "-") or "home"
            page.screenshot(path=OUT / f"{name}-{width}.png")
            print(f"OK {width}px {path or '/'}: {page.title()}")
        page.close()
    browser.close()
server.shutdown()
