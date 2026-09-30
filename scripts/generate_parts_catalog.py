#!/usr/bin/env python3
"""Generate the parts catalogue and its single-product offer pages."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

from site_ui import enhance_page

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://toyoservicescartagena.com"
PRODUCTS = json.loads((Path(__file__).parent / "parts_catalog.json").read_text(encoding="utf-8"))

HEADER = '''<header class="site-header"><nav class="nav container"><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg?v=3" alt="" width="60" height="40"><span>TOYO <span>SERVICES</span></span></a><button class="menu" aria-expanded="false" aria-label="Abrir menú">☰</button><div class="nav-links"><a href="/">Inicio</a><a href="/servicios/">Servicios</a><a href="/modelos/">Modelos</a><a href="/blog/">Guía Toyota</a><a href="/#ubicacion">Área de atención</a></div></nav></header>'''
FOOTER = '''<footer class="footer"><div class="container"><div class="footer-grid"><div><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg?v=3" alt="" width="60" height="40"><span>TOYO <span>SERVICES</span></span></a><p class="muted">Mantenimiento, mecánica, repuestos y acabados premium en Cartagena.</p><p class="footer-contact"><a href="tel:+573018638164">+57 301 863 8164</a> · <a href="https://wa.me/573018638164" target="_blank" rel="noopener">WhatsApp</a></p></div><div><h3>Explora</h3><a href="/servicios/">Servicios</a><a href="/modelos/">Modelos Toyota</a><a href="/blog/">Guía Toyota</a><a href="/nosotros/">Nosotros</a></div><div><h3>Información</h3><a href="/metodologia/">Metodología editorial</a><a href="/preguntas-frecuentes/">Preguntas frecuentes</a><a href="/legal/">Condiciones del servicio</a><a href="/privacidad/">Privacidad y datos</a></div></div><div class="legal"><span>© <span data-year></span> Toyo Services.</span><span>Taller independiente no afiliado a Toyota Motor Corporation.</span></div></div></footer><a class="wa-float" href="https://wa.me/573018638164" target="_blank" rel="noopener" title="Escribir a Toyo Services por WhatsApp" aria-label="Escribir a Toyo Services por WhatsApp"><img src="/assets/images/whatsapp-logo.png" width="96" height="96" alt="" aria-hidden="true"></a><script src="/assets/js/main.js?v=22" defer></script>'''


def money(value: int) -> str:
    return f"${value:,.0f}".replace(",", ".")


def product_url(product: dict) -> str:
    return f"{BASE}/repuestos/{product['slug']}/"


def whatsapp(product: dict) -> str:
    message = (f"Hola Toyo Services. Quiero cotizar {product['short_name']} por {money(product['price'])} COP. "
               "Mi Hilux es año: __. Motor: __. Transmisión: __. Compartiré el VIN y la foto por este chat.")
    return "https://wa.me/573018638164?text=" + quote(message, safe="")


def schemas(product: dict) -> str:
    url = product_url(product)
    product_schema = {
        "@context": "https://schema.org", "@type": "Product", "@id": f"{url}#product",
        "name": product["name"], "description": product["description"],
        "category": product["category"], "url": url,
        "offers": {"@type": "Offer", "url": url, "price": product["price"],
                   "priceCurrency": product["currency"],
                   "availability": f"https://schema.org/{product['availability']}",
                   "seller": {"@type": "Organization", "@id": f"{BASE}/#business", "name": "Toyo Services"},
                   "areaServed": {"@type": "City", "name": "Cartagena de Indias"}},
    }
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Catálogo de repuestos", "item": f"{BASE}/repuestos/"},
            {"@type": "ListItem", "position": 3, "name": product["name"], "item": url},
        ],
    }
    return "".join(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>' for data in (product_schema, breadcrumb))


def product_page(product: dict) -> str:
    url = product_url(product)
    title = f"{product['short_name']} | {money(product['price'])} en Cartagena"
    compatibility = "".join(f"<li>{html.escape(item)}</li>" for item in product["compatibility"])
    request_data = "".join(f"<li>{html.escape(item)}</li>" for item in product["request_data"])
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(product['description'])} Precio: {money(product['price'])} COP. Llegada estimada a Cartagena en {product['lead_time_days']} días."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}"><meta property="og:type" content="product"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Toyo Services"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="Precio {money(product['price'])} COP. Disponible por pedido desde {product['origin']} para {product['destination']}."><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#080a0d"><link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="48x48"><link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="/site.webmanifest"><link rel="stylesheet" href="/assets/css/styles.min.css?v=26">{schemas(product)}</head><body>{HEADER}<main><section class="product-hero"><div class="container"><nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / <a href="/repuestos/">Repuestos</a> / Sensor de velocidad Hilux</nav><span class="eyebrow">Repuesto Toyota por pedido</span><h1>{html.escape(product['name'])}</h1><p class="product-lead">{html.escape(product['description'])}</p><div class="product-offer" aria-label="Precio y disponibilidad"><div><span>Precio del repuesto</span><strong>{money(product['price'])} <small>COP</small></strong></div><div><span>Disponibilidad</span><strong>{html.escape(product['availability_label'])}</strong></div><div><span>Entrega estimada</span><strong>{product['lead_time_days']} días a Cartagena</strong><small>Despacho desde {html.escape(product['origin'])}, sujeto a confirmación al ordenar.</small></div></div><div class="actions"><a class="btn btn-primary" href="{whatsapp(product)}" target="_blank" rel="noopener">Confirmar por VIN y pedir</a><a class="btn btn-outline" href="/repuestos/">Ver catálogo de repuestos</a></div></div></section><section class="product-details"><div class="container product-layout"><article><span class="eyebrow">Compatibilidad antes de comprar</span><h2>No todas las Hilux usan el mismo sensor</h2><p>El nombre del vehículo no confirma por sí solo la pieza. Verificamos la aplicación antes de solicitarla para reducir errores de conector, ubicación o referencia.</p><ul class="detail-checklist">{compatibility}</ul><h2>Datos necesarios para cotizar</h2><ul class="detail-checklist">{request_data}</ul></article><aside class="product-summary"><h2>Resumen de la oferta</h2><dl><div><dt>Producto</dt><dd>{html.escape(product['short_name'])}</dd></div><div><dt>Precio</dt><dd>{money(product['price'])} COP</dd></div><div><dt>Origen</dt><dd>{html.escape(product['origin'])}</dd></div><div><dt>Destino</dt><dd>{html.escape(product['destination'])}</dd></div><div><dt>Tiempo estimado</dt><dd>{product['lead_time_days']} días</dd></div></dl><p>Precio publicado para el repuesto. Si necesitas diagnóstico o instalación, ese alcance se confirma y cotiza por separado.</p><a class="btn btn-primary" href="{whatsapp(product)}" target="_blank" rel="noopener">Consultar disponibilidad actual</a></aside></div></section><section class="product-notes"><div class="container"><h2>Qué hace un sensor de velocidad</h2><p>Según la versión y la ubicación, una señal de velocidad puede intervenir en la información que reciben el tablero, la transmisión u otros módulos. Un código de falla o una lectura irregular no demuestra por sí solo que el sensor sea la causa: cableado, conectores y componentes relacionados también deben comprobarse.</p><h2>Precio y plazo</h2><p>El precio visible es <strong>{money(product['price'])} COP</strong>. La pieza se gestiona desde {html.escape(product['origin'])} y la llegada estimada a {html.escape(product['destination'])} es de {product['lead_time_days']} días, después de confirmar compatibilidad y disponibilidad. El plazo puede variar por hora de solicitud, transportadora o novedades logísticas; se confirma antes del pago.</p><p><a href="/blog/repuestos-toyota-por-vin-cartagena/">Aprende por qué el VIN evita comprar una referencia equivocada</a> o revisa el <a href="/servicios/repuestos/">servicio de repuestos Toyota en Cartagena</a>.</p></div></section></main>{FOOTER}</body></html>'''
    page = page.replace("/assets/css/styles.min.css?v=26", "/assets/css/styles.css?v=26")
    return enhance_page(page, f"/repuestos/{product['slug']}/")


def catalog_page() -> str:
    cards, items = [], []
    for index, product in enumerate(PRODUCTS, 1):
        path = f"/repuestos/{product['slug']}/"
        cards.append(f'''<article class="catalog-card"><span>{html.escape(product['category'])}</span><h2><a href="{path}">{html.escape(product['name'])}</a></h2><p>{html.escape(product['description'])}</p><div class="catalog-price"><strong>{money(product['price'])} COP</strong><small>{html.escape(product['availability_label'])} · {product['lead_time_days']} días a Cartagena</small></div><a class="text-link" href="{path}">Ver precio, compatibilidad y pedido →</a></article>''')
        items.append({"@type": "ListItem", "position": index, "url": f"{BASE}{path}", "name": product["name"]})
    schema = {"@context": "https://schema.org", "@type": "ItemList", "name": "Catálogo de repuestos Toyota en Cartagena", "itemListElement": items}
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Catálogo de repuestos Toyota en Cartagena | Precios</title><meta name="description" content="Consulta precios y disponibilidad de repuestos Toyota en Cartagena. Cada pieza se confirma por VIN, modelo, año, motor y transmisión antes del pedido."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}/repuestos/"><meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Toyo Services"><meta property="og:title" content="Catálogo de repuestos Toyota en Cartagena"><meta property="og:description" content="Precios, compatibilidad y tiempos estimados de repuestos Toyota por pedido."><meta property="og:url" content="{BASE}/repuestos/"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#080a0d"><link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="48x48"><link rel="stylesheet" href="/assets/css/styles.min.css?v=26"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body>{HEADER}<main><header class="page-hero"><div class="container"><nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / Repuestos</nav><span class="eyebrow">Catálogo en crecimiento</span><h1>Repuestos Toyota en Cartagena con precio y compatibilidad claros.</h1><p>Publicamos referencias disponibles por pedido y confirmamos cada aplicación por VIN antes de comprar. El precio y el plazo de cada ficha se verifican al momento de ordenar.</p></div></header><section><div class="container"><div class="catalog-grid">{''.join(cards)}</div><aside class="catalog-help"><h2>¿Buscas otro repuesto Toyota?</h2><p>Envíanos modelo, año, motor, transmisión, VIN y una fotografía o referencia. Lo revisamos y, cuando la información esté confirmada, podremos añadirlo a este catálogo.</p><a class="btn btn-primary" href="https://wa.me/573018638164?text=Hola%20Toyo%20Services.%20Busco%20un%20repuesto%20Toyota.%20Modelo%3A%20__.%20A%C3%B1o%3A%20__.%20Motor%3A%20__.%20Pieza%20o%20referencia%3A%20__." target="_blank" rel="noopener">Solicitar otro repuesto</a></aside></div></section></main>{FOOTER}</body></html>'''
    page = page.replace("/assets/css/styles.min.css?v=26", "/assets/css/styles.css?v=26")
    return enhance_page(page, "/repuestos/")


def main() -> None:
    catalog = ROOT / "repuestos"
    catalog.mkdir(exist_ok=True)
    (catalog / "index.html").write_text(catalog_page(), encoding="utf-8")
    for product in PRODUCTS:
        folder = catalog / product["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(product_page(product), encoding="utf-8")
    print(f"Generated catalog with {len(PRODUCTS)} product page(s)")


if __name__ == "__main__":
    main()
