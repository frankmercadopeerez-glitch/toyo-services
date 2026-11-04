"""Regression checks for the approved logo and site typography."""
import re
import unittest
from pathlib import Path
from site_ui import apply_branding

ROOT=Path(__file__).resolve().parents[1]
PUBLIC={'blog','servicios','modelos','nosotros','legal','privacidad','metodologia','preguntas-frecuentes','creditos-imagenes','cotizar','repuestos'}

def pages():
    yield from ROOT.glob('*.html')
    for folder in PUBLIC:
        yield from (ROOT/folder).rglob('*.html')

class Branding(unittest.TestCase):
    def test_multiline_brand_preserves_navigation_and_footer(self):
        before = '<a class="brand" href="/"><span>TOYO SERVICES</span></a\n >'
        following = '<button class="menu">Menú</button><div class="nav-links"><a href="/servicios/">Servicios</a></div><p>Contacto y descripción</p>'
        result = apply_branding(before + following)
        self.assertTrue(result.endswith(following))
        self.assertEqual(result.count('<a '), 2)

    def test_all_pages_share_approved_identity(self):
        for file in pages():
            with self.subTest(file=str(file.relative_to(ROOT))):
                text=file.read_text(encoding='utf-8')
                brands=re.findall(r'<a\b[^>]*class="brand"[^>]*>.*?</a>',text,re.S)
                for brand in brands:
                    self.assertIn('class="brand-wordmark"',brand)
                    self.assertIn('alt="Toyo Services"',brand)
                    self.assertNotIn('<span>',brand)
                    self.assertIn('toyo-services-wordmark.svg?v=20261104',brand)
                self.assertIn('styles.min.css?v=27',text)
                self.assertEqual(text,apply_branding(text))
                for style in ['normal','italic']:
                    self.assertEqual(text.count(f'href="/assets/fonts/exo-2-latin-{style}.woff2"'),1)

    def test_fonts_are_local_and_valid(self):
        css=(ROOT/'assets/css/styles.css').read_text(encoding='utf-8')
        self.assertNotIn('Bahnschrift',css)
        self.assertIn('--font-body: "Exo 2"',css)
        for filename in re.findall(r'url\("(/assets/fonts/[^\"]+)"\)',css):
            data=(ROOT/filename.lstrip('/')).read_bytes()
            self.assertEqual(data[:4],b'wOF2')
        self.assertIn('SIL OPEN FONT LICENSE',(ROOT/'assets/fonts/Exo-2-OFL.txt').read_text())

    def test_logo_remains_true_vector(self):
        for name in ['toyo-services-logo.svg','toyo-services-wordmark.svg']:
            svg=(ROOT/'assets/images'/name).read_text()
            self.assertNotRegex(svg,r'<(?:image|text)\b')
            self.assertIn('<path',svg)
        svg=(ROOT/'assets/images/toyo-services-logo.svg').read_text()
        self.assertIn('rx="43"',svg)
        self.assertIn('ry="27"',svg)

if __name__=='__main__':unittest.main()
