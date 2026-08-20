from pathlib import Path
import html, json

from image_dimensions import sync_html_image_dimensions

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://toyoservicescartagena.com"

services = [
  {"slug":"mantenimiento-general","title":"Mantenimiento general Toyota en Cartagena","desc":"Mantenimiento preventivo y correctivo Toyota por kilometraje, historial y condición real en Cartagena.","image":"service-maintenance-premium.webp","intro":"Organizamos el mantenimiento de tu Toyota según modelo, año, kilometraje, historial y condiciones de uso. La revisión permite separar lo urgente, lo próximo y lo que solo necesita seguimiento.","includes":["Aceite, filtros, niveles y puntos de lubricación aplicables","Inspección de frenos, dirección, suspensión, llantas y luces","Revisión de batería, correas, mangueras, fugas y refrigeración","Registro de hallazgos y recomendaciones priorizadas"],"process":["Identificamos el vehículo y revisamos antecedentes y síntomas reportados.","Inspeccionamos los sistemas incluidos y confirmamos referencias antes de instalar piezas o fluidos.","Presentamos alcance y autorización; al terminar verificamos niveles, funcionamiento y recomendaciones."],"faqs":[["¿Cada cuánto debe revisarse?","Se parte del manual, tiempo y kilometraje, ajustados por tráfico, recorridos cortos, carga y ambiente."],["¿Incluye repuestos?","La cotización separa mano de obra, fluidos y repuestos según el servicio autorizado."],["¿Puedo hacer una revisión antes de viaje?","Sí. Conviene programarla con tiempo para corregir hallazgos y probar el vehículo."]]},
  {"slug":"transmision","title":"Servicio de transmisión Toyota en Cartagena","desc":"Diagnóstico y mantenimiento de transmisiones automáticas y mecánicas Toyota en Cartagena.","image":"service-transmission-premium.webp","intro":"Atendemos tirones, demoras al engranar, patinamiento, vibraciones, fugas y ruidos. El fluido y el procedimiento se eligen por transmisión y especificación; no aplicamos soluciones universales.","includes":["Inspección de fugas, soportes y condición externa","Lectura de códigos y datos cuando el sistema lo permite","Revisión de nivel y condición del fluido con el procedimiento aplicable","Prueba de funcionamiento y propuesta de diagnóstico o mantenimiento"],"process":["Documentamos cuándo aparece el síntoma y realizamos una prueba controlada si es seguro.","Combinamos datos electrónicos con revisión mecánica y del fluido.","Definimos si procede mantenimiento, reparación o pruebas adicionales antes de desmontar."],"faqs":[["¿Un cambio de fluido corrige cualquier tirón?","No. Primero debe identificarse la causa; un síntoma puede involucrar control, soportes, presión o desgaste."],["¿Hacen lavado de transmisión?","El método depende del diseño, estado e historial. No se recomienda una operación automática sin evaluación."],["¿Reparan transmisiones?","El alcance se define después del diagnóstico y según repuestos y condición del conjunto."]]},
  {"slug":"aceite-filtros","title":"Cambio de aceite Toyota en Cartagena","desc":"Cambio de aceite y filtros Toyota con viscosidad, norma y referencias apropiadas para cada motor.","image":"service-oil-premium.webp","intro":"Un cambio de aceite profesional utiliza la viscosidad y norma adecuadas, instala el filtro correcto y aprovecha la visita para detectar fugas, niveles anormales o desgaste visible.","includes":["Aceite según motor, año y especificación aplicable","Filtro de aceite y revisión de filtros relacionados","Inspección visual de fugas, correas, mangueras y niveles","Reinicio del recordatorio de mantenimiento cuando corresponde"],"process":["Confirmamos versión, motor, capacidad y especificación.","Drenamos de forma segura, sustituimos filtro y verificamos sellos y torque.","Comprobamos nivel y fugas después de circular el lubricante y registramos el servicio."],"faqs":[["¿Qué aceite usa mi Toyota?","Depende de motor, año y manual. No debe decidirse solo por clima o kilometraje."],["¿Puedo llevar el aceite?","Debe verificarse sellado, procedencia, cantidad y especificación antes de autorizarlo."],["¿Cada cuánto se cambia?","Se siguen tiempo y kilometraje del fabricante, considerando condiciones severas de uso."]]},
  {"slug":"frenos-suspension","title":"Frenos y suspensión Toyota en Cartagena","desc":"Diagnóstico de frenos, dirección y suspensión Toyota para ruidos, vibraciones y pérdida de estabilidad.","image":"service-brakes-premium.webp","intro":"Ruidos, vibraciones, desviaciones y rebote necesitan una inspección conjunta. Frenos, llantas, rodamientos, dirección y suspensión pueden producir síntomas parecidos.","includes":["Pastillas, discos, líquido, mangueras y cálipers","Amortiguadores, resortes, bujes, rótulas y terminales","Rodamientos, llantas, rines y fijaciones","Prueba de manejo y recomendación de alineación cuando aplica"],"process":["Reproducimos el síntoma de forma controlada y revisamos el vehículo apoyado y elevado.","Medimos desgaste y holguras antes de seleccionar piezas.","Después de reparar comprobamos torque, respuesta, ruidos y geometría aplicable."],"faqs":[["¿Un ruido siempre es amortiguador?","No. Bujes, rótulas, frenos, rodamientos o fijaciones pueden sonar de forma similar."],["¿La alineación elimina vibraciones?","No siempre; balanceo, llantas, rines, frenos y transmisión también deben considerarse."],["¿Cuándo no debo seguir conduciendo?","Si hay pérdida de frenado, rueda inestable, ruido severo o desviación peligrosa, detén el vehículo con seguridad."]]},
  {"slug":"motor-refrigeracion","title":"Motor y refrigeración Toyota en Cartagena","desc":"Diagnóstico de motor y sistema de refrigeración Toyota para temperatura, fugas, potencia y consumo irregular.","image":"service-cooling-premium.webp","intro":"Atendemos pérdida de potencia, temperatura elevada, consumo de fluidos, humo, ruidos y fallas de encendido. Antes de reparar confirmamos el origen con inspección y pruebas dirigidas.","includes":["Inspección de fugas, mangueras, correas y conexiones","Pruebas de presión, temperatura, compresión o señales según el caso","Radiadores, bomba, termostato, ventiladores y refrigerante","Diagnóstico de encendido, admisión, combustible y condición mecánica"],"process":["Registramos condiciones del síntoma y comprobamos niveles sin abrir sistemas calientes.","Diseñamos pruebas según evidencia; no desmontamos por intuición.","Definimos alcance, repuestos y verificaciones posteriores antes de autorizar la reparación."],"faqs":[["¿Puedo conducir si sube la temperatura?","No. Detente con seguridad y evita abrir el sistema caliente; continuar puede aumentar el daño."],["¿El refrigerante se elige por color?","No. El color no demuestra especificación ni compatibilidad."],["¿Hacen reparaciones mayores?","Sí, sujetas a diagnóstico, disponibilidad de repuestos y autorización del alcance."]]},
  {"slug":"reparacion-motor","title":"Reparación de motor Toyota en Cartagena","desc":"Diagnóstico y reparación de motores Toyota con pruebas, desarme autorizado, medición, rectificación y armado según la condición comprobada.","image":"service-engine-repair-premium.webp","intro":"Una reparación de motor comienza demostrando por qué consume aceite, pierde compresión, emite humo, se recalienta o produce un ruido interno. Medimos antes de desmontar y documentamos lo encontrado para decidir entre una reparación localizada, una reconstrucción o una alternativa de reemplazo.","includes":["Pruebas de compresión, fugas, presión de aceite y refrigeración según el síntoma","Desmontaje e inspección interna únicamente con alcance autorizado","Medición de culata, bloque, cilindros, pistones, cigüeñal y componentes aplicables","Rectificación externa, repuestos, armado, fluidos y verificaciones cotizados por etapas"],"process":["Confirmamos el síntoma, revisamos historial, niveles, códigos y señales mecánicas antes de abrir.","Si el diagnóstico lo justifica, autorizamos una etapa de desmontaje, limpieza y medición para establecer el daño real.","Presentamos alternativas, piezas y mecanizados; después del armado verificamos presión, temperatura, fugas y funcionamiento."],"faqs":[["¿Cuánto cuesta reparar un motor Toyota?","No existe un precio responsable sin diagnóstico. Depende del motor, daño, mecanizados, repuestos y componentes reutilizables; cotizamos por etapas."],["¿Siempre hay que rectificar el motor?","No. La rectificación se decide con mediciones y tolerancias; algunos casos admiten una reparación localizada y otros requieren un alcance mayor."],["¿Es mejor reparar o cambiar el motor?","Se comparan daño, trazabilidad del motor alternativo, compatibilidad, costo total y garantía. La decisión se toma con evidencia, no solo por el precio inicial."]]},
  {"slug":"diagnostico-electronico","title":"Diagnóstico electrónico Toyota en Cartagena","desc":"Escaneo y diagnóstico electrónico Toyota con interpretación de códigos, datos y pruebas físicas.","image":"service-electronics-premium.webp","intro":"Leer códigos es el comienzo, no el diagnóstico completo. Relacionamos la queja con datos, cableado, alimentación, sensores y condición mecánica para evitar cambios por ensayo y error.","includes":["Lectura de códigos y datos congelados o en vivo","Pruebas de batería, carga, tierras y conexiones cuando aplican","Comprobación de señales, continuidad, actuadores y componentes","Informe de causa confirmada o siguiente prueba necesaria"],"process":["Conservamos la información antes de borrar códigos o desconectar componentes.","Verificamos el circuito y la condición señalada por el sistema.","Después de corregir repetimos pruebas y comprobamos parámetros o ciclos de conducción."],"faqs":[["¿El escáner dice qué pieza cambiar?","Normalmente no; indica circuitos o condiciones que deben comprobarse."],["¿Pueden borrar una luz del tablero?","Borrarla sin corregir la causa no es una reparación y puede eliminar evidencia útil."],["¿Diagnostican fallas intermitentes?","Sí, aunque pueden requerir registro de condiciones, tiempo de prueba o que la falla se manifieste."]]},
  {"slug":"mecanica-avanzada","title":"Mecánica avanzada Toyota en Cartagena","desc":"Diagnóstico y reparación de fallas complejas Toyota con pruebas mecánicas y electrónicas.","image":"service-diagnostics-premium.webp","intro":"Las fallas complejas exigen relacionar síntomas, datos y mediciones. Nuestro proceso busca demostrar la causa y definir el alcance antes de autorizar reparaciones mayores.","includes":["Diagnóstico combinado de motor, transmisión y electrónica","Pruebas mecánicas, eléctricas y de funcionamiento","Desarme exploratorio únicamente con autorización previa","Presupuesto por etapas cuando la condición interna no es visible"],"process":["Definimos una estrategia de diagnóstico y explicamos sus límites iniciales.","Documentamos resultados y separamos diagnóstico de reparación.","Al reparar, verificamos funcionamiento, fugas, códigos y la condición original reportada."],"faqs":[["¿Cobran el diagnóstico?","El diagnóstico es trabajo técnico y su alcance se informa antes de iniciarlo."],["¿El presupuesto puede cambiar al abrir?","Puede ocurrir si hay daño interno no visible; cualquier ampliación requiere nueva autorización."],["¿Garantizan que una sola prueba encuentre todo?","No siempre. Las fallas intermitentes o múltiples pueden requerir etapas, pero se informa cada avance."]]},
  {"slug":"repuestos","title":"Repuestos Toyota en Cartagena","desc":"Identificación, suministro e instalación de repuestos Toyota para todos los sistemas.","image":"service-parts-premium.webp","intro":"Gestionamos repuestos por modelo, año, VIN, motor y referencia. Presentamos alternativas genuinas, OEM u homologadas cuando son apropiadas y están disponibles.","includes":["Identificación de referencia y compatibilidad","Cotización con marca y alcance cuando sea posible","Instalación, consumibles y procedimientos relacionados","Verificación de funcionamiento y trazabilidad de la pieza"],"process":["Confirmamos el vehículo y la pieza antes de comprar o desmontar.","Explicamos disponibilidad, alternativa y condiciones de garantía.","Instalamos con el procedimiento aplicable y entregamos soporte documental disponible."],"faqs":[["¿Todo repuesto debe ser genuino?","No existe una respuesta única; depende de criticidad, especificación, fabricante y disponibilidad."],["¿Puedo llevar mi repuesto?","Sí, sujeto a verificación y a condiciones claras sobre compatibilidad y garantía de la pieza."],["¿Venden repuestos sin instalación?","Debe consultarse por referencia y disponibilidad; algunos diagnósticos requieren el vehículo."]]},
  {"slug":"modificaciones","title":"Modificaciones Toyota en Cartagena","desc":"Modificaciones integradas para Toyota Prado, Fortuner, Hilux y otros modelos con evaluación de compatibilidad.","image":"service-modifications-premium.webp","intro":"Diseñamos cambios de suspensión, ruedas, iluminación, protección y presencia exterior según uso real. Una modificación debe funcionar como sistema y conservar seguridad y mantenibilidad.","includes":["Definición de objetivo, carga, uso y presupuesto","Compatibilidad de rines, llantas, suspensión y fijaciones","Integración eléctrica protegida para equipos aplicables","Prueba, torque, alineación y documentación según el proyecto"],"process":["Revisamos primero la condición mecánica de base.","Diseñamos fases y comprobamos medidas, cargas e interferencias.","Instalamos, probamos y explicamos mantenimiento y revisiones posteriores."],"faqs":[["¿Toda elevación mejora el 4x4?","No. Cambia geometría, centro de gravedad, confort y desgaste; debe diseñarse según uso."],["¿Instalan rines y llantas?","Sí, después de comprobar medida, PCD, offset, carga y espacio."],["¿Las modificaciones afectan garantía?","Puede depender de la garantía aplicable; conviene revisar sus condiciones antes de intervenir."]]},
  {"slug":"latoneria-pintura","title":"Latonería y pintura Toyota en Cartagena","desc":"Reparación de carrocería, preparación e igualación de pintura Toyota con control de acabado.","image":"service-body-paint-premium.webp","intro":"Recuperamos forma, protección y color después de golpes, rayones o reparaciones previas. La calidad depende de evaluar daños ocultos, preparar la superficie y controlar el acabado.","includes":["Inspección de paneles, soportes, luces y sensores","Corrección de abolladuras y preparación de superficies","Igualación de color, aplicación y difuminado cuando corresponde","Armado, limpieza y control final de acabado y funciones"],"process":["Documentamos daños visibles y desmontajes necesarios.","Acordamos reparación o sustitución y posibles hallazgos internos.","Controlamos color, textura, bordes, armado y curado antes de entregar."],"faqs":[["¿Pueden igualar colores perlados?","Sí, con identificación, pruebas de color y evaluación del acabado actual."],["¿Reparan sin pintar?","Depende del acceso, profundidad y estado de la pintura."],["¿Cuándo puedo lavar o pulir?","La indicación depende del sistema aplicado y sus tiempos de curado."]]},
  {"slug":"actualizacion-estetica","title":"Actualización estética Toyota en Cartagena","desc":"Renovación exterior e interior Toyota con integración limpia de detalles, molduras e iluminación.","image":"service-detailing-premium.webp","intro":"Renovamos elementos envejecidos y añadimos mejoras compatibles sin perder la identidad del modelo. Primero revisamos pintura, ópticas, molduras, interior y sistemas cercanos.","includes":["Evaluación de superficies, piezas y reparaciones previas","Restauración o sustitución de detalles exteriores e interiores","Integración de iluminación y elementos compatibles","Control de acabado, fijaciones y funciones intervenidas"],"process":["Definimos una dirección visual y priorizamos restauración antes de añadir piezas.","Comprobamos medidas, materiales, sensores y puntos de montaje.","Entregamos un resultado integrado con instrucciones de cuidado."],"faqs":[["¿Pueden modernizar un Toyota antiguo?","Sí, según estado, compatibilidad y disponibilidad de piezas."],["¿Cambiar a LED siempre es posible?","No. Óptica, disipación, patrón y sistema eléctrico deben ser compatibles."],["¿Se puede hacer por etapas?","Sí. Se priorizan restauración, funcionalidad y acabados según presupuesto."]]},
  {"slug":"ppf","title":"PPF para Toyota en Cartagena","desc":"Instalación de película protectora PPF para pintura Toyota en zonas de impacto o cobertura completa.","image":"service-ppf-listing.webp","intro":"La película PPF crea una barrera física transparente frente a gravilla, insectos y roces superficiales. Evaluamos pintura, cobertura y terminaciones antes de instalar.","includes":["Inspección, lavado y descontaminación de pintura","Corrección previa acordada cuando sea necesaria","Cobertura frontal, zonas de contacto o proyecto completo","Terminación de bordes e instrucciones de curado y lavado"],"process":["Definimos cobertura y comprobamos estabilidad de la pintura.","Preparamos la superficie y aplicamos patrones con tensión controlada.","Revisamos bordes, contaminación y acabado después del asentamiento inicial."],"faqs":[["¿El PPF evita cualquier daño?","No. Ayuda frente a desgaste e impactos ligeros, pero no evita abolladuras o cortes profundos."],["¿Se instala sobre pintura reparada?","Solo después de evaluar estabilidad y curado."],["¿Puede combinarse con cerámico?","Sí, si ambos sistemas son compatibles y se define el orden correcto."]]},
  {"slug":"recubrimiento-ceramico","title":"Recubrimiento cerámico para Toyota en Cartagena","desc":"Aplicación de recubrimiento cerámico, conocido comercialmente como cristal líquido, con preparación de pintura.","image":"service-ceramic-listing.webp","intro":"El recubrimiento cerámico aporta repelencia, brillo y facilidad de limpieza. No sustituye la corrección de pintura ni funciona como barrera contra golpes o rayones profundos.","includes":["Lavado técnico y descontaminación","Inspección y corrección de pintura según alcance acordado","Aplicación y nivelación del recubrimiento seleccionado","Instrucciones de curado, lavado y mantenimiento"],"process":["Evaluamos la pintura y mostramos el resultado realista posible.","Preparamos la superficie y aplicamos bajo condiciones controladas.","Verificamos residuos, uniformidad y tiempos antes de la entrega."],"faqs":[["¿Es lo mismo que cristal líquido?","Ese término comercial se usa para varios productos; identificamos el recubrimiento y su ficha real."],["¿Evita rayones?","No los profundos. Facilita limpieza y añade una capa sacrificable limitada."],["¿Cuánto dura?","Depende del producto, preparación, exposición y mantenimiento; no existe una duración universal."]]},
  {"slug":"proteccion-anticorrosiva","title":"Protección anticorrosiva Toyota en Cartagena","desc":"Inspección y protección anticorrosiva de bajos Toyota para humedad y ambiente costero.","image":"service-anticorrosion-listing.webp","intro":"La protección anticorrosiva comienza con inspección, limpieza y secado. No cubrimos óxido activo, humedad o suciedad sin tratar porque eso puede ocultar el problema.","includes":["Inspección de bajos, uniones, soportes y drenajes","Limpieza, secado y preparación de áreas aplicables","Protección de frenos, escape, sensores y piezas móviles","Aplicación localizada o integral y plan de inspección"],"process":["Elevamos de forma segura y documentamos la condición inicial.","Tratamos material inestable y enmascaramos zonas que deben quedar libres.","Aplicamos el sistema seleccionado y explicamos curado y revisiones."],"faqs":[["¿Se aplica encima del óxido?","No sin preparación y evaluación del nivel de corrosión."],["¿Es permanente?","No. Puede dañarse y requiere inspección periódica."],["¿Todos los vehículos costeros lo necesitan?","No necesariamente; la recomendación depende de exposición, materiales y condición."]]},
  {"slug":"proteccion-interior","title":"Protección interior Toyota en Cartagena","desc":"Limpieza y protección de cuero, plásticos, vinilo y tapicería Toyota con acabados naturales.","image":"service-interior-listing.webp","intro":"Tratamos cada material con productos compatibles y acabados naturales. Evitamos residuos grasosos en volante, controles y pedales y diferenciamos suciedad de desgaste o decoloración.","includes":["Aspirado y limpieza por tipo de material","Prueba de compatibilidad en zonas discretas","Protección de cuero, vinilo, plástico o textil aplicable","Cuidado de costuras, perforaciones, pantallas y mandos"],"process":["Identificamos materiales, manchas y daños antes de intervenir.","Limpiamos por secciones con humedad y herramientas controladas.","Aplicamos protección compatible, retiramos exceso y explicamos mantenimiento."],"faqs":[["¿Repara cuero agrietado?","No. Una grieta o pérdida de color requiere restauración específica."],["¿Protege interiores claros?","Sí, aunque ningún tratamiento impide toda transferencia o mancha."],["¿Deja brillo?","Buscamos un acabado natural y seguro, no una capa grasosa."]]}
]

