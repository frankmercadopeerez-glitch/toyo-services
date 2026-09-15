"""Shared, idempotent UI upgrades for generated and hand-authored pages."""
import html
import re
from urllib.parse import quote

SERVICES = {
    'mantenimiento-general': 'Mantenimiento general', 'aceite-filtros': 'Cambio de aceite y filtros',
    'diagnostico-electronico': 'Diagnóstico electrónico', 'reparacion-motor': 'Reparación de motor',
    'transmision': 'Transmisión', 'aire-acondicionado': 'Aire acondicionado',
    'motor-refrigeracion': 'Motor y refrigeración', 'bateria': 'Batería y sistema eléctrico',
    'frenos-suspension': 'Frenos y suspensión', 'repuestos': 'Repuestos',
    'mecanica-avanzada': 'Mecánica avanzada', 'latoneria-pintura': 'Latonería y pintura',
    'modificaciones': 'Modificaciones', 'actualizacion-estetica': 'Actualización estética',
    'ppf': 'PPF', 'recubrimiento-ceramico': 'Recubrimiento cerámico',
    'proteccion-anticorrosiva': 'Protección anticorrosiva', 'proteccion-interior': 'Protección interior',
    'otro': 'Necesito orientación',
}

def quote_form():
    options = ''.join(f'<option value="{k}">{v}</option>' for k,v in SERVICES.items())
    return f'''<form class="contact-form" data-whatsapp-form hidden>
<div class="form-field"><label for="contact-model">Modelo Toyota</label><input id="contact-model" name="modelo" list="toyota-models" required maxlength="60" placeholder="Ej. Prado, Fortuner, Hilux" autocomplete="off"><datalist id="toyota-models"><option value="Prado"><option value="Fortuner"><option value="Hilux"><option value="Corolla"><option value="Yaris"><option value="RAV4"><option value="Corolla Cross"><option value="Land Cruiser"></datalist></div>
<div class="form-field"><label for="contact-service">¿Qué necesitas?</label><select id="contact-service" name="servicio" required><option value="">Selecciona una opción</option>{options}</select></div>
<div class="form-field"><label for="contact-year">Año (opcional)</label><input id="contact-year" name="anio" type="number" inputmode="numeric" min="1950" max="2027" placeholder="Ej. 2020"></div>
<div class="form-field"><label for="contact-km">Kilometraje (opcional)</label><input id="contact-km" name="kilometraje" type="number" inputmode="numeric" min="0" max="9999999" step="1" placeholder="Ej. 80000"></div>
<div class="form-field form-field-wide"><label for="contact-version">Motor o versión (opcional)</label><input id="contact-version" name="version" maxlength="100" placeholder="Ej. 2.8 diésel, automática, 4x4"></div>
<fieldset class="parts-fields form-field-wide" data-parts-fields hidden disabled><legend>Datos del repuesto</legend><div class="form-field"><label for="contact-reference">Pieza o referencia (opcional)</label><input id="contact-reference" name="referencia" maxlength="100" placeholder="Nombre, código, lado o posición"></div><div class="form-field"><label for="contact-install">¿Necesitas instalación?</label><select id="contact-install" name="instalacion"><option>Por definir</option><option>Solo el repuesto</option><option>Repuesto e instalación</option></select></div><p class="form-hint">Puedes adjuntar la foto y el VIN directamente en WhatsApp. Confirmaremos compatibilidad y disponibilidad por referencia.</p></fieldset>
<div class="form-field form-field-wide"><label for="contact-message">Describe lo que necesitas</label><textarea id="contact-message" name="mensaje" rows="3" required maxlength="700" aria-describedby="contact-hint" placeholder="Síntoma, cuándo ocurre o trabajo que deseas realizar."></textarea><p class="form-hint" id="contact-hint" data-service-hint>Si no conoces el servicio, selecciona «Necesito orientación» y describe lo que ocurre.</p></div>
<div class="form-field form-field-wide"><label for="contact-name">Nombre (opcional)</label><input id="contact-name" name="nombre" autocomplete="name" maxlength="80"></div>
<label class="form-consent form-field-wide"><input type="checkbox" name="privacidad" required><span>Acepto enviar estos datos por WhatsApp y he leído la <a href="/privacidad/">política de privacidad</a>.</span></label>
<div class="form-submit form-field-wide"><button class="btn btn-primary" type="submit">Preparar mi solicitud →</button><span>Revisa el mensaje antes de abrir WhatsApp.</span></div>
<div class="request-preview form-field-wide" data-request-preview hidden><h3 tabindex="-1" data-preview-heading>Tu solicitud está lista para revisar</h3><label for="request-message">Mensaje para Toyo Services</label><textarea id="request-message" rows="9" readonly></textarea><div class="actions"><a class="btn btn-primary" data-request-link target="_blank" rel="noopener">Abrir WhatsApp y enviar</a><button class="btn btn-outline" type="button" data-copy-request>Copiar mensaje</button></div><p role="status" data-copy-status>La solicitud aún no se ha enviado. Puedes modificar los datos de arriba y prepararla de nuevo.</p></div>
</form>'''

