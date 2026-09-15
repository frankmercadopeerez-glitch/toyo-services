"""Regression checks for public navigation, forms and publish boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_ui import enhance_page
from validate_site import public_html_files

ROOT = Path(__file__).resolve().parents[1]

class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.controls = []
        self.labels = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'label' and 'for' in attrs: self.labels.append(attrs['for'])
        if 'aria-controls' in attrs: self.controls.extend(attrs['aria-controls'].split())

class SiteUI(unittest.TestCase):
    def test_styles_use_defined_tokens(self):
        css = (ROOT/'assets/css/styles.css').read_text(encoding='utf-8')
        used = set(re.findall(r'var\((--[\w-]+)', css))
        defined = set(re.findall(r'(--[\w-]+)\s*:', css))
        self.assertFalse(used-defined, f'Undefined CSS properties: {used-defined}')

    def test_public_pages_have_unique_ids_and_valid_controls(self):
        for file in public_html_files(ROOT):
            with self.subTest(page=str(file.relative_to(ROOT))):
                dom = Markup(file.read_text(encoding='utf-8'))
                self.assertEqual(len(dom.ids), len(set(dom.ids)))
                for target in dom.controls + dom.labels:
                    self.assertIn(target, dom.ids)

    def test_generated_navigation_survives_repeat_runs(self):
        for path in ['servicios/repuestos/index.html', 'blog/costo-mantenimiento-toyota-cartagena/index.html']:
            text = (ROOT/path).read_text(encoding='utf-8')
            route = '/'+path.removesuffix('index.html')
            self.assertEqual(text, enhance_page(text, route))
            self.assertIn('href="#contenido"', text)
            self.assertEqual(text.count('class="nav-quote"'), 1)

    def test_artifacts_are_not_public_content(self):
        self.assertTrue(all('output' not in p.relative_to(ROOT).parts for p in public_html_files(ROOT)))
        self.assertIn('output/', (ROOT/'.vercelignore').read_text())
        self.assertIn('scripts/', (ROOT/'.vercelignore').read_text())

    def test_service_request_links_preserve_context(self):
        for file in (ROOT/'servicios').glob('*/index.html'):
            text = file.read_text(encoding='utf-8')
            self.assertIn('/cotizar/?servicio='+file.parent.name, text)

if __name__ == '__main__':
    unittest.main()
