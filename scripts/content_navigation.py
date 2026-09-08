"""Reusable, crawlable navigation and service-specific conversion content."""
import html
from urllib.parse import quote


def whatsapp_url(message):
    return 'https://wa.me/573018638164?text=' + quote(message, safe='')


def article_contact(article):
    message = (f"Hola Toyo Services. Consulté la guía: {article['title']}. "
               "Quiero orientación para mi Toyota. Modelo: __. Año: __. "
               "Kilometraje: __. Síntoma o repuesto: __.")
    return (f'<aside class="article-contact" aria-label="Consulta sobre esta guía">'
            '<strong>¿Necesitas resolverlo en tu Toyota?</strong>'
            '<p>Comparte modelo, año y el síntoma o repuesto que buscas. '
            'Con esos datos podemos orientar el siguiente paso en Cartagena.</p>'
            f'<a class="btn btn-primary" href="{whatsapp_url(message)}" target="_blank" '
            'rel="noopener">Consultar este caso por WhatsApp</a></aside>')


TOPICS = [
    ('mantenimiento', 'Mantenimiento, aceite y costos', {'mantenimiento-general', 'aceite-filtros'}),
    ('diagnostico', 'Motor, diagnóstico y aire acondicionado', {'motor-refrigeracion', 'reparacion-motor', 'diagnostico-electronico', 'mecanica-avanzada'}),
    ('frenos-transmision', 'Frenos, suspensión y transmisión', {'frenos-suspension', 'transmision'}),
    ('repuestos', 'Repuestos y compatibilidad', {'repuestos'}),
    ('proteccion', 'Pintura y protección', {'latoneria-pintura', 'ppf', 'recubrimiento-ceramico', 'proteccion-anticorrosiva', 'proteccion-interior'}),
    ('modificaciones', 'Accesorios y modificaciones', {'modificaciones', 'actualizacion-estetica'}),
]


def guide_directory(articles):
    nav = '<nav class="topic-links" aria-label="Temas de la Guía Toyota">' + ''.join(
        f'<a href="#{key}">{label}</a>' for key, label, _ in TOPICS) + '</nav>'
    sections = []
    for key, label, services in TOPICS:
        members = [a for a in articles if a['service_path'].strip('/').split('/')[-1] in services]
        members.sort(key=lambda a: a.get('datePublished', ''), reverse=True)
        items = ''.join(f'<li><a href="/blog/{a["slug"]}/">{html.escape(a["title"])}</a></li>' for a in members)
        sections.append(f'<section class="guide-topic" id="{key}"><h2>{label}</h2><ul>{items}</ul></section>')
    return ('<div class="guide-search" data-guide-search hidden>'
            '<label for="guide-search">Busca por modelo, síntoma o servicio</label>'
            '<input id="guide-search" type="search" placeholder="Ej. Fortuner, aceite, repuestos…" '
            'autocomplete="off" aria-controls="guide-directory">'
            '<p role="status" data-guide-count></p></div>' + nav +
            '<div class="guide-directory" id="guide-directory">' + ''.join(sections) + '</div>')


PARTS = [
    ('filtros', 'Filtros y mantenimiento', 'Filtros de aceite, aire, combustible y cabina. La referencia depende del motor y del sistema: antes de cotizar confirmamos año, versión y la especificación del fluido cuando corresponde.', '/servicios/aceite-filtros/', 'Cambio de aceite y filtros'),
    ('frenos', 'Pastillas y discos de freno', 'Pastillas, discos y componentes relacionados con el frenado. Indica eje delantero o trasero; la medida, el cáliper y la versión pueden cambiar la pieza. Un ruido o una vibración requieren diagnóstico antes de comprar.', '/servicios/frenos-suspension/', 'Revisión de frenos y suspensión'),
    ('suspension', 'Amortiguadores, bujes y dirección', 'Consulta amortiguadores, bujes, rótulas, terminales y rodamientos. Confirma lado y posición, además de la configuración de suspensión. Revisar holguras permite distinguir la pieza desgastada de otros posibles orígenes del ruido.', '/blog/suspension-toyota-ruidos-vibraciones-cartagena/', 'Cómo identificar ruidos de suspensión'),
    ('refrigeracion', 'Radiador, bomba de agua y ventilador', 'Repuestos del sistema de refrigeración: radiador, bomba de agua, termostato, mangueras y aspa del ventilador según aplicación. El aspa no es el conjunto completo del ventilador; indica exactamente qué componente necesitas.', '/servicios/motor-refrigeracion/', 'Diagnóstico de refrigeración'),
    ('motor', 'Motor, empaques y soportes', 'Empaques, sellos, soportes, correas y componentes de motor se consultan por referencia y daño comprobado. En una reparación mayor, el diagnóstico y las mediciones determinan qué piezas pueden reutilizarse y cuáles se requieren.', '/servicios/reparacion-motor/', 'Reparación de motor Toyota'),
    ('electrico', 'Batería, sensores y encendido', 'La batería debe corresponder a la capacidad y tecnología aplicables. Sensores, bobinas y otras piezas eléctricas exigen comprobar conector, referencia y causa de la falla: un código del escáner no confirma por sí solo un repuesto dañado.', '/servicios/diagnostico-electronico/', 'Diagnóstico antes de cambiar sensores'),
]