# Capa comercial y editorial. Mantener cada bloque específico evita que las
# fichas compitan entre sí con texto genérico y permite que cada URL responda a
# una intención local distinta.
commercial = {
  "mantenimiento-general": {
    "meta_title": "Mantenimiento Toyota en Cartagena | Toyo Services",
    "meta_desc": "Mantenimiento Toyota en Cartagena por kilometraje y condición: aceite, filtros, frenos, suspensión, batería, refrigeración y diagnóstico.",
    "signs_heading": "Cuándo programar el mantenimiento de tu Toyota",
    "signs_intro": [
      "El mantenimiento no comienza cuando aparece una avería. Conviene programarlo por tiempo, kilometraje y uso, y adelantar la revisión si notas un cambio de comportamiento. Luces de advertencia, ruidos nuevos, consumo irregular o fluidos bajo el vehículo justifican una evaluación antes de seguir acumulando kilómetros.",
      "También es útil revisar el vehículo antes de un viaje, después de comprarlo usado o cuando no existe un historial confiable. La inspección permite construir una línea base y ordenar el trabajo por seguridad, confiabilidad y prevención, sin sustituir piezas únicamente por costumbre."
    ],
    "signals": ["Testigos, ruidos o vibraciones que antes no estaban", "Pérdida de potencia, aumento de consumo o arranque lento", "Fugas, olores, temperatura inusual o niveles que bajan", "Servicio próximo por tiempo, kilometraje o viaje"],
    "scope_heading": "Qué revisamos en un mantenimiento integral",
    "process_heading": "Cómo priorizamos cada hallazgo",
    "local_heading": "Mantenimiento para el uso diario en Cartagena",
    "local_paragraphs": [
      "El calor, la humedad, el tráfico lento, los recorridos cortos y la cercanía al ambiente marino pueden aumentar la exigencia sobre batería, refrigeración, frenos, aire acondicionado y acabados. Eso no significa aplicar el mismo intervalo reducido a todos los vehículos: revisamos el manual y la forma real en que se utiliza.",
      "Atendemos automóviles y SUV como Corolla, Yaris, RAV4, Fortuner y Land Cruiser Prado, además de Hilux de uso particular. Año, motor, versión e historial importan más que el nombre comercial por sí solo, por eso confirmamos los datos antes de recomendar fluidos o repuestos."
    ],
    "parts_heading": "Repuestos, fluidos y autorización del servicio",
    "parts_paragraphs": [
      "La propuesta identifica, cuando es posible, la marca o especificación del fluido, el filtro y las piezas previstas. Una recomendación puede cambiar si la inspección descubre desgaste adicional; cualquier ampliación debe explicarse y autorizarse antes de instalar componentes o realizar un desmontaje no incluido.",
      "Las condiciones de garantía y respaldo dependen de la pieza, su proveedor, la instalación y el uso. Conservamos la trazabilidad disponible y distinguimos el servicio realizado de fallas ajenas al alcance contratado. Toyo Services es un taller independiente y no representa a Toyota Motor Corporation."
    ],
    "bring_heading": "Datos útiles para preparar la visita",
    "bring_intro": "Para orientar la revisión desde el inicio, comparte información concreta del vehículo y evita borrar testigos o desconectar la batería antes del diagnóstico.",
    "bring": ["Modelo, año, versión, motor y kilometraje", "Historial, facturas o fecha del último mantenimiento", "Síntomas, momento en que aparecen y testigos observados", "Viajes próximos, uso habitual y reparaciones recientes"],
    "related": [("Guía de mantenimiento preventivo en Cartagena", "/blog/mantenimiento-preventivo-toyota-cartagena/"), ("Cambio de aceite y filtros", "/servicios/aceite-filtros/"), ("Diagnóstico electrónico", "/servicios/diagnostico-electronico/")]
  },
  "transmision": {
    "meta_title": "Transmisión Toyota en Cartagena | Toyo Services",
    "meta_desc": "Diagnóstico y servicio de transmisión Toyota en Cartagena para tirones, fugas, demoras, vibraciones y mantenimiento de cajas automáticas o mecánicas.",
    "signs_heading": "Síntomas que justifican revisar la transmisión",
    "signs_intro": [
      "Una demora al seleccionar Drive o reversa, tirones, patinamiento, vibración, zumbido o fuga no confirman por sí solos una transmisión dañada. Soportes, ejes, sistema electrónico, temperatura y condición del motor pueden producir sensaciones parecidas. Documentar cuándo ocurre el síntoma ayuda a escoger las pruebas correctas.",
      "Si el vehículo pierde tracción, golpea con fuerza, presenta una fuga abundante o activa una advertencia junto con funcionamiento limitado, es prudente detenerlo de forma segura y solicitar orientación. Continuar conduciendo puede alterar la evidencia o aumentar el alcance de la reparación."
    ],
    "signals": ["Demora o golpe al engranar una posición", "Revoluciones que aumentan sin avance proporcional", "Fuga, olor a fluido recalentado o temperatura anormal", "Tirones, vibración o ruido que cambian con la velocidad"],
    "scope_heading": "Diagnóstico de caja antes de cambiar componentes",
    "process_heading": "Pruebas para definir mantenimiento o reparación",
    "local_heading": "Tráfico, temperatura y uso en Cartagena",
    "local_paragraphs": [
      "El tráfico a baja velocidad y las temperaturas ambientales altas pueden hacer más visible un problema térmico o de presión. El servicio se adapta al diseño de la caja, el historial y el tipo de recorrido; no asumimos que todos los Toyota utilizan el mismo fluido ni el mismo procedimiento de nivel.",
      "Prado, Fortuner, Hilux, RAV4, Corolla y otros modelos pueden incorporar transmisiones diferentes según año, motor y mercado. Confirmamos versión y, cuando corresponde, VIN o código del conjunto antes de cotizar fluido, filtro, empaques o piezas internas."
    ],
    "parts_heading": "Fluido, repuestos y límites del diagnóstico",
    "parts_paragraphs": [
      "El color del fluido no basta para decidir una intervención. Se consideran especificación, nivel bajo el procedimiento aplicable, contaminación, códigos, datos y respuesta del vehículo. Un cambio de fluido no se ofrece como cura universal para tirones o desgaste interno.",
      "Cuando se requiere desmontaje, la cotización puede organizarse por etapas porque algunas condiciones solo son visibles al abrir. Se informa el hallazgo y se solicita autorización antes de ampliar el trabajo. La garantía aplicable depende de las piezas instaladas y del alcance documentado."
    ],
    "bring_heading": "Qué contar antes de la prueba",
    "bring_intro": "Una descripción precisa reduce pruebas innecesarias y ayuda a reproducir una falla intermitente en condiciones controladas.",
    "bring": ["Modelo, año, motor, kilometraje y tipo de transmisión", "Si ocurre en frío, caliente, subida, frenado o velocidad constante", "Servicios anteriores de fluido y referencia utilizada", "Testigos, códigos previos, fugas o reparaciones recientes"],
    "related": [("Señales de falla en transmisión Toyota", "/blog/senales-transmision-toyota/"), ("Diagnóstico electrónico Toyota", "/servicios/diagnostico-electronico/"), ("Mecánica avanzada Toyota", "/servicios/mecanica-avanzada/")]
  },
  "aceite-filtros": {
    "meta_title": "Cambio de aceite Toyota en Cartagena | Toyo Services",
    "meta_desc": "Cambio de aceite Toyota en Cartagena con filtro, especificación y viscosidad correctas, revisión de fugas, niveles y registro del mantenimiento realizado.",
    "signs_heading": "Cuándo cambiar aceite y filtros",
    "signs_intro": [
      "El intervalo se define con el manual del vehículo, el tiempo transcurrido, el kilometraje y las condiciones de uso. Recorridos cortos frecuentes, tráfico intenso, polvo, carga o periodos largos de inactividad pueden justificar una revisión distinta a la de un vehículo que viaja regularmente por carretera.",
      "Un testigo de presión, ruido repentino, fuga importante o nivel fuera de rango requiere diagnóstico; no debe tratarse únicamente añadiendo lubricante. El recordatorio de mantenimiento tampoco mide por sí solo la calidad del aceite: es una ayuda que debe interpretarse con el historial."
    ],
    "signals": ["Fecha o kilometraje próximos según historial y manual", "Nivel que baja, aumenta o cambia sin explicación", "Fuga visible, olor a aceite o humo", "Testigo de presión o ruido que exige detenerse con seguridad"],
    "scope_heading": "Qué incluye un cambio de aceite bien ejecutado",
    "process_heading": "Selección, instalación y comprobación final",
    "local_heading": "Viscosidad y uso de tu Toyota en Cartagena",
    "local_paragraphs": [
      "El clima caliente no autoriza a elegir un aceite más grueso de manera automática. Se revisan las viscosidades permitidas, la norma de desempeño, el motor, posibles sistemas de emisiones y el uso. En una Hilux diésel, por ejemplo, la versión exacta es indispensable; dos unidades similares pueden requerir productos distintos.",
      "Corolla, Yaris, RAV4, Prado, Fortuner y Hilux también cambian capacidad y referencia de filtro según generación. Confirmamos esos datos antes de drenar para disponer de la cantidad correcta y evitar improvisaciones durante el servicio."
    ],
    "parts_heading": "Aceite, filtro y trazabilidad",
    "parts_paragraphs": [
      "La cotización identifica la especificación y cantidad previstas, además del filtro y los elementos de sellado aplicables. Si el cliente aporta productos, se revisan envase, procedencia, cantidad y compatibilidad; aceptar una pieza suministrada por terceros implica condiciones de garantía diferentes que deben quedar claras.",
      "Durante el servicio observamos fugas y niveles accesibles, pero esa inspección no equivale a un diagnóstico completo de todos los sistemas. Cualquier reparación adicional se informa por separado y requiere autorización."
    ],
    "bring_heading": "Información para cotizar el aceite correcto",
    "bring_intro": "Compartir la versión exacta evita basar la recomendación en una fotografía o en el nombre general del modelo.",
    "bring": ["Modelo, año, motor y kilometraje actual", "VIN o tarjeta del vehículo cuando exista duda de versión", "Aceite usado anteriormente y fecha del último cambio", "Consumo, fugas, humo, testigos o reparaciones recientes"],
    "related": [("Qué incluye el cambio de aceite Toyota", "/blog/cambio-aceite-toyota-cartagena/"), ("Aceite recomendado para Hilux diésel", "/blog/aceite-recomendado-toyota-hilux-diesel/"), ("Mantenimiento general Toyota", "/servicios/mantenimiento-general/")]
  },
  "frenos-suspension": {
    "meta_title": "Frenos y suspensión Toyota en Cartagena | Toyo Services",
    "meta_desc": "Revisión de frenos y suspensión Toyota en Cartagena: pastillas, discos, líquido, amortiguadores, bujes, dirección, ruidos y vibraciones.",
    "signs_heading": "Ruidos, vibraciones y cambios de estabilidad",
    "signs_intro": [
      "Un chirrido al frenar, pedal diferente, desviación, rebote, golpe al pasar irregularidades o vibración en el volante merece revisión. El origen puede estar en frenos, llantas, rines, rodamientos, dirección o suspensión, por lo que sustituir el componente más visible no siempre resuelve la causa.",
      "Si disminuye la capacidad de frenado, el pedal se va al fondo, una rueda se siente inestable o el vehículo se desvía peligrosamente, no conviene continuar conduciendo. Detenerse con seguridad protege a los ocupantes y evita agravar daños."
    ],
    "signals": ["Ruido, pulsación o cambio en el recorrido del pedal", "Rebote, inclinación o golpe al pasar desniveles", "Volante descentrado, vibración o desgaste irregular de llanta", "Fuga, testigo de frenos o pérdida de estabilidad"],
    "scope_heading": "Inspección conjunta de frenos, dirección y suspensión",
    "process_heading": "Medición y prueba antes de seleccionar piezas",
    "local_heading": "Uso urbano, vías irregulares y ambiente costero",
    "local_paragraphs": [
      "En Cartagena, tráfico, humedad, agua y superficies irregulares pueden revelar ruidos o acelerar deterioros ya existentes. Revisamos corrosión visible, guardapolvos, mangueras, fijaciones y desgaste, sin afirmar que el ambiente sea la única causa de una falla.",
      "Prado y Fortuner tienen pesos y configuraciones diferentes a Corolla, Yaris o RAV4. En Hilux también importa la carga y cualquier modificación previa. La selección de amortiguadores, pastillas o componentes se hace por versión y uso, no solo por apariencia."
    ],
    "parts_heading": "Piezas, alineación y garantía del trabajo",
    "parts_paragraphs": [
      "Antes de cotizar se miden espesores, holguras y condición de los elementos relacionados. Alineación y balanceo se recomiendan cuando aportan al diagnóstico, pero no se presentan como solución automática para vibraciones causadas por discos, llantas deformadas, rodamientos o transmisión.",
      "La propuesta separa las piezas necesarias de los trabajos opcionales. Después de intervenir se comprueban torque, respuesta y el síntoma reportado. El respaldo depende de la pieza instalada, la reparación autorizada y el uso posterior."
    ],
    "bring_heading": "Cómo describir el comportamiento",
    "bring_intro": "Indica con precisión cuándo aparece el síntoma para orientar la prueba y reducir desmontajes exploratorios.",
    "bring": ["Velocidad, superficie y temperatura cuando aparece", "Si cambia al frenar, girar, acelerar o pasar un desnivel", "Trabajos recientes de llantas, frenos, dirección o suspensión", "Carga habitual, golpes fuertes y modificaciones instaladas"],
    "related": [("Guía de frenos Toyota", "/blog/frenos-toyota-mantenimiento-cartagena/"), ("Ruidos de suspensión Toyota", "/blog/suspension-toyota-ruidos-vibraciones-cartagena/"), ("Suspensión de Toyota Prado", "/blog/suspension-toyota-prado-cartagena/")]
  },
  "motor-refrigeracion": {
    "meta_title": "Motor y refrigeración Toyota en Cartagena | Toyo Services",
    "meta_desc": "Diagnóstico de motor y refrigeración Toyota en Cartagena para recalentamiento, fugas, humo, pérdida de potencia, consumo de fluidos y fallas de encendido.",
    "signs_heading": "Señales de motor o refrigeración que no conviene aplazar",
    "signs_intro": [
      "Temperatura elevada, pérdida de refrigerante, humo, olor dulce, fallas de encendido, ruido nuevo o caída de potencia requieren una revisión dirigida. Un mismo síntoma puede tener causas distintas y añadir fluidos repetidamente puede ocultar una fuga sin resolverla.",
      "Cuando la temperatura sube fuera de lo normal, aparece una advertencia crítica o el motor pierde lubricación, detén el vehículo en un lugar seguro. No abras el sistema de refrigeración caliente: existe riesgo de quemadura y el daño puede aumentar si se continúa conduciendo."
    ],
    "signals": ["Indicador de temperatura alto o ventilador operando de forma inusual", "Refrigerante o aceite que disminuyen sin explicación", "Humo, olor, cascabeleo, ruido o vibración nuevos", "Pérdida de potencia, ralentí irregular o consumo elevado"],
    "scope_heading": "Pruebas para encontrar la causa y no solo el síntoma",
    "process_heading": "Diagnóstico por etapas antes del desmontaje",
    "local_heading": "Calor y tráfico de Cartagena",
    "local_paragraphs": [
      "La temperatura ambiental y el tráfico lento exigen que radiador, ventiladores, bomba, termostato y sellado funcionen correctamente. Sin embargo, el clima no explica por sí solo un recalentamiento; medimos temperatura, presión y señales según la evidencia encontrada.",
      "La configuración cambia entre motores de Corolla, RAV4, Prado, Fortuner e Hilux. Confirmar año, motor y reparaciones previas permite seleccionar refrigerante, empaques y componentes compatibles y evita mezclar productos únicamente por color."
    ],
    "parts_heading": "Alcance, repuestos y reparación mayor",
    "parts_paragraphs": [
      "Una prueba inicial puede señalar la siguiente etapa sin revelar todavía la condición interna completa. Si se requiere desmontar culata, distribución u otro conjunto, explicamos el objetivo, el costo de esa etapa y los posibles hallazgos antes de solicitar autorización.",
      "Cotizamos repuestos por referencia y disponibilidad, e indicamos las verificaciones posteriores necesarias. La garantía se limita al trabajo y componentes documentados; una falla diferente o preexistente no queda incluida automáticamente."
    ],
    "bring_heading": "Datos que ayudan a reproducir la falla",
    "bring_intro": "No limpies fugas ni borres información justo antes de la cita si hacerlo no es necesario para mover el vehículo con seguridad.",
    "bring": ["Cuándo comenzó y si ocurre en frío, tráfico o carretera", "Fluidos añadidos, cantidades y frecuencia", "Testigos, humo, olores, ruidos y pérdida de potencia", "Reparaciones de motor o refrigeración realizadas previamente"],
    "related": [("Cómo evitar recalentamientos Toyota", "/blog/sistema-refrigeracion-toyota-cartagena/"), ("Reparación de motor Toyota", "/servicios/reparacion-motor/"), ("Mecánica avanzada Toyota", "/servicios/mecanica-avanzada/")]
  },
  "reparacion-motor": {
    "meta_title": "Reparación de motor Toyota en Cartagena | Toyo Services",
    "meta_desc": "Reparación de motor Toyota en Cartagena con diagnóstico, mediciones, rectificación, repuestos y armado documentados antes de definir el alcance.",
    "signs_heading": "Señales que pueden requerir una evaluación interna del motor",
    "signs_intro": [
      "Humo azul, consumo anormal de aceite, baja compresión, mezcla de fluidos, presión insuficiente, ruido interno o recalentamientos repetidos merecen una evaluación pronta. Ninguna señal confirma por sí sola que el motor deba reconstruirse: sellos, ventilación del cárter, turbo, inyección o refrigeración pueden producir síntomas relacionados.",
      "Si se enciende la advertencia de presión de aceite, la temperatura sube, aparece un golpe metálico fuerte o el vehículo pierde potencia de forma repentina, detén el motor en un lugar seguro. Continuar circulando puede transformar una falla reparable en daño de bloque, culata o cigüeñal."
    ],
    "signals": ["Humo azul persistente o consumo de aceite medido entre cambios", "Compresión desigual, pérdida de potencia o falla de encendido recurrente", "Golpeteo interno, baja presión de aceite o partículas metálicas", "Recalentamiento previo, mezcla de aceite y refrigerante o pérdida sin fuga visible"],
    "scope_heading": "Pruebas, desarme y medición antes de cotizar la reparación",
    "process_heading": "De la evidencia al armado y la verificación",
    "local_heading": "Reparación de motores Toyota en Cartagena",
    "local_paragraphs": [
      "Atendemos motores de automóviles y SUV Toyota según versión, año e historial. Corolla, RAV4, Prado, Fortuner, Hilux y otras familias utilizan diseños, tolerancias y referencias diferentes; identificar correctamente el motor evita pedir piezas por apariencia o aplicar una medida de otro conjunto.",
      "El calor y el tráfico de Cartagena pueden hacer visible un problema térmico, pero no son un diagnóstico. Revisamos refrigeración, lubricación, admisión, combustible y control electrónico antes de atribuir el daño a una sola causa, porque reconstruir sin corregir el origen puede repetir la falla."
    ],
    "parts_heading": "Rectificación, repuestos, garantía y decisiones por etapas",
    "parts_paragraphs": [
      "Una cotización inicial puede cubrir diagnóstico y desmontaje. Después de limpiar y medir se determina qué piezas cumplen tolerancia, qué componentes deben reemplazarse y qué trabajos externos de culata, bloque o cigüeñal son necesarios. Cada ampliación se presenta antes de continuar.",
      "Comparamos repuestos por referencia, fabricante y trazabilidad. La garantía se documenta según el trabajo, piezas y mecanizados contratados, y exige cumplir fluidos, asentamiento y controles posteriores indicados. No prometemos precio ni fecha final antes de conocer el daño interno y la disponibilidad real."
    ],
    "bring_heading": "Información que reduce pruebas repetidas",
    "bring_intro": "El historial de consumo y reparaciones permite separar una falla progresiva de un evento reciente y orientar las primeras mediciones.",
    "bring": ["Modelo, año, motor, kilometraje y VIN si está disponible", "Cantidad de aceite o refrigerante añadida y distancia recorrida", "Videos de humo, ruido, testigos o momento de la falla", "Facturas, pruebas de compresión y reparaciones previas de motor o refrigeración"],
    "related": [("Toyota consume aceite o echa humo azul", "/blog/toyota-consume-aceite-humo-azul/"), ("Toyota no enciende: causas frecuentes", "/blog/toyota-no-enciende-causas/"), ("¿Reparar o cambiar el motor Toyota?", "/blog/reparar-o-cambiar-motor-toyota/")]
  },
  "diagnostico-electronico": {
    "meta_title": "Diagnóstico Toyota en Cartagena | Toyo Services",
    "meta_desc": "Diagnóstico electrónico Toyota en Cartagena con escaneo, datos en vivo y pruebas de batería, cableado, sensores y actuadores antes de recomendar repuestos.",
    "signs_heading": "Cuándo solicitar un diagnóstico electrónico",
    "signs_intro": [
      "Check Engine, ABS, airbag, carga, control de estabilidad y otras advertencias informan que un sistema detectó una condición, pero no indican automáticamente qué pieza cambiar. También atendemos fallas intermitentes, consumos de batería y comportamientos eléctricos sin testigo permanente.",
      "Una luz roja crítica, pérdida de potencia severa, humo o sobretemperatura puede exigir detener el vehículo. Para advertencias no críticas, evita borrar códigos o desconectar la batería antes de la revisión porque se pueden perder datos congelados y condiciones útiles."
    ],
    "signals": ["Check Engine u otra advertencia encendida o intermitente", "Arranque lento, batería que se descarga o accesorios inestables", "Falla que aparece con lluvia, calor, vibración o movimiento", "Componente sustituido sin que desaparezca el síntoma"],
    "scope_heading": "Del código de falla a una causa comprobada",
    "process_heading": "Escaneo, medición y verificación",
    "local_heading": "Diagnóstico para distintos modelos Toyota",
    "local_paragraphs": [
      "Los módulos y funciones disponibles cambian entre Corolla, Yaris, RAV4, Prado, Fortuner, Hilux y cada generación. La comunicación con el escáner es una fuente de información; se complementa con diagrama, inspección, alimentación, tierras y pruebas físicas cuando corresponden.",
      "Humedad, calor o reparaciones anteriores pueden influir en conexiones, pero no atribuimos una falla al ambiente sin evidencia. En problemas intermitentes puede ser necesario registrar datos, repetir condiciones o conservar el vehículo durante una ventana de prueba acordada."
    ],
    "parts_heading": "Diagnóstico separado de la reparación",
    "parts_paragraphs": [
      "El diagnóstico es trabajo técnico aunque concluya que una pieza no debe cambiarse. Si se confirma una reparación, presentamos su alcance por separado. Si la evidencia todavía no es suficiente, informamos la siguiente prueba en vez de prometer una respuesta inmediata.",
      "Los módulos o sensores se identifican por versión y referencia antes de comprarlos. Programación, calibración o codificación solo se incluyen cuando son aplicables y han sido cotizadas; no todas las sustituciones se resuelven conectando una pieza nueva. La garantía de una reparación se limita al alcance comprobado y autorizado."
    ],
    "bring_heading": "Información que no debes borrar",
    "bring_intro": "La secuencia exacta de una falla intermitente puede ser tan valiosa como el código almacenado.",
    "bring": ["Fotografía o video del tablero y mensaje mostrado", "Momento, clima y maniobra cuando ocurre", "Baterías, accesorios o módulos instalados recientemente", "Códigos o diagnósticos anteriores sin reemplazar la evidencia actual"],
    "related": [("Qué significa el Check Engine Toyota", "/blog/check-engine-diagnostico-electronico-toyota/"), ("Mecánica avanzada Toyota", "/servicios/mecanica-avanzada/"), ("Motor y refrigeración Toyota", "/servicios/motor-refrigeracion/")]
  },
  "mecanica-avanzada": {
    "meta_title": "Mecánica Toyota en Cartagena | Toyo Services",
    "meta_desc": "Mecánica avanzada Toyota en Cartagena para fallas complejas de motor, transmisión, refrigeración y electrónica, con diagnóstico y autorización por etapas.",
    "signs_heading": "Fallas complejas que requieren pruebas coordinadas",
    "signs_intro": [
      "Cuando una falla persiste después de reparaciones, aparece solo bajo determinadas condiciones o involucra varios sistemas, conviene detener el cambio de piezas por ensayo. Pérdida de potencia, consumo de fluidos, vibraciones, ruido interno o advertencias recurrentes necesitan una estrategia basada en mediciones.",
      "La mecánica avanzada no significa desmontar de inmediato. Primero se confirma la queja, se consulta el historial y se decide qué pruebas pueden separar causas mecánicas, eléctricas, electrónicas o de instalación."
    ],
    "signals": ["Falla repetida después de una reparación anterior", "Ruido interno, humo, consumo o compresión irregular", "Síntoma que relaciona motor, transmisión y electrónica", "Desmontaje mayor propuesto sin pruebas que expliquen la causa"],
    "scope_heading": "Diagnóstico mecánico y electrónico integrado",
    "process_heading": "Decisiones por etapas y con evidencia",
    "local_heading": "Aplicación en Prado, Fortuner, Hilux y automóviles Toyota",
    "local_paragraphs": [
      "Cada familia mecánica tiene procedimientos, tolerancias y referencias diferentes. En Prado, Fortuner o Hilux también se considera el sistema 4x4, la carga y modificaciones; en Corolla, Yaris y RAV4 importan sus configuraciones específicas y el historial de mantenimiento.",
      "Las condiciones de Cartagena pueden hacer visibles problemas térmicos o eléctricos, pero no sustituyen un diagnóstico. Probamos el vehículo bajo condiciones seguras y razonables, sin prometer reproducir de inmediato una falla que aparece de forma esporádica."
    ],
    "parts_heading": "Desarme exploratorio, repuestos y presupuesto",
    "parts_paragraphs": [
      "Algunas condiciones internas solo se confirman al abrir. En esos casos se autoriza primero una etapa de desmontaje e inspección, se documentan los hallazgos y se prepara una ampliación antes de comprar piezas o continuar el armado.",
      "La cotización distingue diagnóstico, mano de obra, mecanizados externos cuando sean necesarios y repuestos identificados. Las garantías y tiempos dependen del alcance, disponibilidad y servicios de terceros; se comunican sin prometer resultados fuera de lo comprobable."
    ],
    "bring_heading": "Historial necesario para no repetir trabajo",
    "bring_intro": "Facturas, referencias instaladas y resultados de pruebas anteriores ayudan a decidir qué debe comprobarse nuevamente.",
    "bring": ["Modelo, versión, motor, kilometraje y modificaciones", "Cronología del síntoma y reparaciones ya realizadas", "Consumo de aceite o refrigerante medido", "Códigos, pruebas de compresión u otros informes disponibles"],
    "related": [("Cómo se diagnostica una falla compleja", "/blog/mecanica-avanzada-toyota-cartagena/"), ("Diagnóstico electrónico Toyota", "/servicios/diagnostico-electronico/"), ("Transmisión Toyota", "/servicios/transmision/")]
  },
  "repuestos": {
    "meta_title": "Repuestos Toyota en Cartagena | Toyo Services",
    "meta_desc": "Repuestos Toyota en Cartagena identificados por VIN y referencia, con opciones genuinas, OEM u homologadas, suministro, instalación y trazabilidad.",
    "signs_heading": "La referencia correcta antes de comprar",
    "signs_intro": [
      "Dos Toyota del mismo modelo pueden utilizar piezas diferentes por año, motor, transmisión, mercado o fecha de producción. Por eso evitamos confirmar compatibilidad únicamente con una fotografía. VIN, referencia desmontada y datos técnicos reducen devoluciones y montajes incorrectos.",
      "Suministramos piezas asociadas a un diagnóstico o a una necesidad identificada. Cuando se solicita venta sin instalación, aclaramos qué datos faltan, qué comprobaciones corresponden al comprador y qué condiciones dependen del proveedor."
    ],
    "signals": ["Referencia ilegible o pieza modificada previamente", "Varias opciones para un mismo modelo y año", "Componente crítico de frenos, dirección, motor o transmisión", "Compra por internet sin confirmar medidas, conector o especificación"],
    "scope_heading": "Identificación, suministro e instalación",
    "process_heading": "Cómo reducimos errores de compatibilidad",
    "local_heading": "Repuestos para Toyota en Cartagena",
    "local_paragraphs": [
      "Gestionamos solicitudes para Corolla, Yaris, RAV4, Prado, Fortuner, Hilux y otros modelos atendidos por el taller. La disponibilidad cambia y no publicamos inventario ficticio: confirmamos referencia, marca, plazo informado por el proveedor y alcance de instalación antes del pago o autorización.",
      "En el ambiente costero conviene revisar fijaciones, sellos y componentes relacionados durante el montaje, pero una pieza no se reemplaza solo por ubicación. La inspección define si existe corrosión, desgaste, contaminación o daño adicional."
    ],
    "parts_heading": "Genuino, OEM, homologado y condiciones de garantía",
    "parts_paragraphs": [
      "Una pieza genuina se comercializa bajo la marca del vehículo; OEM y alternativas homologadas requieren evaluar fabricante, especificación y criticidad. No todas las opciones son equivalentes ni la más costosa es automáticamente la indicada. Presentamos la alternativa disponible con su identificación cuando la información del proveedor lo permite.",
      "La garantía puede provenir del fabricante o proveedor y está sujeta a instalación, uso y diagnóstico. Una pieza aportada por el cliente conserva las condiciones de quien la vendió; el taller responde por la mano de obra dentro del alcance acordado, no por defectos de un componente externo."
    ],
    "bring_heading": "Datos para solicitar un repuesto",
    "bring_intro": "Cuanta más precisión exista al inicio, menor es el riesgo de cotizar una variante incompatible.",
    "bring": ["VIN, modelo, año, motor y transmisión", "Referencia de la pieza o fotografía legible de etiquetas", "Lado, posición, medidas y conector cuando aplican", "Diagnóstico que justifica el cambio y piezas relacionadas"],
    "related": [("Guía de repuestos originales, OEM y homologados", "/blog/repuestos-toyota-originales-homologados-cartagena/"), ("Mantenimiento general Toyota", "/servicios/mantenimiento-general/"), ("Diagnóstico electrónico Toyota", "/servicios/diagnostico-electronico/")]
  },
  "modificaciones": {
    "meta_title": "Modificaciones Toyota en Cartagena | Toyo Services",
    "meta_desc": "Modificaciones para Toyota Prado, Fortuner e Hilux en Cartagena: suspensión, rines, llantas, protección e iluminación con revisión de compatibilidad.",
    "signs_heading": "Primero define qué debe mejorar el vehículo",
    "signs_intro": [
      "Una modificación útil parte de un objetivo: viajes, uso urbano, terreno irregular, carga, presencia visual o protección. Elegir piezas solo por apariencia puede aumentar ruido, peso, consumo, esfuerzo de dirección o desgaste y reducir la facilidad de mantenimiento.",
      "Antes de diseñar el proyecto revisamos la condición mecánica base. Holguras, frenos débiles, llantas envejecidas o fallas eléctricas deben resolverse antes de añadir altura, masa o consumo eléctrico."
    ],
    "signals": ["Roce de llantas o geometría alterada", "Accesorios sin fusible, soporte o ruta protegida", "Elevación sin considerar alineación y ángulos", "Peso adicional sin revisar carga ni frenado"],
    "scope_heading": "Compatibilidad entre suspensión, ruedas y accesorios",
    "process_heading": "Diseño, instalación y comprobaciones",
    "local_heading": "Proyectos para Prado, Fortuner e Hilux en Cartagena",
    "local_paragraphs": [
      "Estos modelos ofrecen múltiples configuraciones y no comparten automáticamente rines, llantas o suspensión. Revisamos PCD, offset, ancho, carga, interferencias y geometría. En Hilux también importa el uso de la platón; en Prado y Fortuner, el confort y la estabilidad familiar suelen tener prioridad.",
      "La circulación urbana exige conservar visibilidad, maniobrabilidad y acceso a mantenimiento. El uso de iluminación, protecciones y cambios de dimensiones debe respetar las normas aplicables; el cliente conserva la responsabilidad sobre homologación y uso en vía."
    ],
    "parts_heading": "Piezas, legalidad y garantía",
    "parts_paragraphs": [
      "Cotizamos por fases cuando el proyecto combina varios sistemas. Identificamos las piezas instaladas y las revisiones posteriores de torque o alineación. Un accesorio suministrado por el cliente se evalúa antes de aceptar el montaje y conserva la garantía de su vendedor.",
      "Una modificación puede influir en garantías vigentes del vehículo y en otros componentes. Toyo Services no representa a Toyota Motor Corporation; recomendamos revisar las condiciones del fabricante, aseguradora y regulación antes de autorizar cambios relevantes."
    ],
    "bring_heading": "Información para diseñar el proyecto",
    "bring_intro": "Fotos de referencia sirven para hablar de estilo, pero las medidas y el uso real determinan la viabilidad. Revisamos además el estado actual para que el proyecto no dependa de componentes desgastados o instalaciones anteriores sin protección.",
    "bring": ["Modelo, año, versión, medida actual de rin y llanta", "Carga, pasajeros, ciudad, viajes y uso fuera de vía", "Modificaciones instaladas y piezas que ya compraste", "Objetivo, prioridades y cambios que no deseas aceptar"],
    "related": [("Guía de modificaciones Hilux y 4x4", "/blog/transformaciones-toyota-hilux-4x4-cartagena/"), ("Rines recomendados para Toyota Prado", "/blog/rines-toyota-prado-medidas-recomendadas/"), ("Frenos y suspensión Toyota", "/servicios/frenos-suspension/")]
  },
  "latoneria-pintura": {
    "meta_title": "Latonería Toyota en Cartagena | Toyo Services",
    "meta_desc": "Latonería y pintura Toyota en Cartagena para golpes, rayones y paneles reparados, con evaluación, preparación, igualación de color y control de acabado.",
    "signs_heading": "Evaluar el daño antes de prometer un acabado",
    "signs_intro": [
      "Un golpe visible puede involucrar soportes, grapas, luces, sensores o bordes ocultos. También puede existir pintura anterior con espesor o adherencia diferentes. La inspección define si conviene reparar, sustituir, desmontar o realizar una prueba antes de cotizar el acabado final.",
      "Rayones que atraviesan la capa de color, metal expuesto, desalineación o ingreso de agua no deberían aplazarse. Una solución cosmética rápida puede ocultar corrosión o dejar sin corregir una función de seguridad."
    ],
    "signals": ["Panel deformado, bordes desalineados o cierre irregular", "Pintura saltada, metal expuesto o corrosión", "Luz, cámara, sensor o moldura afectados", "Diferencia de tono o textura de una reparación anterior"],
    "scope_heading": "De la estructura visible al acabado final",
    "process_heading": "Desmontaje, preparación y control de color",
    "local_heading": "Pintura y ambiente costero de Cartagena",
    "local_paragraphs": [
      "Sol, humedad y contaminación superficial influyen en la apariencia y en el cuidado posterior, pero no utilizamos el clima como explicación automática para un defecto. Se revisa el estado real de la pintura, reparaciones anteriores y zonas de corrosión antes de definir materiales y preparación.",
      "Corolla, Yaris, RAV4, Prado, Fortuner e Hilux tienen piezas, molduras y colores que varían por versión. El código de color orienta, pero la igualación puede requerir pruebas y ajuste por el envejecimiento del acabado existente."
    ],
    "parts_heading": "Repuestos de carrocería, hallazgos y garantía",
    "parts_paragraphs": [
      "La cotización inicial se basa en daños visibles. Si el desmontaje revela soporte roto, reparación previa o corrosión oculta, documentamos el hallazgo y solicitamos autorización adicional. No reemplazamos piezas sin explicar por qué la reparación dejó de ser apropiada.",
      "El cuidado, curado y exposición posterior afectan el resultado. Entregamos recomendaciones y delimitamos la garantía al material y trabajo aplicados; golpes, rayones nuevos o fallas ajenas al panel intervenido no forman parte del alcance."
    ],
    "bring_heading": "Qué necesitamos para estimar el trabajo",
    "bring_intro": "Las fotografías ayudan a una orientación inicial, pero la cotización definitiva puede requerir inspección y desmontaje autorizado. No ocultes bordes o piezas sueltas antes de la evaluación.",
    "bring": ["Fotos con luz natural desde varios ángulos", "Modelo, año, código de color si está disponible", "Descripción del golpe y funciones afectadas", "Reparaciones anteriores, seguro y piezas ya adquiridas"],
    "related": [("Guía de latonería y pintura Toyota", "/blog/latoneria-pintura-toyota-cartagena/"), ("Actualización estética Toyota", "/servicios/actualizacion-estetica/"), ("PPF para Toyota", "/servicios/ppf/")]
  },
  "actualizacion-estetica": {
    "meta_title": "Estética Toyota en Cartagena | Toyo Services",
    "meta_desc": "Actualización estética Toyota en Cartagena con renovación de molduras, iluminación y detalles exteriores o interiores, según estado y compatibilidad.",
    "signs_heading": "Restaurar antes de añadir elementos",
    "signs_intro": [
      "Una actualización bien integrada comienza por identificar qué está envejecido, mal reparado o incompleto. Molduras opacas, iluminación desigual, fijaciones rotas y acabados incompatibles pueden necesitar restauración antes de incorporar nuevas piezas.",
      "El objetivo no es convertir todos los vehículos en el mismo proyecto. Definimos una dirección visual acorde con el modelo, el uso y el estado para evitar accesorios que interfieran con sensores, visibilidad, mantenimiento o seguridad."
    ],
    "signals": ["Molduras sueltas, decoloradas o con fijaciones rotas", "Iluminación modificada con patrón o conexión inadecuados", "Piezas decorativas que interfieren con sensores", "Acabados interiores grasosos, incompatibles o deteriorados"],
    "scope_heading": "Actualizaciones exteriores e interiores compatibles",
    "process_heading": "Diseño visual y ejecución por etapas",
    "local_heading": "Acabados para Toyota de uso premium en Cartagena",
    "local_paragraphs": [
      "La exposición al sol y la humedad puede acelerar cambios de color y deterioro de algunos materiales. Evaluamos si una superficie puede recuperarse, requiere sustitución o necesita un tratamiento diferente. Ninguna protección elimina por completo el envejecimiento.",
      "Prado, Fortuner, RAV4, Corolla y otros Toyota tienen lenguajes de diseño distintos. Buscamos que iluminación, molduras, emblemas y detalles conserven proporción y funcionalidad, sin presentar el vehículo como una versión que no es."
    ],
    "parts_heading": "Compatibilidad, piezas y expectativas",
    "parts_paragraphs": [
      "Antes de comprar confirmamos medidas, conectores, puntos de montaje y posibles interferencias. La disponibilidad de una pieza estética cambia y las fotografías de catálogo pueden variar; identificamos lo cotizado y evitamos prometer una coincidencia no comprobada.",
      "La garantía depende de la pieza y del tipo de instalación. Cambios eléctricos o perforaciones requieren autorización expresa. Toyo Services es independiente de Toyota Motor Corporation y no ofrece conversiones como si fueran actualizaciones oficiales de fábrica."
    ],
    "bring_heading": "Cómo definir el resultado esperado",
    "bring_intro": "Una lista de prioridades ayuda a separar restauración, funcionalidad y cambios puramente visuales. También permite organizar el proyecto por etapas, comprobar primero las piezas de mayor impacto y conservar coherencia entre exterior e interior. Indica si el vehículo debe mantenerse completamente reversible y qué elementos originales deseas guardar después del trabajo.",
    "bring": ["Modelo, año, versión y fotografías actuales", "Referencias visuales y elementos que deseas conservar", "Accesorios o reparaciones ya instalados", "Presupuesto por etapas y fecha objetivo razonable"],
    "related": [("Ideas de actualización estética Toyota", "/blog/actualizacion-estetica-toyota-cartagena/"), ("Protección interior Toyota", "/servicios/proteccion-interior/"), ("Latonería y pintura Toyota", "/servicios/latoneria-pintura/")]
  },
  "ppf": {
    "meta_title": "PPF Toyota en Cartagena | Toyo Services",
    "meta_desc": "Instalación de PPF para Toyota en Cartagena, desde zonas de impacto hasta cobertura amplia, con preparación de pintura, terminación y cuidados de curado.",
    "signs_heading": "Cuándo tiene sentido proteger con PPF",
    "signs_intro": [
      "El PPF resulta útil en zonas expuestas a gravilla, insectos, roces de uso y contacto frecuente, como frontal, bordes, manijas o estribos. La cobertura se decide según recorridos, estado de la pintura, presupuesto y tiempo previsto de conservación del vehículo.",
      "La película no corrige pintura ni evita abolladuras, vandalismo o impactos severos. Aplicarla sobre un acabado inestable puede revelar o acelerar problemas, por lo que inspeccionamos repintes, contaminación y defectos antes de confirmar la instalación."
    ],
    "signals": ["Frontal expuesto a carretera o viajes frecuentes", "Rayones ligeros repetidos en manijas y zonas de carga", "Pintura reciente cuyo curado debe verificarse", "Repintes, barniz desprendido o contaminación que requieren evaluación"],
    "scope_heading": "Preparación, cobertura y terminación de bordes",
    "process_heading": "Instalación y revisión después del asentamiento",
    "local_heading": "PPF bajo sol, humedad y uso en Cartagena",
    "local_paragraphs": [
      "El calor y la exposición exterior influyen en curado, limpieza y envejecimiento. Entregamos indicaciones sobre el primer lavado, presión de agua y contaminantes; no prometemos una duración universal porque producto, cobertura, cuidado y estacionamiento cambian el resultado.",
      "En Prado, Fortuner, Hilux y RAV4 se pueden priorizar frontal, espejos, bordes y zonas de carga. En Corolla o Yaris la estrategia puede concentrarse en impactos urbanos. La forma del panel y reparaciones previas condicionan terminaciones y cobertura."
    ],
    "parts_heading": "Película, pintura previa y condiciones de respaldo",
    "parts_paragraphs": [
      "La cotización identifica cobertura y película propuesta. Corrección de pintura, desmontaje de accesorios o retiro de material anterior son trabajos separados cuando resultan necesarios. Si existe pintura reparada, la adherencia y el curado deben evaluarse antes de instalar o retirar PPF.",
      "La garantía o respaldo corresponde al material y la instalación documentados, sujeto al uso y mantenimiento. Bordes manipulados, golpes, cortes o fallas de pintura preexistentes no se consideran automáticamente defectos de la película."
    ],
    "bring_heading": "Datos para definir la cobertura",
    "bring_intro": "Una inspección presencial permite identificar repintes y medir la complejidad mejor que una sola fotografía. También ayuda a acordar terminaciones, bordes y zonas que deben quedar excluidas.",
    "bring": ["Modelo, año y paneles que deseas proteger", "Uso urbano, carretera, parqueadero y zonas de contacto", "Historial de pintura, pulido, cerámico o PPF anterior", "Resultado esperado y presupuesto de cobertura"],
    "related": [("Guía completa de PPF para Toyota", "/blog/ppf-toyota-cartagena-proteccion-pintura/"), ("Recubrimiento cerámico Toyota", "/servicios/recubrimiento-ceramico/"), ("Latonería y pintura Toyota", "/servicios/latoneria-pintura/")]
  },
  "recubrimiento-ceramico": {
    "meta_title": "Cerámico Toyota en Cartagena | Toyo Services",
    "meta_desc": "Recubrimiento cerámico para Toyota en Cartagena con lavado, descontaminación, preparación de pintura, aplicación controlada y guía de mantenimiento.",
    "signs_heading": "Qué puede y qué no puede hacer un cerámico",
    "signs_intro": [
      "Un recubrimiento cerámico puede aportar repelencia, brillo y una limpieza más sencilla, pero no funciona como una película contra impactos ni elimina rayones profundos. El resultado visual depende principalmente de la preparación y del estado de la pintura antes de aplicar.",
      "El término cristal líquido se usa para productos diferentes. Antes de cotizar aclaramos el sistema, la preparación incluida y las expectativas de duración, sin basarnos únicamente en nombres comerciales o promesas universales."
    ],
    "signals": ["Pintura áspera o contaminada que necesita preparación", "Marcas de lavado que deben evaluarse antes de sellar", "Vehículo recién pintado cuyo curado aún no está confirmado", "Cerámico anterior con comportamiento irregular"],
    "scope_heading": "Preparación de pintura y aplicación uniforme",
    "process_heading": "Curado, inspección y entrega",
    "local_heading": "Mantenimiento del recubrimiento en Cartagena",
    "local_paragraphs": [
      "Sol, lluvia, salinidad ambiental, agua y técnicas de lavado influyen en el desempeño. Recomendamos métodos y productos compatibles y explicamos que la repelencia puede reducirse por contaminación superficial sin que eso confirme que el recubrimiento desapareció.",
      "La aplicación puede realizarse en automóviles y SUV Toyota después de revisar pintura, plásticos y reparaciones. Prado, Fortuner e Hilux tienen superficies y zonas de trabajo amplias; Corolla, Yaris y RAV4 requieren el mismo control de preparación aunque cambie el tiempo del proyecto."
    ],
    "parts_heading": "Producto, corrección y garantía",
    "parts_paragraphs": [
      "La cotización distingue descontaminación, nivel de corrección y recubrimiento. No prometemos eliminar todos los defectos: el espesor y condición de la pintura determinan cuánto puede corregirse de forma prudente. PPF o películas existentes se evalúan por separado.",
      "Duración y respaldo dependen del producto identificado, la aplicación y el mantenimiento. Daños por fricción, químicos inadecuados o pintura defectuosa no quedan cubiertos como si fueran fallas del recubrimiento."
    ],
    "bring_heading": "Información para evaluar la pintura",
    "bring_intro": "Indica qué resultado priorizas: corrección visual, facilidad de lavado, brillo o combinación con PPF. Revisamos el vehículo limpio y con iluminación suficiente para separar contaminación, rayones, manchas y defectos de pintura.",
    "bring": ["Modelo, año, color y lugar habitual de parqueo", "Historial de pintura, pulido y recubrimientos", "Método y frecuencia de lavado", "Zonas con rayones, manchas o repintes conocidos"],
    "related": [("Cerámico y cristal líquido: diferencias", "/blog/recubrimiento-ceramico-cristal-liquido-toyota-cartagena/"), ("PPF para Toyota", "/servicios/ppf/"), ("Actualización estética Toyota", "/servicios/actualizacion-estetica/")]
  },
  "proteccion-anticorrosiva": {
    "meta_title": "Anticorrosivo Toyota en Cartagena | Toyo Services",
    "meta_desc": "Protección anticorrosiva para Toyota en Cartagena con inspección de bajos, limpieza, preparación, aplicación controlada y plan de revisiones periódicas.",
    "signs_heading": "Inspeccionar antes de cubrir los bajos",
    "signs_intro": [
      "Una protección responsable comienza identificando corrosión, recubrimientos viejos, barro, humedad, fugas y zonas que deben permanecer libres. Aplicar producto sobre suciedad u óxido activo puede ocultar el avance sin resolver la causa.",
      "Conviene revisar vehículos expuestos con frecuencia a costa, agua, barro o almacenamiento prolongado, además de unidades usadas cuya historia no se conoce. La recomendación depende de materiales, condición y exposición real, no solamente de residir en Cartagena."
    ],
    "signals": ["Óxido superficial, recubrimiento levantado o metal expuesto", "Barro o humedad atrapados en uniones y cavidades accesibles", "Vehículo recién comprado sin historial de bajos", "Uso costero, entrada al agua o viajes por terreno contaminante"],
    "scope_heading": "Limpieza, preparación y zonas de exclusión",
    "process_heading": "Aplicación documentada y revisión periódica",
    "local_heading": "Protección frente al ambiente costero de Cartagena",
    "local_paragraphs": [
      "La humedad y los contaminantes marinos pueden favorecer corrosión cuando permanecen sobre superficies vulnerables. Limpiar y secar correctamente es tan importante como el producto. También verificamos drenajes y evitamos cubrir frenos, escape, sensores, juntas o piezas móviles.",
      "Hilux, Prado y Fortuner pueden tener exposición distinta según viajes y uso; Corolla, Yaris y RAV4 no quedan exentos si circulan o estacionan cerca de ambientes agresivos. Cada inspección se adapta a la arquitectura de los bajos y a modificaciones existentes."
    ],
    "parts_heading": "Límites del tratamiento y garantía",
    "parts_paragraphs": [
      "La protección no reconstruye metal perdido ni sustituye una reparación estructural. Si encontramos corrosión avanzada, fugas o piezas debilitadas, recomendamos resolverlas antes de aplicar. El alcance puede ser localizado o amplio según acceso y estado.",
      "Ningún sistema es permanente. Golpes, elevadores, reparaciones y desgaste pueden abrir zonas que requieren retoque. La garantía se refiere a la aplicación acordada y no cubre corrosión oculta, preexistente o nueva fuera del área tratada."
    ],
    "bring_heading": "Preparación para la inspección",
    "bring_intro": "Informa cualquier contacto reciente con agua, barro o reparación de bajos para programar limpieza y secado adecuados. Una fotografía de la zona ayuda a orientar la cita, pero no reemplaza la inspección elevada ni permite determinar corrosión oculta.",
    "bring": ["Modelo, año y uso habitual", "Exposición a costa, inundación, barro o almacenamiento", "Tratamientos anticorrosivos anteriores", "Golpes, soldaduras, fugas o reparaciones recientes"],
    "related": [("Protección anticorrosiva en ambiente costero", "/blog/proteccion-anticorrosiva-toyota-cartagena/"), ("Mantenimiento general Toyota", "/servicios/mantenimiento-general/"), ("Latonería y pintura Toyota", "/servicios/latoneria-pintura/")]
  },
  "proteccion-interior": {
    "meta_title": "Protección interior Toyota en Cartagena | Toyo Services",
    "meta_desc": "Limpieza y protección interior Toyota en Cartagena para cuero, vinilo, plásticos y tapicería, con prueba de compatibilidad y acabado natural.",
    "signs_heading": "Cada material necesita un método diferente",
    "signs_intro": [
      "Cuero recubierto, vinilo, plástico, textil, microfibra y pantallas no deben limpiarse con el mismo producto. Antes de intervenir distinguimos suciedad, transferencia de color, desgaste, decoloración, grietas y reparaciones previas para no prometer una recuperación que exige restauración.",
      "Volante, pedales, palancas y controles necesitan superficies limpias y sin residuos resbalosos. Buscamos un acabado natural y retiramos exceso; el brillo intenso no se utiliza como prueba de limpieza o protección."
    ],
    "signals": ["Manchas o transferencia de color en asientos claros", "Plástico opaco, pegajoso o tratado con producto incompatible", "Olor o humedad que requiere identificar su origen", "Cuero agrietado o decolorado que necesita restauración separada"],
    "scope_heading": "Limpieza segura y protección por superficie",
    "process_heading": "Prueba, trabajo por secciones y acabado",
    "local_heading": "Interiores expuestos al clima de Cartagena",
    "local_paragraphs": [
      "El calor y la radiación pueden acelerar resequedad y cambios de color, especialmente en vehículos estacionados al exterior. La protección reduce algunos efectos y facilita mantenimiento, pero no detiene por completo el envejecimiento ni sustituye hábitos de ventilación y sombra.",
      "Prado, Fortuner, RAV4, Corolla y otros modelos combinan materiales distintos incluso dentro de una misma versión. Identificamos zonas perforadas, costuras, airbags, sensores y controles para limitar humedad y herramientas donde corresponde."
    ],
    "parts_heading": "Manchas, daños previos y expectativas",
    "parts_paragraphs": [
      "No todas las manchas pueden eliminarse sin alterar el material. Explicamos el resultado probable y realizamos pruebas discretas cuando existe riesgo. Reparación de cuero, cambio de tapicería, tratamiento de inundación o eliminación de olores con causa activa se cotizan como trabajos diferentes.",
      "La protección aplicada necesita limpieza compatible. La garantía no cubre derrames nuevos, transferencia de prendas, abrasión o deterioro preexistente. Documentamos el alcance y damos instrucciones de cuidado razonables."
    ],
    "bring_heading": "Qué informar antes de limpiar",
    "bring_intro": "Evita aplicar productos caseros justo antes de la cita, pues pueden fijar manchas o dificultar la identificación del material. Retira objetos personales para que podamos revisar costuras, rieles, bolsillos y zonas de contacto sin riesgo de extravío. Avísanos si existen mandos flojos, costuras abiertas o componentes eléctricos cerca de una mancha.",
    "bring": ["Origen y antigüedad aproximada de manchas u olores", "Productos aplicados anteriormente", "Reparaciones, tintes o tapicería reemplazada", "Alergias, sensibilidad y zonas que no deben intervenirse"],
    "related": [("Cuidado de cuero y plásticos Toyota", "/blog/proteccion-interior-toyota-cuero-plasticos-cartagena/"), ("Actualización estética Toyota", "/servicios/actualizacion-estetica/"), ("Recubrimiento cerámico Toyota", "/servicios/recubrimiento-ceramico/")]
  }
}