def service_finder():
    items = [
        ('01', 'Me toca mantenimiento', 'Aceite, filtros y revisión por historial.', '/servicios/mantenimiento-general/'),
        ('02', 'Busco un repuesto', 'Identificación por versión y referencia.', '/servicios/repuestos/'),
        ('03', 'Tengo un testigo o una falla', 'Check Engine, pérdida de potencia o encendido.', '/servicios/diagnostico-electronico/'),
        ('04', 'Siento ruido o vibración', 'Frenos, dirección y suspensión.', '/servicios/frenos-suspension/'),
        ('05', 'Hay temperatura o una fuga', 'Revisión del motor y la refrigeración.', '/servicios/motor-refrigeracion/'),
        ('06', 'Quiero renovar o proteger', 'Pintura, acabados y protección exterior.', '/servicios/#latoneria-pintura'),
    ]
    cards = ''.join(f'<a href="{url}"><span class="finder-number">{n}</span><h3>{title}</h3><p>{desc}</p><span class="finder-arrow" aria-hidden="true">↗</span></a>' for n,title,desc,url in items)
    return f'''<section class="service-finder" aria-labelledby="finder-title"><div class="container"><span class="eyebrow">Empieza por lo que necesitas</span><h2 id="finder-title">Encuentra el siguiente paso para tu Toyota.</h2><div class="finder-grid">{cards}</div><p class="finder-help">¿No sabes por dónde empezar? <a href="/cotizar/?servicio=otro">Describe tu caso y solicita orientación →</a></p></div></section>'''

def enhance_page(page, route):
    page = re.sub(r'/assets/css/styles.min.css\?v=\d+', '/assets/css/styles.min.css?v=25', page)
    page = re.sub(r'/assets/js/main.js\?v=\d+', '/assets/js/main.js?v=21', page)
    if 'class="site-header"' in page:
        if 'class="skip"' not in page:
            page = page.replace('<body>', '<body><a class="skip" href="#contenido">Saltar al contenido</a>', 1)
        page = re.sub(r'<main(?![^>]*\bid=)([^>]*)>', r'<main id="contenido"\1>', page, count=1)
        page = page.replace('class="nav-links"', 'class="nav-links" id="principal-links"') if 'id="principal-links"' not in page else page
        page = page.replace('class="menu"', 'class="menu" aria-controls="principal-links" type="button"') if 'aria-controls="principal-links"' not in page else page
        if 'class="nav-quote"' not in page:
            page = re.sub(r'(<div class="nav-links"[^>]*>)(.*?)(</div>)', lambda m: m[1] + m[2] + '<a href="/servicios/repuestos/">Repuestos</a><a class="nav-quote" href="/cotizar/">Cotizar →</a>' + m[3], page, count=1, flags=re.S)
    if route.startswith('/servicios/') and route != '/servicios/':
        slug = route.strip('/').split('/')[-1]
        if 'class="service-jumps"' not in page:
            page = page.replace('<section class="service-detail-body">', '<nav class="service-jumps container" aria-label="En este servicio"><a href="#alcance">Qué incluye y proceso</a><a href="#preparar">Antes de venir</a><a href="#dudas">Preguntas frecuentes</a><a href="/cotizar/?servicio='+slug+'">Preparar solicitud →</a></nav><section class="service-detail-body" id="alcance">', 1)
            page = page.replace('<section class="service-detail-body">', '<section class="service-detail-body" id="preparar">', 1)
            page = page.replace('<section class="faq">', '<section class="faq" id="dudas">', 1)
            page = page.replace('<a class="btn btn-outline" href="/#ubicacion">Ver área de atención</a>', '<a class="btn btn-outline" href="/cotizar/?servicio='+slug+'">Preparar solicitud</a>')
    return page