def parts_content():
    rows = []
    for key, title, text, href, label in PARTS:
        wa = whatsapp_url(f'Hola Toyo Services. Busco un repuesto de {title.lower()} para mi Toyota. Modelo: __. Año: __. Motor: __. Pieza o referencia: __. Compartiré el VIN y la foto por este chat.')
        rows.append(f'<article id="repuestos-{key}"><h3>{title}</h3><p>{text}</p>'
                    f'<p><a href="{href}">{label}</a></p><a href="{wa}" target="_blank" rel="noopener">Consultar referencia y disponibilidad →</a></article>')
    return ('<section class="service-expansion" id="categorias-repuestos"><div class="container">'
            '<span class="eyebrow">Encuentra la pieza correcta</span><h2>Repuestos Toyota por sistema</h2>'
            '<p>Estas son familias de repuestos que puedes consultar para Prado, Fortuner, Hilux, Corolla, Yaris y RAV4. '
            'Confirmamos disponibilidad, marca y plazo para cada referencia antes de cerrar la solicitud.</p>'
            '<div class="parts-grid">' + ''.join(rows) + '</div>'
            '<h2>Cómo cotizar un repuesto sin confundir la versión</h2>'
            '<ol><li>Indica modelo, año, motor y si tu Toyota es 4x2 o 4x4 cuando aplique.</li>'
            '<li>Comparte por WhatsApp el VIN y una foto legible de la referencia. Para piezas de carrocería, indica lado y posición.</li>'
            '<li>Confirma si necesitas solo suministro o también instalación. La cotización debe identificar pieza, marca, plazo y condiciones.</li></ol>'
            '<p>Consulta la <a href="/blog/repuestos-toyota-por-vin-cartagena/">guía de identificación por VIN</a> '
            'y las <a href="/blog/repuestos-toyota-originales-homologados-cartagena/">diferencias entre repuestos genuinos, OEM y alternativos</a>.</p>'
            '</div></section>')


def maintenance_content():
    return '''<section class="service-expansion" id="plan-mantenimiento"><div class="container">
<span class="eyebrow">Un plan según tu Toyota</span><h2>Mantenimiento por kilometraje, tiempo e historial</h2>
<p>Si tu Toyota se acerca a los 20.000, 40.000, 80.000 o 100.000 km, el primer paso es identificar el plan de su versión. Esas cifras no significan cambiar las mismas piezas en todos los Toyota. Revisamos qué corresponde por manual, qué ya se hizo y qué revela la inspección.</p>
<div class="parts-grid"><article><h3>Mantenimiento preventivo</h3><p>Para conservar el funcionamiento antes de una falla: aceite y filtros, inspección de frenos, suspensión, batería, niveles, fugas y refrigeración según el alcance cotizado.</p><a href="/blog/mantenimiento-preventivo-toyota-cartagena/">Qué incluye una revisión preventiva</a></article>
<article><h3>Mantenimiento correctivo</h3><p>Cuando ya hay testigos, fugas, vibraciones o pérdida de potencia, primero se diagnostica el sistema afectado. Cambiar consumibles no reemplaza la investigación de una avería.</p><a href="/servicios/diagnostico-electronico/">Diagnóstico de fallas Toyota</a></article>
<article><h3>Toyota usado o sin historial</h3><p>Organizamos una revisión inicial para conocer el estado del vehículo y los servicios pendientes. No asumimos que todos los fluidos o componentes se hayan sustituido por el kilometraje del tablero.</p><a href="/blog/inspeccion-precompra-toyota-usado-cartagena/">Qué revisar en un Toyota usado</a></article>
<article><h3>Antes de viajar</h3><p>Revisa con anticipación frenos, llantas, niveles, luces y temperatura de funcionamiento. Así queda margen para corregir hallazgos y verificar el vehículo antes de salir de Cartagena.</p><a href="/blog/revision-toyota-antes-de-viaje-cartagena/">Lista de revisión antes de viaje</a></article></div>
<h2>Qué determina el precio del mantenimiento</h2><p>Modelo, motor, kilometraje, historial y trabajo autorizado. Pide que la cotización distinga diagnóstico, mano de obra, fluidos, filtros y repuestos. Una inspección, un cambio de aceite y una reparación son alcances diferentes.</p>
<p><a href="/blog/costo-mantenimiento-toyota-cartagena/">Cómo comparar el costo de mantenimiento Toyota en Cartagena</a> · <a href="/blog/cada-cuanto-cambiar-aceite-toyota/">Cuándo corresponde cambiar el aceite</a></p>
<h2>Planes para Prado, Fortuner, Hilux y otros Toyota</h2><p>Consulta el enfoque de atención para <a href="/modelos/toyota-prado/">Toyota Prado</a>, <a href="/modelos/toyota-fortuner/">Toyota Fortuner</a> y <a href="/modelos/toyota-hilux/">Toyota Hilux</a>. Para Corolla, Yaris, RAV4 y otros modelos, confirma año, motor y versión al solicitar la visita.</p>
<p>En un híbrido hay diferencias respecto a una versión de gasolina: consulta <a href="/blog/mantenimiento-toyota-hibrido-cartagena/">qué verificar en el mantenimiento de un Toyota híbrido</a>. El alcance disponible se confirma antes de la intervención.</p>
</div></section>'''


def service_expansion(slug):
    return parts_content() if slug == 'repuestos' else maintenance_content() if slug == 'mantenimiento-general' else ''