header = '''<header class="site-header"><nav class="nav container"><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg?v=3" alt="" width="60" height="40"><span>TOYO <span>SERVICES</span></span></a><button class="menu" aria-expanded="false" aria-label="Abrir menú">☰</button><div class="nav-links"><a href="/">Inicio</a><a aria-current="page" href="/servicios/">Servicios</a><a href="/modelos/">Modelos</a><a href="/blog/">Guía Toyota</a><a href="/#ubicacion">Área de atención</a></div></nav></header>'''
footer = '''<footer class="footer"><div class="container"><div class="footer-grid"><div><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg?v=3" alt="" width="60" height="40"><span>TOYO <span>SERVICES</span></span></a><p class="muted">Mantenimiento, mecánica, repuestos y acabados premium en Cartagena.</p></div><div><h3>Explora</h3><a href="/servicios/">Servicios</a><a href="/modelos/">Modelos Toyota</a><a href="/blog/">Guía Toyota</a><a href="/nosotros/">Nosotros</a></div><div><h3>Información</h3><a href="/metodologia/">Metodología editorial</a><a href="/preguntas-frecuentes/">Preguntas frecuentes</a><a href="/legal/">Condiciones del servicio</a><a href="/privacidad/">Privacidad y datos</a><a href="/creditos-imagenes/">Créditos visuales</a></div></div><div class="legal"><span>© <span data-year></span> Toyo Services.</span><span>Taller independiente no afiliado a Toyota Motor Corporation.</span></div></div></footer><span class="wa-float" title="WhatsApp disponible próximamente" aria-label="WhatsApp disponible próximamente"><img src="/assets/images/whatsapp-logo.png" width="224" height="225" alt="" aria-hidden="true"></span><script src="/assets/js/main.js?v=18" defer></script>'''

