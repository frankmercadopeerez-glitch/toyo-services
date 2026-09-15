"""Reapply shared components after generating content. No development artifacts."""
from pathlib import Path
import re
from site_ui import enhance_page, quote_form, service_finder

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = {'blog', 'servicios', 'modelos', 'nosotros', 'legal', 'privacidad', 'metodologia', 'preguntas-frecuentes', 'creditos-imagenes', 'cotizar'}

def main():
    home_path = ROOT/'index.html'
    home = home_path.read_text(encoding='utf-8')
    home = re.sub(r'<form class="contact-form".*?</form>', lambda _: quote_form(), home, count=1, flags=re.S)
    if 'class="service-finder"' not in home:
        home = home.replace('<section class="local-expertise"', service_finder()+'<section class="local-expertise"', 1)
    home = home.replace('Completa los datos básicos. Al enviar, abriremos WhatsApp con la', 'Completa los datos básicos y revisa el mensaje. Después podrás abrir WhatsApp con la')
    home_path.write_text(home, encoding='utf-8')
    header = re.search(r'<header class="site-header">.*?</header>', home, re.S)[0]
    footer = re.search(r'<footer class="footer">.*?</body>', home, re.S)[0].removesuffix('</body>')
    quote = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cotizar servicio o repuesto Toyota en Cartagena | Toyo Services</title><meta name="description" content="Prepara tu solicitud de mantenimiento, diagnóstico o repuestos Toyota en Cartagena. Comparte modelo, año y necesidad; revisa el mensaje y envíalo por WhatsApp."><meta name="robots" content="index,follow"><link rel="canonical" href="https://toyoservicescartagena.com/cotizar/"><meta property="og:title" content="Cotiza para tu Toyota | Toyo Services"><meta property="og:description" content="Una solicitud clara para tu mantenimiento, diagnóstico o repuesto Toyota en Cartagena."><meta property="og:type" content="website"><meta property="og:url" content="https://toyoservicescartagena.com/cotizar/"><meta property="og:image" content="https://toyoservicescartagena.com/assets/images/toyo-hero-toyota.webp"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/styles.min.css?v=25"></head><body>'''+header+'''<main id="contenido"><section class="contact-form-section quote-page"><div class="container"><nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / Cotizar</nav><div class="contact-form-layout"><div class="contact-form-intro"><span class="eyebrow">Hablemos de tu Toyota</span><h1>Una solicitud clara. Un mejor punto de partida.</h1><p>Cuéntanos qué necesitas. Revisarás tu mensaje antes de enviarlo a Toyo Services por WhatsApp.</p><ol class="quote-steps"><li><strong>Identifica tu Toyota</strong><span>Modelo, año y versión si los conoces.</span></li><li><strong>Describe tu necesidad</strong><span>Síntoma, mantenimiento o referencia del repuesto.</span></li><li><strong>Coordina el siguiente paso</strong><span>Confirmamos alcance, disponibilidad y recepción.</span></li></ol><p>La solicitud no reserva una cita ni confirma un precio. El diagnóstico y los trabajos se acuerdan según el caso.</p><p>¿Prefieres hablar directamente?<br><a href="tel:+573018638164">Llamar al +57 301 863 8164</a><br><a href="https://wa.me/573018638164" target="_blank" rel="noopener">Escribir por WhatsApp</a></p><p>Cuatro Vientos, junto a Primax, Cartagena.<br><a href="/#ubicacion">Cómo llegar al taller →</a></p></div><div><noscript><p>Para solicitar atención, <a href="https://wa.me/573018638164">escríbenos por WhatsApp</a> o llama al +57 301 863 8164.</p></noscript>'''+quote_form()+'''</div></div></div></section></main>'''+footer+'''</body></html>'''
    quote = quote.replace('href="#ubicacion"', 'href="/#ubicacion"')
    quote = quote.replace('<ol class="quote-steps">', '<p><a class="btn btn-primary" href="#contact-model">Completar mi solicitud ↓</a></p><ol class="quote-steps">')
    quote = quote.replace('<meta property="og:type"', '<meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Toyo Services"><meta name="theme-color" content="#080a0d"><meta name="twitter:card" content="summary_large_image"><meta property="og:type"', 1)
    (ROOT/'cotizar').mkdir(exist_ok=True)
    (ROOT/'cotizar/index.html').write_text(quote, encoding='utf-8')
    for file in ROOT.rglob('*.html'):
        rel = file.relative_to(ROOT)
        if len(rel.parts)>1 and rel.parts[0] not in PUBLIC_DIRS:
            continue
        route = '/' if str(rel)=='index.html' else '/'+rel.parent.as_posix()+'/'
        page = enhance_page(file.read_text(encoding='utf-8'), route)
        if rel.as_posix() == 'servicios/index.html' and 'data-service-search' not in page:
            finder = '''<div class="container service-search" data-service-search hidden><label for="service-search">Encuentra un servicio o describe el síntoma</label><div class="search-line"><input id="service-search" type="search" placeholder="Ej. aceite, repuestos, ruido, caja…" aria-controls="service-results" autocomplete="off"><button type="button" data-clear-services>Limpiar</button></div><p role="status" data-service-count></p><p data-service-empty hidden>Podemos orientarte aunque no conozcas el nombre del servicio. <a href="/cotizar/?servicio=otro">Cuéntanos qué ocurre →</a></p></div>'''
            page = page.replace('<article class="service-row"', '<div id="service-results"></div><article class="service-row"', 1)
            page = page.replace('</header>\n      <section>', '</header>'+finder+'\n      <section>', 1)
            if 'data-service-search' not in page:
                raise ValueError('Service directory insertion failed')
        file.write_text(page, encoding='utf-8')
    css = (ROOT/'assets/css/styles.css').read_text(encoding='utf-8')
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    (ROOT/'assets/css/styles.min.css').write_text(css.strip(), encoding='utf-8')
    print('Shared UI, request page and stylesheet updated')

if __name__ == '__main__':
    main()