for service in services:
    content=commercial[service["slug"]]
    canonical=f"{BASE}/servicios/{service['slug']}/"
    service_label=service['title'].replace(' en Cartagena','')
    schema={"@context":"https://schema.org","@type":"Service","@id":f"{canonical}#service","name":service["title"],"description":content["meta_desc"],"url":canonical,"image":f"{BASE}/assets/images/{service['image']}","areaServed":{"@type":"City","name":"Cartagena de Indias"},"provider":{"@type":"Organization","@id":f"{BASE}/#business","name":"Toyo Services","url":f"{BASE}/"}}
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in service["faqs"]]}
    breadcrumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":f"{BASE}/"},{"@type":"ListItem","position":2,"name":"Servicios","item":f"{BASE}/servicios/"},{"@type":"ListItem","position":3,"name":service["title"],"item":canonical}]}
    includes=''.join(f'<li>{html.escape(x)}</li>' for x in service['includes'])
    process=''.join(f'<li><span>0{i}</span><p>{html.escape(x)}</p></li>' for i,x in enumerate(service['process'],1))
    faqs=''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in service['faqs'])
    sign_paragraphs=''.join(f'<p>{html.escape(x)}</p>' for x in content['signs_intro'])
    signals=''.join(f'<li>{html.escape(x)}</li>' for x in content['signals'])
    local_paragraphs=''.join(f'<p>{html.escape(x)}</p>' for x in content['local_paragraphs'])
    parts_paragraphs=''.join(f'<p>{html.escape(x)}</p>' for x in content['parts_paragraphs'])
    bring=''.join(f'<li>{html.escape(x)}</li>' for x in content['bring'])
    related=''.join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for label,href in content['related'])
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(content['meta_title'])}</title><meta name="description" content="{html.escape(content['meta_desc'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{html.escape(service['title'])}"><meta property="og:description" content="{html.escape(content['meta_desc'])}"><meta property="og:image" content="{BASE}/assets/images/{service['image']}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/images/favicon.svg?v=3"><link rel="stylesheet" href="/assets/css/styles.css?v=19"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faq,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(breadcrumb,ensure_ascii=False)}</script></head><body>{header}<main><section class="service-detail-hero"><div class="container"><nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / <a href="/servicios/">Servicios</a> / {html.escape(service['title'])}</nav><span class="eyebrow">Servicio especializado</span><h1>{html.escape(service['title'])}</h1><p>{html.escape(service['intro'])}</p><div class="actions"><span class="btn btn-primary btn-disabled" role="button" aria-disabled="true">Cotización por WhatsApp · próximamente</span><a class="btn btn-outline" href="/#ubicacion">Ver área de atención</a></div></div></section><section class="service-detail-body"><div class="container"><img class="service-detail-image" src="/assets/images/{service['image']}" width="1536" height="1024" alt="{html.escape(service['title'])}"><div class="service-detail-grid"><div><span class="eyebrow">Cuándo revisar</span><h2>{html.escape(content['signs_heading'])}</h2>{sign_paragraphs}<ul class="detail-checklist">{signals}</ul></div><div><span class="eyebrow">Qué incluye</span><h2>{html.escape(content['scope_heading'])}</h2><ul class="detail-checklist">{includes}</ul></div><div><span class="eyebrow">Proceso de trabajo</span><h2>{html.escape(content['process_heading'])}</h2><ol class="detail-process">{process}</ol></div></div></div></section><section class="service-detail-body"><div class="container"><div class="service-detail-grid"><div><span class="eyebrow">Contexto local</span><h2>{html.escape(content['local_heading'])}</h2>{local_paragraphs}</div><div><span class="eyebrow">Alcance responsable</span><h2>{html.escape(content['parts_heading'])}</h2>{parts_paragraphs}</div><div><span class="eyebrow">Antes de venir</span><h2>{html.escape(content['bring_heading'])}</h2><p>{html.escape(content['bring_intro'])}</p><ul class="detail-checklist">{bring}</ul></div></div><div class="service-detail-faq"><span class="eyebrow">Información relacionada</span><h2>Guías relacionadas con {html.escape(service_label)}</h2><ul>{related}</ul></div></div></section><section class="faq"><div class="container service-detail-faq"><span class="eyebrow">Preguntas del servicio</span><h2>Preguntas frecuentes sobre {html.escape(service_label)}</h2>{faqs}</div></section><section class="service-quote"><div class="container"><div><span class="eyebrow">Evaluación previa</span><h2>Siguiente paso para {html.escape(service_label)}</h2><p>El alcance final depende del modelo, año, versión, historial y condición comprobada del vehículo.</p></div><div class="actions"><span class="btn btn-primary btn-disabled" role="button" aria-disabled="true">Cotización por WhatsApp · próximamente</span><a class="btn btn-outline" href="/#ubicacion">Ver área de atención</a></div></div></section></main>{footer}</body></html>'''
    page=sync_html_image_dimensions(page, ROOT)
    folder=ROOT/'servicios'/service['slug']; folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(page,encoding='utf-8')

print(f"Generated {len(services)} service pages")
