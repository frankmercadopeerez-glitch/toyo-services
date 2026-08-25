from pathlib import Path
import html, json, math, re

from image_dimensions import sync_html_image_dimensions
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://toyoservicescartagena.com"
BUSINESS_ID = f"{BASE}/#business"


def responsive_attrs(filename, sizes):
    source = ROOT / "assets" / "images" / filename
    with Image.open(source) as image:
        original_width = image.width
    stem = Path(filename).stem
    candidates = [
        f"/assets/images/{stem}-{width}w.webp {width}w"
        for width in (400, 640, 960, 1120, 1440)
        if width < original_width and (source.with_name(f"{stem}-{width}w.webp")).exists()
    ]
    candidates.append(f"/assets/images/{filename} {original_width}w")
    return f'srcset="{", ".join(candidates)}" sizes="{sizes}"'

articles = [
 {
  "slug":"mantenimiento-preventivo-toyota-cartagena","title":"Mantenimiento preventivo Toyota en Cartagena: guía por sistemas","description":"Guía completa de mantenimiento preventivo Toyota en Cartagena: qué revisar por kilometraje, condiciones severas, fluidos, frenos, batería y refrigeración.","category":"Mantenimiento","read":"10 min","image":"blog-maintenance-guide.webp",
  "intro":"Un Toyota puede conservar su confiabilidad durante muchos años cuando el mantenimiento responde al modelo, al kilometraje y al uso real. En Cartagena, el calor, la humedad, los recorridos cortos y el tráfico sostenido justifican una revisión más consciente que limitarse a cambiar aceite.",
  "sections":[
   ("El plan correcto comienza con el vehículo",["El manual del propietario y el historial son la referencia inicial. El año, motor, transmisión y versión determinan especificaciones diferentes; por eso no conviene aplicar una lista universal.","Una inspección profesional organiza lo urgente, lo próximo y lo que puede vigilarse. Así se evita reemplazar piezas sin necesidad y también posponer componentes que sí afectan seguridad o confiabilidad."]),
   ("Qué debe incluir una revisión integral",["Aceite y filtros; niveles y condición de refrigerante, líquido de frenos y fluidos de transmisión; estado de batería, correas, mangueras, luces, limpiaparabrisas y posibles fugas.","En la parte dinámica se revisan frenos, llantas, dirección, amortiguadores, bujes, rodamientos y comportamiento durante una prueba de manejo. Un ruido o vibración necesita ubicación y causa, no una pieza elegida por intuición."]),
   ("Uso severo en Cartagena",["Mucho tiempo en ralentí, trayectos cortos, polvo, carga frecuente y tráfico lento pueden exigir intervalos de inspección más cercanos. El kilometraje por sí solo no refleja las horas que el motor permanece encendido.","La humedad y el ambiente costero también justifican observar conexiones, terminales, bajos y puntos donde puede comenzar corrosión. La prevención se basa en evidencia visible, no en asumir que todo vehículo costero está afectado."]),
   ("Cómo construir un historial útil",["Registra fecha, kilometraje, especificación del fluido, referencia del filtro, piezas instaladas y recomendaciones pendientes. Ese historial facilita diagnósticos futuros y ayuda a conservar el valor del vehículo.","Si acabas de comprar un Toyota usado sin antecedentes claros, conviene establecer una línea base: inspección, escaneo, revisión de fluidos y comprobación de elementos de seguridad antes de planear mejoras estéticas o accesorios."])
  ],"faqs":[("¿Cada cuánto debo llevar mi Toyota?","Depende del modelo, manual y tipo de uso. Deben considerarse kilometraje y tiempo, además de condiciones severas como tráfico, carga o recorridos cortos."),("¿El mantenimiento preventivo evita todas las fallas?","No garantiza que nunca ocurra una avería, pero permite detectar desgaste, fugas y cambios de comportamiento antes de que avancen."),("¿Atienden pickups y SUV Toyota?","Sí. Toyo Services atiende automóviles, pickups y SUV, sujetos a evaluación técnica.")]
 },
 {
  "slug":"mecanica-avanzada-toyota-cartagena","title":"Mecánica avanzada Toyota en Cartagena: diagnóstico antes de reparar","description":"Cómo se diagnostican fallas complejas de motor, transmisión, refrigeración y electrónica Toyota antes de autorizar una reparación.","category":"Mecánica avanzada","read":"11 min","image":"blog-diagnostics-guide.webp",
  "intro":"Una falla compleja no se resuelve cambiando piezas hasta acertar. La mecánica avanzada combina entrevista, inspección, datos electrónicos, mediciones y pruebas mecánicas para demostrar la causa antes de definir una reparación.",
  "sections":[
   ("Síntoma, código y causa no son lo mismo",["El conductor percibe un síntoma: pérdida de potencia, consumo, humo, ruido, temperatura o una luz de advertencia. El escáner puede registrar códigos, pero esos códigos señalan circuitos o condiciones; rara vez ordenan por sí solos qué pieza cambiar.","El diagnóstico relaciona el momento de la falla, datos en vivo, inspección física y pruebas dirigidas. Un código de mezcla, por ejemplo, puede involucrar entrada de aire, combustible, sensor, cableado o condición mecánica."]),
   ("Pruebas que pueden ser necesarias",["Según el caso se revisan presión, compresión, vacío, temperatura, alimentación eléctrica, continuidad, señales de sensores, fugas y parámetros de funcionamiento. No todas las pruebas aplican a todos los vehículos.","En transmisión se analiza nivel y condición del fluido cuando el diseño lo permite, soportes, códigos, temperaturas, respuesta al engranar y comportamiento en ruta. Abrir un conjunto sin diagnóstico previo puede aumentar costo y tiempo."]),
   ("Cuándo detener el vehículo",["Una advertencia roja de presión de aceite, temperatura fuera de rango, pérdida fuerte de tracción, olor intenso a combustible o ruido mecánico severo exige detenerse con seguridad. Continuar puede convertir una falla localizada en daño mayor.","Una luz amarilla fija suele permitir buscar diagnóstico con precaución, pero si parpadea o el motor funciona de forma muy irregular debe reducirse el riesgo y solicitar asistencia."]),
   ("Presupuesto y alcance",["Una reparación profesional separa diagnóstico, repuestos, mano de obra y trabajos adicionales condicionados a lo que se encuentre. El cliente debe saber qué se comprobó y por qué se recomienda cada intervención.","Toyo Services concentra esta metodología en Toyota para reconocer configuraciones, especificaciones y patrones de la marca sin presentar el taller como concesionario oficial."])
  ],"faqs":[("¿Un escaneo diagnostica por completo el vehículo?","No. El escaneo aporta códigos y datos; deben interpretarse y comprobarse con inspecciones o mediciones."),("¿Pueden reparar motor y transmisión?","Se evalúan fallas y reparaciones de motor y transmisión Toyota. El alcance final depende del diagnóstico, disponibilidad de repuestos y condición del conjunto."),("¿Debo seguir conduciendo con el check engine encendido?","Depende de cómo se comporte y si la luz está fija o parpadea. Si hay pérdida fuerte de potencia, ruido, olor o la luz parpadea, evita continuar y solicita revisión.")]
 },
 {
  "slug":"repuestos-toyota-originales-homologados-cartagena","title":"Repuestos Toyota en Cartagena: originales, OEM y homologados","description":"Aprende a elegir repuestos Toyota originales, OEM u homologados según referencia, sistema, uso, garantía y disponibilidad en Cartagena.","category":"Repuestos","read":"10 min","image":"blog-parts-guide.webp",
  "intro":"Elegir un repuesto no consiste solo en encontrar una pieza que físicamente encaje. Referencia, especificación, material, tolerancias y compatibilidad electrónica pueden cambiar entre años, motores y versiones del mismo modelo Toyota.",
  "sections":[
   ("Qué significa cada alternativa",["Un repuesto genuino se comercializa bajo la marca del fabricante del vehículo. OEM suele referirse al fabricante que produce componentes para equipo original, mientras homologado o aftermarket abarca alternativas de distintas calidades.","Estas categorías no permiten concluir automáticamente qué opción conviene. En piezas críticas se priorizan especificación, trazabilidad, reputación del fabricante y compatibilidad confirmada."]),
   ("Identificación correcta",["La placa, VIN, modelo, año, motor, transmisión y referencia de la pieza retirada ayudan a evitar errores. Algunas variantes cambian conectores, diámetros, relaciones, calibraciones o soportes aunque el nombre comercial sea idéntico.","En componentes electrónicos también puede requerirse programación, aprendizaje o calibración después de instalar. El repuesto correcto sin el procedimiento correcto puede generar nuevas advertencias."]),
   ("Dónde no conviene improvisar",["Frenos, dirección, distribución, sensores críticos, soportes, refrigeración y componentes internos del motor merecen especial cuidado. Una diferencia pequeña puede afectar seguridad o durabilidad.","Filtros, fluidos y sellos también deben respetar norma y medida. El color de un líquido no demuestra su especificación y dos filtros parecidos pueden tener válvulas o capacidades distintas."]),
   ("Cotización transparente",["Una propuesta clara indica marca, referencia cuando sea posible, cantidad, mano de obra y alcance de garantía. También debe explicar si la disponibilidad obliga a pedir la pieza o si existe una alternativa técnicamente equivalente.","Toyo Services suministra e instala repuestos para sistemas Toyota y presenta opciones según disponibilidad y evaluación, sin prometer que cualquier pieza sirve para cualquier versión."])
  ],"faqs":[("¿Siempre debo instalar repuesto genuino Toyota?","No existe una respuesta única. Para algunos sistemas es la opción preferible; en otros puede haber fabricantes OEM u homologados confiables. La decisión depende de criticidad y especificación."),("¿Puedo llevar mi propio repuesto?","Debe consultarse antes. Es necesario verificar referencia, estado y compatibilidad, además de definir la responsabilidad sobre la pieza suministrada por el cliente."),("¿Cómo evitan pedir una pieza equivocada?","Se cruza la información del vehículo, referencia, sistema y muestra cuando está disponible antes de confirmar la compra.")]
 },
 {
  "slug":"accesorios-toyota-cartagena-guia","title":"Accesorios Toyota en Cartagena: cómo elegir e instalar sin improvisar","description":"Guía de accesorios Toyota en Cartagena: iluminación, cámaras, multimedia, estribos, barras, protectores y soluciones de carga.","category":"Accesorios","read":"9 min","image":"blog-upgrades-guide.webp",
  "intro":"Un accesorio bien elegido debe resolver una necesidad sin comprometer seguridad, electricidad, visibilidad ni uso cotidiano. La compatibilidad con modelo y versión es tan importante como el diseño.",
  "sections":[
   ("Define primero el objetivo",["Trabajo, viajes, familia, carga, ciudad y uso 4x4 requieren soluciones distintas. Un portaequipaje puede ser útil para viajes pero añadir ruido y altura; una luz auxiliar puede mejorar un entorno privado pero debe instalarse y utilizarse respetando normas.","Antes de comprar se revisan medidas, puntos de anclaje, capacidad, interferencias y mantenimiento futuro."]),
   ("Accesorios eléctricos y multimedia",["Cámaras, sensores, pantallas, cargadores e iluminación deben integrarse con fusibles, calibre de cable y conexiones apropiadas. Cortar cableado o tomar alimentación sin protección puede provocar fallas intermitentes.","En vehículos con redes electrónicas se evita interferir con módulos, airbags o señales. También se comprueba consumo en reposo para proteger la batería."]),
   ("Equipamiento exterior",["Estribos, barras, protectores y soluciones de carga necesitan fijaciones adecuadas y revisión periódica. No deben ocultar luces, placas, sensores ni limitar ángulos de apertura.","El peso añadido y su ubicación modifican comportamiento. En accesorios grandes conviene considerar capacidad de carga, altura y centro de gravedad."]),
   ("Instalación y entrega",["Una instalación limpia incluye ruta protegida de cables, tornillería correcta, ausencia de vibraciones y prueba de todas las funciones. El propietario debe conocer uso, límites y mantenimiento.","Toyo Services evalúa compatibilidad y puede integrar cada elemento con actualizaciones estéticas o modificaciones funcionales."])
  ],"faqs":[("¿Instalan cámaras y pantallas?","Sí, sujeto a compatibilidad con el modelo, versión, sistema eléctrico y equipo seleccionado."),("¿Un accesorio puede afectar la garantía del vehículo?","Depende de la garantía aplicable y de cómo se instale. En vehículos cubiertos conviene revisar sus condiciones antes de modificar sistemas."),("¿Puedo instalar accesorios comprados por internet?","Primero debe verificarse compatibilidad, calidad, elementos incluidos y condiciones de instalación.")]
 },
 {
  "slug":"transformaciones-toyota-hilux-4x4-cartagena","title":"Modificaciones Toyota Hilux y 4x4 en Cartagena: planificación segura","description":"Guía para modificar Toyota Hilux, Fortuner, Prado y otros 4x4: suspensión, protección, carga, iluminación y compatibilidad.","category":"Modificaciones","read":"12 min","image":"blog-modifications-guide.webp",
  "intro":"Modificar un Toyota 4x4 debe comenzar por el objetivo real, no por una lista de piezas. Carretera, trocha, playa y viaje prolongado plantean cargas y prioridades diferentes.",
  "sections":[
   ("Proyecto antes que accesorios sueltos",["Se define objetivo, carga habitual, pasajeros, terreno, presupuesto y reversibilidad. Después se ordenan fases para evitar comprar dos veces o crear incompatibilidades.","Suspensión, llantas, protecciones, iluminación y carga se influyen entre sí. Elevar o añadir peso sin considerar alineación, frenado y geometría puede deteriorar conducción."]),
   ("Suspensión y capacidad",["La altura no es el único criterio. Importan tasa de resorte, recorrido, amortiguación, peso constante y confort. Una configuración demasiado rígida puede comportarse mal cuando el vehículo está vacío.","Después de intervenir se revisan torque, alineación, mangueras, cableado, ángulos y espacio de llanta durante giro y compresión."]),
   ("Protección e iluminación",["Protectores inferiores deben fijarse en puntos capaces y permitir mantenimiento. Barras y defensas no deben interferir con refrigeración, sensores o seguridad.","La iluminación auxiliar requiere circuito independiente protegido, relé cuando aplique, mando accesible y orientación responsable. Potencia sin control puede deslumbrar o sobrecargar el sistema."]),
   ("Legalidad, seguridad y mantenimiento",["Antes de modificar dimensiones, iluminación o elementos externos deben revisarse las reglas aplicables y condiciones de seguro o garantía. Toyo Services no sustituye la homologación exigida por una autoridad.","Una modificación necesita inspecciones posteriores: fijaciones, fugas, desgaste de llantas, alineación y conexiones. El proyecto termina cuando el conjunto funciona de forma coherente."])
  ],"faqs":[("¿Pueden modificar una Hilux, Fortuner o Prado?","Sí. El proyecto se diseña según el objetivo, la versión y las condiciones de uso, sujeto a evaluación técnica."),("¿Toda elevación mejora el 4x4?","No. Puede aumentar despeje, pero también cambia geometría, centro de gravedad y desgaste. Debe plantearse como sistema."),("¿Instalan iluminación auxiliar?","Sí, cuando el equipo es compatible y puede integrarse con protección eléctrica y uso responsable.")]
 },
 {
  "slug":"actualizacion-estetica-toyota-cartagena","title":"Actualización estética Toyota en Cartagena: renovar sin perder identidad","description":"Opciones para actualizar estética exterior e interior Toyota: iluminación, molduras, acabados, restauración e integración visual.","category":"Estética","read":"9 min","image":"blog-aesthetic-guide.webp",
  "intro":"Actualizar la apariencia de un Toyota no significa convertirlo en otro vehículo. Un buen proyecto mejora detalles envejecidos y añade elementos compatibles sin crear una mezcla visual ni afectar funciones.",
  "sections":[
   ("Evaluación del estado actual",["Se revisan pintura, faros, molduras, emblemas, plásticos, tapicería, iluminación y reparaciones previas. Restaurar una pieza original puede dar mejor resultado que cubrirla con un accesorio.","También se identifican sensores, cámaras, airbags y puntos de desmontaje para no afectar sistemas durante el trabajo."]),
   ("Exterior coherente",["Iluminación, parrillas, protectores, barras y detalles deben respetar proporciones y versión. Color, textura y terminación de cada pieza determinan si la actualización parece integrada.","Los faros requieren patrón, orientación y compatibilidad eléctrica. Más intensidad no equivale a mejor iluminación si dispersa o deslumbra."]),
   ("Interior y tecnología",["Pantallas, cámaras, iluminación ambiental y renovación de superficies pueden modernizar el uso diario. Se prioriza ergonomía, visibilidad, controles accesibles y cableado oculto.","No se deben cubrir testigos, salidas de airbag ni zonas de ventilación. Las modificaciones deben permitir mantenimiento posterior."]),
   ("Plan por etapas",["Un proyecto puede dividirse en restauración, funcionalidad y detalles finales. Esto permite evaluar cada resultado y mantener consistencia.","Toyo Services combina actualización estética, accesorios y correcciones mecánicas para que la presentación del vehículo acompañe su condición técnica."])
  ],"faqs":[("¿Pueden actualizar un Toyota antiguo?","Sí, después de evaluar estado, disponibilidad de piezas y compatibilidad. Se priorizan seguridad y funcionamiento."),("¿Cambiar bombillos por LED siempre funciona?","No. Óptica, patrón, disipación, espacio y sistema eléctrico deben ser compatibles."),("¿Hacen proyectos por etapas?","Sí. Se puede priorizar restauración, funcionalidad y acabados según presupuesto y disponibilidad.")]
 },
 {
  "slug":"suspension-toyota-ruidos-vibraciones-cartagena","title":"Suspensión Toyota: ruidos, vibraciones y señales de desgaste","description":"Cómo identificar ruidos y desgaste en suspensión y dirección Toyota: amortiguadores, bujes, terminales, rodamientos y alineación.","category":"Suspensión","read":"10 min","image":"blog-suspension-guide.webp",
  "intro":"Un ruido al pasar un desnivel no identifica por sí solo un amortiguador. La suspensión y dirección contienen piezas que trabajan juntas; holguras, llantas, frenos y fijaciones pueden producir sensaciones parecidas.",
  "sections":[
   ("Cómo describir el síntoma",["Anota si ocurre al girar, frenar, acelerar, pasar baches o circular a cierta velocidad. También importa si es golpe seco, zumbido, crujido o vibración.","La ubicación percibida dentro de la cabina puede engañar. Una prueba controlada y una inspección con carga ayudan a reproducir el problema."]),
   ("Componentes que se revisan",["Amortiguadores, resortes, bases, bujes, rótulas, terminales, brazos, barras estabilizadoras y rodamientos. También llantas, rines, torque y posibles roces.","Una pieza con caucho agrietado no siempre está funcionalmente agotada; se evalúa holgura, movimiento y efecto real antes de reemplazar."]),
   ("Vibración y alineación",["La vibración por velocidad puede relacionarse con balanceo, deformación, rin o rodamiento. Al frenar puede involucrar discos, bujes o montaje. En aceleración se consideran ejes, soportes y transmisión.","Alinear sin corregir holguras puede producir un resultado temporal. Primero se inspecciona, después se corrige y finalmente se alinea cuando corresponde."]),
   ("Después de la reparación",["Se verifican torque, altura, alineación y prueba de manejo. Algunas fijaciones con bujes deben apretarse en posición de trabajo para evitar precarga.","En modificaciones de suspensión, el conjunto debe revisarse con peso, llantas y geometría."])
  ],"faqs":[("¿Todo ruido al pasar un bache es amortiguador?","No. Puede provenir de bujes, bases, barras, frenos, dirección u objetos sueltos. Debe reproducirse e inspeccionarse."),("¿Debo alinear después de cambiar suspensión?","Con frecuencia sí, según el componente intervenido. Primero deben eliminarse holguras."),("¿Una vibración siempre es balanceo?","No. También puede involucrar llantas deformadas, rines, rodamientos, frenos, ejes o soportes.")]
 },
 {
  "slug":"frenos-toyota-mantenimiento-cartagena","title":"Frenos Toyota en Cartagena: mantenimiento, síntomas y diagnóstico","description":"Guía completa de frenos Toyota: pastillas, discos, líquido, vibraciones, ruidos y señales que requieren revisión inmediata.","category":"Frenos","read":"10 min","image":"blog-brakes-guide.webp",
  "intro":"El sistema de frenos debe evaluarse por capacidad, equilibrio y condición, no solo por el grosor de una pastilla. Pedal, líquido, discos, mangueras, sensores y llantas influyen en la respuesta.",
  "sections":[
   ("Señales que no deben ignorarse",["Pedal que se hunde, pérdida de respuesta, desviación fuerte, fuga o advertencia roja requieren detener el vehículo con seguridad. Un chirrido leve puede tener varias causas, pero debe revisarse si persiste.","La vibración al frenar puede relacionarse con variación del disco, montaje, bujes o llanta. Cambiar discos sin comprobar el conjunto puede hacer que el síntoma regrese."]),
   ("Inspección completa",["Se revisan pastillas, discos o campanas, cálipers, guías, mangueras, tuberías, líquido, fugas y freno de estacionamiento. En sistemas electrónicos se consultan advertencias y datos cuando aplica.","El desgaste desigual entre ruedas puede indicar guía trabada, pistón, manguera o condición de montaje."]),
   ("Líquido y procedimiento",["El líquido absorbe humedad con el tiempo y su condición no se juzga solo por color. Se usa la especificación indicada y se purga con método compatible con el sistema.","Contaminar con aceite o producto incorrecto puede dañar sellos. Los envases y herramientas deben mantenerse limpios."]),
   ("Asentamiento y verificación",["Después de reemplazar componentes se comprueba pedal, fugas, torque y funcionamiento. Pastillas y discos nuevos pueden requerir asentamiento progresivo según fabricante.","El conductor recibe indicaciones y debe regresar si aparece pérdida de respuesta, ruido anormal o advertencia."])
  ],"faqs":[("¿Puedo conducir si el pedal se siente esponjoso?","No es recomendable. Puede existir aire, fuga u otra condición que reduzca frenado; requiere revisión inmediata."),("¿Siempre se rectifican los discos?","No. Depende de espesor, variación, daño y especificación. Algunos deben reemplazarse."),("¿Por qué una pastilla se gasta más que la otra?","Puede haber guías, pistón, manguera o montaje con movimiento restringido. Debe corregirse la causa.")]
 },
 {
  "slug":"sistema-refrigeracion-toyota-cartagena","title":"Sistema de refrigeración Toyota en Cartagena: evitar recalentamientos","description":"Cómo cuidar radiador, refrigerante, termostato, bomba, ventiladores y mangueras Toyota frente al calor y tráfico de Cartagena.","category":"Refrigeración","read":"10 min","image":"blog-cooling-guide.webp",
  "intro":"En el clima de Cartagena el sistema de refrigeración trabaja con alta carga térmica, especialmente en tráfico y con aire acondicionado. Una temperatura anormal nunca debe tratarse como algo normal del clima.",
  "sections":[
   ("Cómo circula y controla la temperatura",["Refrigerante, bomba, termostato, radiador, ventiladores, tapa, mangueras y sensores forman un circuito. Una falla en cualquiera puede producir pérdida, presión incorrecta o falta de intercambio térmico.","El tablero puede mostrar la consecuencia tarde. Por eso una inspección preventiva observa niveles, residuos, fugas secas, estado de mangueras y funcionamiento de ventiladores."]),
   ("Refrigerante correcto",["No debe elegirse solo por color. La química y especificación importan para metales, sellos y protección contra corrosión. Mezclar productos incompatibles puede crear depósitos.","Rellenar repetidamente sin localizar la pérdida solo aplaza el problema. Un circuito sellado no debería consumir refrigerante de forma continua."]),
   ("Qué hacer si aumenta la temperatura",["Apaga el aire acondicionado, busca un lugar seguro y detén el motor si la temperatura sigue subiendo o aparece advertencia. No abras la tapa en caliente: el sistema presurizado puede causar quemaduras.","Después de un recalentamiento se debe comprobar causa y posibles consecuencias, no únicamente completar nivel."]),
   ("Prevención en tráfico costero",["Mantén limpio el paso de aire, revisa ventiladores, batería y carga eléctrica, y atiende fugas u olores dulces. El aire acondicionado y la refrigeración comparten flujo frontal en muchos vehículos.","Una prueba de presión o verificación de gases se utiliza cuando los síntomas lo justifican; no es necesaria de forma indiscriminada."])
  ],"faqs":[("¿Puedo usar agua sola?","Solo puede ser una medida de emergencia según la situación. Para operación normal se utiliza refrigerante con especificación y mezcla correctas."),("¿Es normal completar refrigerante cada mes?","No. Una pérdida repetida necesita diagnóstico, aunque no deje charco visible."),("¿Puedo abrir la tapa cuando está caliente?","No. Existe riesgo de expulsión de líquido a presión y quemaduras graves.")]
 },
 {
  "slug":"check-engine-diagnostico-electronico-toyota","title":"Check Engine Toyota: qué significa y cómo se diagnostica","description":"Qué hacer cuando enciende el Check Engine de un Toyota, diferencia entre luz fija y parpadeante, códigos OBD y diagnóstico electrónico.","category":"Diagnóstico","read":"11 min","image":"blog-electronics-guide.webp",
  "intro":"La luz Check Engine informa que un módulo detectó una condición fuera de rango. No nombra una pieza y tampoco debe borrarse sin registrar la información que puede ayudar a encontrar la causa.",
  "sections":[
   ("Luz fija o parpadeante",["Una luz fija con funcionamiento normal suele permitir programar diagnóstico pronto y conducir con moderación. Una luz parpadeante puede indicar una falla capaz de dañar el catalizador; si hay tirones, olor o pérdida de potencia, evita continuar.","Advertencias rojas de aceite o temperatura son diferentes y requieren respuesta inmediata. El manual del vehículo explica cada testigo."]),
   ("Qué aporta el escáner",["Registra códigos, datos congelados del momento de la falla y parámetros en vivo. También permite saber si los monitores están listos y si la falla es actual, pendiente o histórica.","Borrar códigos elimina pistas y reinicia monitores; no repara la causa. Desconectar batería también puede perder adaptaciones o información."]),
   ("Proceso de diagnóstico",["Se confirma la queja, inspeccionan conexiones y mangueras, consultan datos y se diseñan pruebas. Dependiendo del código se mide alimentación, tierra, señal, presión, fugas o condición mecánica.","La pieza mencionada en la descripción del código puede estar reportando correctamente un problema originado en otro lugar."]),
   ("Después de corregir",["Se borran códigos cuando corresponde, se prueba el vehículo y se verifica que los parámetros vuelvan a rango. Algunos monitores necesitan ciclos de conducción para completar.","Si la luz regresa, se conserva el contexto y se continúa el diagnóstico en lugar de repetir la misma pieza."])
  ],"faqs":[("¿Puedo borrar el Check Engine y seguir?","Borrarlo no corrige la causa y puede eliminar información útil. Primero conviene registrar códigos y datos."),("¿El código dice exactamente qué pieza cambiar?","Normalmente no. Indica un circuito o condición que debe comprobarse."),("¿Una tapa de combustible puede encender la luz?","En algunos sistemas evaporativos sí, pero no debe asumirse sin consultar el código y revisar el sistema.")]
 }
]

articles += json.loads((ROOT / "scripts" / "seo_articles.json").read_text(encoding="utf-8"))
articles += [article for article in json.loads((ROOT / "scripts" / "additional_services_articles.json").read_text(encoding="utf-8")) if not article.get("disabled")]
articles += json.loads((ROOT / "scripts" / "legacy_articles.json").read_text(encoding="utf-8"))

# Cada URL responde a una intención informativa y entrega la conversión a una
# única página comercial. Esto evita que varias guías compitan entre sí por la
# misma consulta y elimina los CTA genéricos hacia /servicios/.
EDITORIAL = {
 "mantenimiento-preventivo-toyota-cartagena": (
  "Mantenimiento preventivo Toyota en Cartagena",
  "Guía de mantenimiento preventivo Toyota en Cartagena: sistemas que conviene revisar según modelo, historial, uso, tiempo y kilometraje.",
  "plan preventivo por sistemas", "/servicios/mantenimiento-general/", "mantenimiento general"
 ),
 "mecanica-avanzada-toyota-cartagena": (
  "Mecánica Toyota en Cartagena: diagnóstico avanzado",
  "Conoce cómo se diagnostican fallas complejas de motor, transmisión, refrigeración y electrónica Toyota antes de autorizar una reparación.",
  "diagnóstico de fallas complejas", "/servicios/mecanica-avanzada/", "mecánica avanzada"
 ),
 "repuestos-toyota-originales-homologados-cartagena": (
  "Repuestos Toyota en Cartagena: cómo elegirlos",
  "Aprende a elegir repuestos Toyota en Cartagena por referencia, sistema, compatibilidad, trazabilidad y alcance de instalación y garantía.",
  "selección y compatibilidad de repuestos", "/servicios/repuestos/", "repuestos Toyota"
 ),
 "accesorios-toyota-cartagena-guia": (
  "Accesorios Toyota: instalación segura en Cartagena",
  "Guía para elegir e instalar accesorios Toyota en Cartagena sin afectar seguridad, cableado, sensores, capacidad de carga ni mantenimiento.",
  "instalación segura de accesorios", "/servicios/modificaciones/", "modificaciones"
 ),
 "transformaciones-toyota-hilux-4x4-cartagena": (
  "Modificaciones Toyota Hilux y 4x4 en Cartagena",
  "Cómo planear modificaciones para Toyota Hilux y otros 4x4 considerando suspensión, carga, ruedas, iluminación, seguridad y mantenimiento.",
  "planificación de modificaciones 4x4", "/servicios/modificaciones/", "modificaciones"
 ),
 "actualizacion-estetica-toyota-cartagena": (
  "Cómo renovar la estética de tu Toyota en Cartagena",
  "Guía para evaluar una actualización estética Toyota en Cartagena: estado inicial, compatibilidad, integración visual, instalación y cuidados.",
  "renovación estética compatible", "/servicios/actualizacion-estetica/", "actualización estética"
 ),
 "suspension-toyota-ruidos-vibraciones-cartagena": (
  "Diagnóstico de ruidos en suspensión Toyota",
  "Aprende a diferenciar ruidos y vibraciones de suspensión Toyota y qué revisar en amortiguadores, bujes, rótulas, dirección, llantas y rines.",
  "diagnóstico general de ruidos de suspensión", "/servicios/frenos-suspension/", "frenos y suspensión"
 ),
 "frenos-toyota-mantenimiento-cartagena": (
  "Frenos Toyota en Cartagena: señales y revisión",
  "Identifica ruidos, vibraciones, cambios de pedal y testigos de los frenos Toyota, y conoce qué debe comprobarse antes de cambiar componentes.",
  "señales y diagnóstico del sistema de frenos", "/servicios/frenos-suspension/", "frenos y suspensión"
 ),
 "sistema-refrigeracion-toyota-cartagena": (
  "Refrigeración Toyota: cómo evitar recalentamientos",
  "Guía del sistema de refrigeración Toyota en Cartagena: refrigerante, radiador, ventiladores, bomba, termostato, mangueras y señales de alerta.",
  "prevención de recalentamiento", "/servicios/motor-refrigeracion/", "motor y refrigeración"
 ),
 "check-engine-diagnostico-electronico-toyota": (
  "Check Engine Toyota: diagnóstico paso a paso",
  "Qué hacer cuando enciende el Check Engine de un Toyota y cómo se relacionan códigos, datos en vivo, inspección y pruebas antes de reparar.",
  "interpretación y diagnóstico del Check Engine", "/servicios/diagnostico-electronico/", "diagnóstico electrónico"
 ),
 "cambio-aceite-toyota-cartagena": (
  "Qué incluye un cambio de aceite Toyota",
  "Descubre qué debe incluir un cambio de aceite Toyota en Cartagena: confirmación del lubricante y filtro, inspecciones y registro del servicio.",
  "alcance comercial del cambio de aceite", "/servicios/aceite-filtros/", "aceite y filtros"
 ),
 "aceite-recomendado-toyota-hilux-diesel": (
  "Aceite Toyota Hilux diésel: norma y viscosidad",
  "Guía para elegir aceite de una Toyota Hilux diésel según motor, año, manual, viscosidad, norma, filtro y condiciones reales de utilización.",
  "selección de aceite para Hilux diésel", "/servicios/aceite-filtros/", "aceite y filtros"
 ),
 "mantenimiento-toyota-prado-cartagena": (
  "Checklist de mantenimiento para Toyota Prado",
  "Checklist de mantenimiento Toyota Prado en Cartagena: motor, refrigeración, transmisión, sistema 4x4, frenos, suspensión, ruedas e historial.",
  "mantenimiento integral de Toyota Prado", "/servicios/mantenimiento-general/", "mantenimiento general"
 ),
 "rines-toyota-prado-medidas-recomendadas": (
  "Rines Toyota Prado: medidas, offset y carga",
  "Qué revisar al elegir rines para Toyota Prado: diámetro, ancho, offset, PCD, centro, capacidad de carga, llanta, confort y espacio disponible.",
  "compatibilidad de rines para Toyota Prado", "/servicios/modificaciones/", "modificaciones"
 ),
 "suspension-toyota-prado-cartagena": (
  "Suspensión Toyota Prado: qué revisar por versión",
  "Guía de suspensión Toyota Prado por versión: configuración, síntomas, amortiguadores, bujes, dirección, rodamientos, ruedas y alineación.",
  "diagnóstico de suspensión para Toyota Prado", "/servicios/frenos-suspension/", "frenos y suspensión"
 ),
 "llantas-toyota-prado-medida-presion": (
  "Llantas Toyota Prado: medida, carga y presión",
  "Cómo elegir llantas para Toyota Prado por medida, índice de carga, presión indicada, uso, desgaste y compatibilidad con la versión y el rin.",
  "selección de llantas para Toyota Prado", "/servicios/modificaciones/", "modificaciones"
 ),
 "aire-acondicionado-toyota-cartagena": (
  "Aire acondicionado Toyota en Cartagena",
  "Diagnóstico del aire acondicionado Toyota en Cartagena: poco frío, fugas, compresor, ventiladores, filtro de cabina y carga por especificación.",
  "diagnóstico del aire acondicionado", "/servicios/mecanica-avanzada/", "mecánica avanzada"
 ),
 "bateria-toyota-senales-cambio-cartagena": (
  "Batería Toyota: señales y pruebas en clima cálido",
  "Reconoce señales de batería débil en un Toyota y las pruebas de arranque, carga, conexiones y consumo necesarias antes de reemplazarla.",
  "diagnóstico de batería y sistema de carga", "/servicios/diagnostico-electronico/", "diagnóstico electrónico"
 ),
 "latoneria-pintura-toyota-cartagena": (
  "Proceso de latonería y pintura para Toyota",
  "Guía del proceso de latonería y pintura para Toyota en Cartagena: evaluación del daño, preparación, igualación de color, armado y control final.",
  "proceso de reparación de carrocería y pintura", "/servicios/latoneria-pintura/", "latonería y pintura"
 ),
 "mantenimiento-toyota-fortuner-cartagena": (
  "Mantenimiento Toyota Fortuner: viaje, carga y 4x4",
  "Guía de mantenimiento Toyota Fortuner en Cartagena para viaje y carga: motor, refrigeración, frenos, suspensión, transmisión, 4x4 y ruedas.",
  "mantenimiento integral de Toyota Fortuner", "/servicios/mantenimiento-general/", "mantenimiento general"
 ),
 "ppf-toyota-cartagena-proteccion-pintura": (
  "PPF para Toyota en Cartagena: guía de protección",
  "Guía de PPF para Toyota en Cartagena: límites de protección, zonas de cobertura, preparación de pintura, instalación, curado y mantenimiento.",
  "protección de pintura con PPF", "/servicios/ppf/", "PPF"
 ),
 "recubrimiento-ceramico-cristal-liquido-toyota-cartagena": (
  "Recubrimiento cerámico Toyota: beneficios reales",
  "Qué aporta un recubrimiento cerámico para Toyota, cómo se prepara la pintura, qué no protege y qué cuidados influyen en su duración.",
  "beneficios y límites del recubrimiento cerámico", "/servicios/recubrimiento-ceramico/", "recubrimiento cerámico"
 ),
 "proteccion-anticorrosiva-toyota-cartagena": (
  "Cómo proteger los bajos de tu Toyota en Cartagena",
  "Conoce cómo se evalúa y aplica protección anticorrosiva a un Toyota en Cartagena: inspección de bajos, preparación, zonas críticas y seguimiento.",
  "protección de bajos frente al ambiente costero", "/servicios/proteccion-anticorrosiva/", "protección anticorrosiva"
 ),
 "proteccion-interior-toyota-cuero-plasticos-cartagena": (
  "Cuidado interior Toyota en clima cálido",
  "Cómo limpiar y proteger cuero, plásticos, vinilo y tapicería Toyota en Cartagena sin dejar brillo excesivo, residuos ni superficies resbalosas.",
  "cuidado de cuero, plásticos y tapicería", "/servicios/proteccion-interior/", "protección interior"
 ),
 "toyota-consume-aceite-humo-azul": (
  "Toyota consume aceite o echa humo azul: causas",
  "Qué revisar si tu Toyota consume aceite o expulsa humo azul: medición, fugas, PCV, turbo, sellos, compresión y posible reparación del motor.",
  "causas del consumo de aceite y humo azul", "/servicios/reparacion-motor/", "reparación de motor"
 ),
 "toyota-no-enciende-causas": (
  "Toyota no enciende: causas y diagnóstico",
  "Qué revisar cuando un Toyota no enciende: batería, terminales, arranque, alternador, inmovilizador, combustible, encendido y diagnóstico.",
  "diagnóstico de un Toyota que no enciende", "/servicios/reparacion-motor/", "reparación de motor"
 ),
 "reparar-o-cambiar-motor-toyota": (
  "¿Reparar o cambiar el motor Toyota? Guía práctica",
  "Cómo decidir entre reparar, rectificar, reconstruir o cambiar un motor Toyota según diagnóstico, mediciones, repuestos, trazabilidad y garantía.",
  "decisión entre reparar o reemplazar el motor", "/servicios/reparacion-motor/", "reparación de motor"
 ),
 "cada-cuanto-cambiar-aceite-toyota": (
  "Cuándo cambiar el aceite de un Toyota",
  "Aprende cuándo revisar y cambiar el aceite de un Toyota según el manual, el tiempo, el kilometraje, el uso y las condiciones de conducción.",
  "momento correcto para cambiar el aceite", "/servicios/aceite-filtros/", "aceite y filtros"
 ),
 "senales-transmision-toyota": (
  "Transmisión Toyota: señales que requieren revisión",
  "Reconoce tirones, demoras, fugas, ruidos y alertas de una transmisión Toyota, y entiende por qué el diagnóstico debe preceder cualquier reparación.",
  "señales tempranas de problemas de transmisión", "/servicios/transmision/", "transmisión"
 ),
 "mantenimiento-toyota-cartagena": (
  "Mantenimiento Toyota en el clima de Cartagena",
  "Guía para cuidar un Toyota en Cartagena frente a calor, humedad, tráfico y recorridos cortos, sin reemplazar el programa específico del fabricante.",
  "mantenimiento condicionado por el clima de Cartagena", "/servicios/mantenimiento-general/", "mantenimiento general"
 )
}

# Los temas cercanos comparten servicio comercial, pero no la misma pregunta.
# Estas aperturas dejan explícito qué resuelve cada guía y qué deja a las demás.
INTRO_OVERRIDES = {
 "actualizacion-estetica-toyota-cartagena": (
  "Esta guía ayuda a decidir si conviene restaurar, reemplazar o integrar cada elemento antes de iniciar una actualización estética. "
  "El foco está en evaluar compatibilidad, coherencia visual y cuidados posteriores, no en presentar un catálogo de piezas."
 ),
 "cambio-aceite-toyota-cartagena": (
  "Esta guía no fija un intervalo universal: explica qué debe incluir un servicio de cambio de aceite, cómo se confirma el lubricante y el filtro, "
  "y qué inspecciones y registros conviene recibir al terminar. Para decidir cuándo hacerlo, consulta la guía específica sobre intervalos."
 ),
 "cada-cuanto-cambiar-aceite-toyota": (
  "Aquí la pregunta es cuándo revisar o cambiar el aceite. La respuesta parte del manual, el tiempo, el kilometraje y las condiciones de uso; "
  "no describe el alcance comercial del servicio ni sustituye la especificación de una versión concreta."
 ),
 "aceite-recomendado-toyota-hilux-diesel": (
  "Esta guía se concentra en seleccionar aceite para una Hilux diésel mediante motor, año, manual, norma y viscosidad. "
  "No propone una viscosidad única para todas las Hilux ni define por sí sola el intervalo de cambio."
 ),
 "rines-toyota-prado-medidas-recomendadas": (
  "El foco de esta guía es la geometría y capacidad del rin: diámetro, ancho, offset, PCD, centro y carga. "
  "La presión y el índice de la llanta se verifican aparte con la información aplicable a la versión."
 ),
 "llantas-toyota-prado-medida-presion": (
  "Esta guía trata la llanta: medida, índice de carga y velocidad, presión indicada, desgaste y uso. "
  "Cambiar el rin exige además revisar offset, ancho, centro y espacio disponible en la Prado."
 ),
 "suspension-toyota-ruidos-vibraciones-cartagena": (
  "Esta guía organiza el diagnóstico por síntoma para distintos Toyota: cuándo aparece el ruido, cómo se siente la vibración y qué conjuntos deben inspeccionarse. "
  "No presupone que el amortiguador sea la causa ni sustituye una revisión específica de la versión."
 ),
 "suspension-toyota-prado-cartagena": (
  "Aquí el análisis se limita a Toyota Prado y a las diferencias que pueden existir entre generaciones, versiones, equipamiento y modificaciones previas. "
  "El objetivo es identificar primero la configuración instalada y después relacionarla con el síntoma."
 ),
 "mantenimiento-toyota-prado-cartagena": (
  "Esta guía funciona como checklist integral para una Toyota Prado: historial, motor, transmisión, sistema 4x4, frenos, suspensión y ruedas. "
  "Las guías de rines, llantas y suspensión profundizan por separado en compatibilidad y síntomas."
 ),
 "mantenimiento-toyota-fortuner-cartagena": (
  "Esta guía prioriza el uso habitual de una Toyota Fortuner con pasajeros, equipaje, carretera o sistema 4x4. "
  "El plan se adapta a su versión y motorización; no copia automáticamente el checklist de una Prado ni un intervalo genérico para SUV."
 ),
 "latoneria-pintura-toyota-cartagena": (
  "Esta guía explica las etapas de una reparación de carrocería: evaluación, conformado, preparación, color, armado y control final. "
  "Su propósito es ayudar a revisar el alcance y el acabado esperado antes de autorizar el trabajo."
 ),
 "proteccion-anticorrosiva-toyota-cartagena": (
  "Esta guía explica cómo inspeccionar los bajos y decidir dónde una protección anticorrosiva puede aportar valor. "
  "No asume que todo vehículo costero necesita la misma aplicación ni que el recubrimiento sustituye la limpieza y las revisiones periódicas."
 ),
}

SOURCE_UPDATE_SLUGS = {
    "accesorios-toyota-cartagena-guia",
    "actualizacion-estetica-toyota-cartagena",
    "aire-acondicionado-toyota-cartagena",
    "bateria-toyota-senales-cambio-cartagena",
    "check-engine-diagnostico-electronico-toyota",
    "frenos-toyota-mantenimiento-cartagena",
    "latoneria-pintura-toyota-cartagena",
    "mecanica-avanzada-toyota-cartagena",
    "ppf-toyota-cartagena-proteccion-pintura",
    "proteccion-anticorrosiva-toyota-cartagena",
    "proteccion-interior-toyota-cuero-plasticos-cartagena",
    "recubrimiento-ceramico-cristal-liquido-toyota-cartagena",
    "repuestos-toyota-originales-homologados-cartagena",
    "senales-transmision-toyota",
    "sistema-refrigeracion-toyota-cartagena",
    "suspension-toyota-ruidos-vibraciones-cartagena",
}

NEW_ENGINE_ARTICLES = {
    "toyota-consume-aceite-humo-azul",
    "toyota-no-enciende-causas",
    "reparar-o-cambiar-motor-toyota",
}

for article in articles:
    title, description, intent, service_path, service_label = EDITORIAL[article["slug"]]
    article.update({
        "title": title,
        "description": description,
        "intent": intent,
        "service_path": service_path,
        "service_label": service_label,
        "dateModified": (
            "2026-08-25"
            if article["slug"] in SOURCE_UPDATE_SLUGS
            else "2026-08-20"
            if article["slug"] in NEW_ENGINE_ARTICLES
            else "2026-08-13"
        ),
    })
    if article["slug"] in NEW_ENGINE_ARTICLES:
        article["datePublished"] = "2026-08-20"
    if article["slug"] in INTRO_OVERRIDES:
        article["intro"] = INTRO_OVERRIDES[article["slug"]]

if len(articles) != len(EDITORIAL) or len({article["slug"] for article in articles}) != len(articles):
    raise ValueError("Cada artículo debe tener un slug único y una asignación editorial")
if len({article["intent"] for article in articles}) != len(articles):
    raise ValueError("Cada artículo debe responder a una intención informativa única")
for article in articles:
    if len(article["title"]) > 60:
        raise ValueError(f"Título demasiado largo: {article['slug']}")
    if not 125 <= len(article["description"]) <= 155:
        raise ValueError(f"Meta description fuera de rango: {article['slug']}")
    service_page = ROOT / article["service_path"].strip("/") / "index.html"
    if not service_page.exists():
        raise FileNotFoundError(f"No existe el servicio propietario de {article['slug']}: {service_page}")

extras = {
 "Mantenimiento":[
  ("Cómo priorizar cuando hay varias recomendaciones",["Primero se atienden condiciones de seguridad, fugas activas, temperatura, lubricación y fallas que pueden causar daños mayores. Después se organizan elementos de confiabilidad y, finalmente, trabajos de confort o apariencia. Esta jerarquía permite usar el presupuesto con criterio.","No todo hallazgo exige reemplazo inmediato. Una recomendación debe indicar condición, riesgo, margen de uso razonable y forma de seguimiento. Fotografías, medidas o una explicación visible ayudan al propietario a decidir sin presión."]),
  ("Preparación para una revisión eficiente",["Lleva el historial disponible y explica cuándo aparece cada síntoma, si ocurre en frío o caliente, con aire acondicionado, carga o determinada velocidad. Evita limpiar una fuga justo antes de la visita porque puede ocultar evidencia útil.","Retira objetos pesados o sueltos si se evaluarán ruidos y confirma el nivel habitual de combustible. Al recibir el vehículo, revisa qué se realizó, qué quedó pendiente y cuándo debe comprobarse de nuevo."])
 ],
 "Mecánica avanzada":[
  ("Errores que encarecen una reparación",["Cambiar sensores por el nombre de un código, mezclar fluidos, borrar información antes de escanear o continuar conduciendo con temperatura o presión anormales puede aumentar el alcance. También dificulta el diagnóstico instalar piezas usadas sin referencia clara.","Una segunda opinión es útil cuando la propuesta no explica pruebas ni causa. Lo importante no es acumular opiniones sino comparar evidencia: valores medidos, condición encontrada y relación lógica con el síntoma."]),
  ("Cómo se confirma que la reparación funcionó",["La verificación puede incluir arranque en frío, temperatura de operación, prueba de ruta, datos en vivo, ausencia de fugas y repetición de la condición que generaba la falla. Un código borrado no es prueba suficiente.","Algunas reparaciones requieren reaprendizajes o ciclos de conducción. El cliente debe saber qué comportamiento puede ser temporal y qué señal indicaría detenerse o regresar al taller."])
 ],
 "Repuestos":[
  ("Piezas económicas y costo total",["El precio de compra es solo una parte. Deben sumarse mano de obra, fluidos, empaques, calibración y riesgo de repetir el trabajo. Una pieza barata que dura poco puede costar más que una alternativa trazable.","Tampoco la opción más costosa es automáticamente mejor. La comparación responsable usa especificación, fabricante, garantía, disponibilidad y criticidad del sistema."]),
  ("Qué conservar después del servicio",["Guarda factura, marca, referencia y empaque cuando sea útil para garantía. Solicita conocer la pieza retirada, salvo que deba devolverse como núcleo o por condición comercial previamente explicada.","Tras instalar, observa fugas, ruidos, advertencias y comportamiento. Algunos componentes necesitan asentamiento, torque de comprobación o inspección posterior."])
 ],
 "Accesorios":[
  ("Compatibilidad con seguridad y mantenimiento",["No deben bloquearse puntos de elevación, acceso a filtros, rueda de repuesto, ganchos o sensores. Un accesorio que obliga a desmontajes excesivos en cada servicio aumenta tiempo y riesgo de daño.","En el habitáculo se protegen zonas de airbag, visibilidad y movimiento de pedales. Cables y módulos deben quedar sujetos, identificables y lejos de humedad o calor."]),
  ("Preguntas antes de comprar",["¿Qué problema resuelve? ¿Es compatible con la versión? ¿Qué incluye el kit? ¿Requiere perforar, programar o cortar cableado? ¿Aumenta altura, peso o consumo eléctrico? Estas respuestas evitan compras impulsivas.","También conviene definir acabado, garantía y disponibilidad de repuestos del accesorio. Una instalación profesional no corrige un producto de baja calidad o sin soporte."])
 ],
 "Modificaciones":[
  ("Orden recomendado del proyecto",["Comienza con mantenimiento y corrección de fallas. Después define carga y suspensión, continúa con protección y ruedas, y deja electrónica, accesorios y estética para una fase compatible con lo anterior.","Este orden puede cambiar según el objetivo, pero evita instalar iluminación antes de dimensionar la energía o elegir suspensión sin conocer el peso final."]),
  ("Prueba y documentación",["Registra referencias, alturas, alineación, torque y conexiones. Una prueba debe incluir maniobras lentas, giro completo, frenado y condiciones normales de carretera antes de exigir el vehículo.","Tras los primeros recorridos se inspeccionan fijaciones, roces, ruidos y asentamiento. Las modificaciones necesitan mantenimiento propio además del plan Toyota original."])
 ],
 "Estética":[
  ("Evitar que una modificación se vea añadida",["La clave está en proporción, temperatura de color, textura y repetición de acabados. Demasiados elementos compiten entre sí; pocos cambios bien integrados suelen producir un resultado más duradero.","Antes de pedir una pieza conviene visualizar tamaño y posición, además de comprobar si existen variantes para la misma carrocería."]),
  ("Cuidado después de actualizar",["Cada material necesita limpieza compatible. Productos agresivos pueden manchar plásticos, atacar adhesivos o deteriorar recubrimientos. El instalador debe explicar curado y mantenimiento.","Revisa fijaciones y sellos después de lluvia o carretera. Si una luz genera condensación, parpadeo o advertencia, debe corregirse en lugar de ocultarse."])
 ],
 "Suspensión":[
  ("Llantas y presión también importan",["Una presión incorrecta cambia confort, desgaste y respuesta. Medidas no equivalentes o llantas con deformación pueden simular problemas de suspensión y afectar calibraciones.","Se revisa desgaste en bordes, escalonamiento, fecha, reparación previa y compatibilidad. Rotar no corrige una pieza con holgura ni una geometría fuera de rango."]),
  ("Ruidos después de una intervención",["Una fijación sin torque, resorte mal asentado, manguera en tensión o protector rozando puede aparecer después de reparar. Documentar el momento exacto facilita localizarlo.","La revisión posterior no debe limitarse al componente nuevo: confirma relación con los elementos vecinos y que el vehículo conserva altura y movimiento adecuados."])
 ],
 "Frenos":[
  ("Hábitos que afectan duración",["Descensos prolongados con el freno aplicado, sobrecarga y conducción con un cáliper restringido elevan temperatura. En carretera se usa una marcha apropiada sin exceder límites del motor y se mantiene distancia.","Lavar componentes muy calientes o contaminar superficies con productos puede afectar respuesta. Cualquier cambio tras una intervención merece inspección."]),
  ("ABS y ayudas electrónicas",["ABS, control de estabilidad y asistencia dependen de sensores, rodamientos, llantas y alimentación eléctrica. Una advertencia no siempre significa que el freno hidráulico desapareció, pero indica que una ayuda puede estar deshabilitada.","El diagnóstico consulta códigos y señales de rueda, además de cableado y condición mecánica. Cambiar un sensor sin comprobar su señal puede no resolver."])
 ],
 "Refrigeración":[
  ("Relación con el aire acondicionado",["El condensador del aire acondicionado suele estar delante del radiador y ambos dependen del flujo de aire. Suciedad externa, ventiladores débiles o presión incorrecta pueden manifestarse más en tráfico.","No se recarga refrigerante de aire sin diagnosticar. Tampoco se culpa al aire acondicionado de una temperatura alta sin revisar el sistema de motor."]),
  ("Después de cambiar un componente",["Se purga aire con el procedimiento correspondiente, comprueba calefacción cuando aplica, funcionamiento de ventiladores, presión y ausencia de fugas. Una bolsa de aire puede causar lecturas o circulación irregulares.","Al enfriar se verifica nivel nuevamente. El propietario debe observar temperatura y piso donde estaciona durante los primeros recorridos."])
 ],
 "Diagnóstico":[
  ("Códigos históricos y fallas intermitentes",["Un código guardado puede provenir de batería baja, desconexión o evento antiguo. Se compara con fecha, kilometraje, datos congelados y frecuencia antes de atribuirle el síntoma actual.","Las fallas intermitentes requieren capturar condiciones. Anotar temperatura, lluvia, combustible, velocidad y accesorios encendidos puede revelar un patrón."]),
  ("Batería y alimentación eléctrica",["Voltaje bajo puede producir múltiples advertencias y comunicaciones erráticas. Se comprueba batería, arranque, carga, tierras y terminales antes de condenar módulos.","Después de sustituir batería algunos modelos requieren reinicios o aprendizajes. Mantener energía con métodos inadecuados también puede crear riesgos."])
 ]
}

# Refuerzos propios para los clústeres con mayor riesgo de solapamiento. Las
# guías por modelo no reutilizan los dos apartados genéricos de su categoría.
ARTICLE_EXTRAS = {
 "cambio-aceite-toyota-cartagena": [
  ("Qué pedir en una cotización", ["La propuesta debe identificar el vehículo, la especificación y cantidad de lubricante, la referencia del filtro y las comprobaciones incluidas. Así se comparan alcances equivalentes y no solo un precio aislado.", "Si durante el servicio aparecen fuga, rosca dañada o un filtro incorrecto instalado previamente, el trabajo adicional se explica y autoriza por separado."]),
  ("Después de recibir el vehículo", ["Comprueba que no existan testigos ni fugas y conserva el registro del producto y kilometraje. El nivel se revisa con el procedimiento indicado para ese motor, porque el momento y la superficie de medición influyen.", "Una etiqueta de próximo servicio ayuda como recordatorio, pero no reemplaza el programa del manual ni la vigilancia periódica del nivel."]),
  ("Recepción y trazabilidad", ["Antes de abrir un envase se confirma la identificación del Toyota y se registra lo autorizado. La factura debe permitir reconocer producto, filtro y cantidad; una frase genérica como cambio de aceite dificulta reconstruir el historial.", "Si el vehículo tiene protector inferior, blindaje o una modificación que cambia el acceso, se revisa su montaje al retirar y volver a instalar. Cualquier fijación ausente se informa en lugar de ocultarla."]),
  ("Lubricante usado y limpieza del trabajo", ["El aceite retirado se contiene sin contaminar suelo, agua ni otros residuos y se entrega al canal de manejo correspondiente. Esta etapa forma parte de un servicio ordenado aunque no sea visible al conducir.", "La zona del filtro y del tapón se deja limpia para que una fuga posterior pueda identificarse. Limpiar no significa ocultar evidencia previa: las manchas encontradas se documentan antes de intervenir."])
 ],
 "aceite-recomendado-toyota-hilux-diesel": [
  ("Trabajo, carga y ralentí", ["Una Hilux utilizada con carga, polvo, recorridos cortos o mucho ralentí puede trabajar en condiciones distintas a una camioneta de carretera. El manual define cómo tratar esos escenarios; no se corrigen eligiendo por costumbre un aceite más grueso.", "Registrar horas de uso cuando el vehículo las muestra, consumo y reposiciones ayuda a interpretar mejor el mantenimiento que mirar únicamente el odómetro."]),
  ("Motor y sistema de emisiones", ["La ficha técnica confirma que existen distintas motorizaciones y configuraciones Hilux. En versiones diésel con sistemas de control de emisiones, el lubricante debe ser compatible con la especificación correspondiente.", "Si el nivel aumenta, aparecen regeneraciones anormales, humo o pérdida de potencia, no se prolonga el intervalo ni se cambia de producto a ciegas: se diagnostica la condición."])
 ],
 "mantenimiento-toyota-prado-cartagena": [
  ("Historial de una Prado usada", ["En una unidad sin registros se comprueban fluidos, fugas, códigos, ruedas y funcionamiento 4x4 antes de asumir que una pieza fue atendida. También se documentan accesorios, elevación, blindaje o cambios de rin que alteren carga y geometría.", "La línea base permite separar mantenimiento pendiente de una falla actual y evita reemplazar de nuevo componentes que sí tienen evidencia reciente."]),
  ("Peso, ruedas y uso real", ["Pasajeros, equipaje, remolque y terreno cambian el esfuerzo sobre frenos, llantas y suspensión. Se revisan capacidad y presión aplicables a la versión, sin copiar valores de otra generación.", "Antes de un viaje se corrigen vibraciones, desgaste irregular y pérdidas de fluidos con tiempo suficiente para probar la reparación."])
 ],
 "mantenimiento-toyota-fortuner-cartagena": [
  ("Uso familiar, carretera y carga", ["Una Fortuner que circula con pasajeros y equipaje exige atención a llantas, frenos y temperatura. El plan parte de la capacidad y configuración de la versión, no de una pauta genérica para cualquier SUV.", "Antes de viajar se inspecciona con anticipación para poder corregir hallazgos y confirmar el resultado en condiciones normales."]),
  ("Versiones diésel y gasolina", ["La gama Fortuner incluye configuraciones de motor diferentes; por eso cambian combustible, fluidos y componentes de emisiones. La ficha técnica y el manual de la unidad determinan qué aplica.", "En una versión diésel, pérdida de potencia, humo o alertas del sistema de emisiones necesitan diagnóstico; no se resuelven automáticamente con un cambio de aceite o filtro."])
 ],
 "suspension-toyota-prado-cartagena": [
  ("Configuración y equipamiento de la versión", ["La suspensión puede variar entre generaciones y versiones, e incluir componentes o controles distintos. Antes de cotizar se identifica el sistema instalado y cualquier modificación previa.", "Un repuesto compatible por apariencia puede tener tasa, recorrido o conexión diferente. Se verifica referencia y función antes del montaje."]),
  ("Confort frente a control", ["Una Prado puede sentirse rígida por presión, tipo de llanta o carga, mientras un rebote excesivo puede involucrar amortiguación. La prueba busca separar percepción de una holgura o componente fuera de condición.", "Después de reparar se comprueban altura, torque, giro, frenado y ausencia de roces; la alineación es el cierre del proceso cuando corresponde, no el diagnóstico inicial."])
 ],
 "mantenimiento-toyota-cartagena": [
  ("Aire acondicionado y tráfico", ["Si el aire enfría en carretera pero pierde capacidad detenido, se revisan caudal, condensador, ventiladores y estado del circuito. Añadir refrigerante sin medir no demuestra ni corrige la causa.", "El sistema de aire y la refrigeración del motor comparten la necesidad de un flujo de aire correcto, pero cada uno requiere pruebas propias."]),
  ("Después de playa, lluvia intensa o inundación", ["La exposición ocasional no significa que exista daño, pero justifica observar bajos, conectores, frenos, rodamientos y acumulaciones. El lavado se hace sin dirigir presión hacia componentes sensibles.", "Si el agua alcanzó zonas no previstas por el fabricante, se prioriza una inspección antes de encender o continuar conduciendo; el alcance depende del nivel y tiempo de exposición."])
 ]
}

CATEGORY_EXTRA_OWNERS = {
    "mantenimiento-preventivo-toyota-cartagena",
    "mecanica-avanzada-toyota-cartagena",
    "repuestos-toyota-originales-homologados-cartagena",
    "accesorios-toyota-cartagena-guia",
    "transformaciones-toyota-hilux-4x4-cartagena",
    "actualizacion-estetica-toyota-cartagena",
    "suspension-toyota-ruidos-vibraciones-cartagena",
    "frenos-toyota-mantenimiento-cartagena",
    "sistema-refrigeracion-toyota-cartagena",
    "check-engine-diagnostico-electronico-toyota",
}

TOYOTA_MAINTENANCE = (
    "Mantenimiento planeado Toyota Colombia",
    "https://www.toyota.com.co/postventa/mantenimiento/planeado",
)
TOYOTA_MANUALS = (
    "Manuales y garantías Toyota por modelo y año",
    "https://www.toyota.com/espanol/owners/warranty-owners-manuals/",
)
TOYOTA_BATTERY = (
    "Toyota: señales para revisar o reemplazar la batería",
    "https://www.toyota.com/espanol/car-tips/replace-car-battery/",
)
TOYOTA_OWNER_RESOURCES = (
    "Recursos oficiales Toyota para propietarios y manuales",
    "https://www.toyota.com/owners/",
)
TOYOTA_GENUINE_PARTS = (
    "Toyota: repuestos y accesorios por vehículo y VIN",
    "https://www.toyota.com/espanol/owners/genuine-parts/",
)
TOYOTA_COLLISION = (
    "Toyota: criterios para reparación de colisiones",
    "https://www.toyota.com/owners/collision-center/",
)
THREE_M_PPF = (
    "Referencia técnica de película PPF automotriz (3M)",
    "https://multimedia.3m.com/mws/media/2159829O/product-bulletin-ppf-series-100-en-we.pdf",
)
THREE_M_CERAMIC = (
    "Referencia técnica de recubrimiento cerámico automotriz (3M)",
    "https://multimedia.3m.com/mws/media/1990834O/3m-ceramic-coating-tds-39901.pdf",
)
THREE_M_CORROSION = (
    "Procedimientos de protección anticorrosiva automotriz (3M)",
    "https://multimedia.3m.com/mws/media/2428117O/3m-cavity-wax-plus-08852-tds-ceemea.pdf",
)
PRADO_PAGE = (
    "Land Cruiser Prado: información y materiales oficiales",
    "https://www.toyota.com.co/vehiculos/camionetas/land-cruiser-prado",
)
FORTUNER_PAGE = (
    "Toyota Fortuner: información y materiales oficiales",
    "https://www.toyota.com.co/vehiculos/camionetas/fortuner",
)
HILUX_SPECS = (
    "Toyota Hilux: información y materiales oficiales",
    "https://www.toyota.com.co/vehiculo/hilux-3",
)

DEFAULT_SOURCES_BY_SERVICE = {
    "/servicios/mantenimiento-general/": [TOYOTA_MAINTENANCE, TOYOTA_MANUALS],
    "/servicios/mecanica-avanzada/": [TOYOTA_OWNER_RESOURCES, TOYOTA_MANUALS],
    "/servicios/repuestos/": [TOYOTA_GENUINE_PARTS, TOYOTA_MANUALS],
    "/servicios/modificaciones/": [TOYOTA_GENUINE_PARTS, TOYOTA_MANUALS],
    "/servicios/actualizacion-estetica/": [TOYOTA_GENUINE_PARTS, TOYOTA_MANUALS],
    "/servicios/frenos-suspension/": [TOYOTA_MANUALS, TOYOTA_GENUINE_PARTS],
    "/servicios/motor-refrigeracion/": [TOYOTA_MANUALS, TOYOTA_MAINTENANCE],
    "/servicios/diagnostico-electronico/": [TOYOTA_MANUALS, TOYOTA_OWNER_RESOURCES],
    "/servicios/aceite-filtros/": [TOYOTA_MANUALS, TOYOTA_MAINTENANCE],
    "/servicios/latoneria-pintura/": [TOYOTA_COLLISION, TOYOTA_GENUINE_PARTS],
    "/servicios/ppf/": [THREE_M_PPF],
    "/servicios/recubrimiento-ceramico/": [THREE_M_CERAMIC],
    "/servicios/proteccion-anticorrosiva/": [THREE_M_CORROSION],
    "/servicios/proteccion-interior/": [TOYOTA_MANUALS],
    "/servicios/transmision/": [TOYOTA_MANUALS, TOYOTA_GENUINE_PARTS],
    "/servicios/reparacion-motor/": [TOYOTA_MANUALS, TOYOTA_GENUINE_PARTS],
}

planned_maintenance_sources = {
    "mantenimiento-preventivo-toyota-cartagena",
    "cambio-aceite-toyota-cartagena",
    "cada-cuanto-cambiar-aceite-toyota",
    "mantenimiento-toyota-cartagena",
}

SOURCE_NOTES_BY_SERVICE = {
    "/servicios/mantenimiento-general/": "Cruza el programa de mantenimiento con el manual, el historial y la configuración exacta del vehículo antes de fijar prioridades.",
    "/servicios/mecanica-avanzada/": "Solicita que cada conclusión esté vinculada con síntomas reproducidos, códigos registrados, inspecciones o valores medidos; una guía general no reemplaza esas pruebas.",
    "/servicios/repuestos/": "Confirma VIN, referencia, fabricante, compatibilidad, garantía y procedimiento de instalación antes de comprar o autorizar una pieza.",
    "/servicios/modificaciones/": "Verifica medidas, capacidad, puntos de montaje, interferencias, requisitos legales y mantenimiento del componente exacto antes de instalarlo.",
    "/servicios/actualizacion-estetica/": "Compara material, acabado, compatibilidad con sensores y cuidados del elemento exacto; una fotografía de catálogo no demuestra ajuste ni durabilidad.",
    "/servicios/frenos-suspension/": "La referencia y el procedimiento dependen de versión, configuración y condición. Pide inspección de holguras, ruedas y fijaciones antes de reemplazar componentes.",
    "/servicios/motor-refrigeracion/": "Comprueba especificación del refrigerante, diseño del circuito y valores de prueba aplicables al motor; color y apariencia no identifican por sí solos un fluido.",
    "/servicios/diagnostico-electronico/": "Conserva códigos, datos congelados y síntomas antes de borrar información. La documentación del sistema y las mediciones deben respaldar el diagnóstico.",
    "/servicios/aceite-filtros/": "Confirma en el manual de la unidad la norma, viscosidad, capacidad, filtro e intervalo aplicables al motor y a sus condiciones de uso.",
    "/servicios/latoneria-pintura/": "Antes de autorizar, revisa alcance del desarme, reparación, preparación, sistema de pintura, método de igualación y criterios de entrega.",
    "/servicios/ppf/": "Solicita ficha técnica del PPF, cobertura acordada, preparación, garantía, curado y cuidados del producto exacto que se instalará.",
    "/servicios/recubrimiento-ceramico/": "Solicita ficha técnica del recubrimiento, preparación, número de capas cuando aplique, curado, mantenimiento y exclusiones de garantía.",
    "/servicios/proteccion-anticorrosiva/": "Verifica producto, zonas incluidas, preparación, compatibilidad con cauchos y drenajes, método de aplicación y programa de inspección posterior.",
    "/servicios/proteccion-interior/": "Identifica primero cuero, textil, vinilo o plástico y comprueba ficha técnica, compatibilidad, acabado y cuidados del producto que se utilizará.",
    "/servicios/transmision/": "La especificación del fluido, el nivel, la temperatura de comprobación y el procedimiento cambian por transmisión; confirma la documentación de la unidad.",
    "/servicios/reparacion-motor/": "Solicita valores medidos, piezas y mecanizados incluidos, referencias, trabajos externos, pruebas posteriores y condiciones de garantía antes de autorizar una reparación interna.",
}

for article in articles:
    sources = list(DEFAULT_SOURCES_BY_SERVICE[article["service_path"]])
    if article["slug"] in planned_maintenance_sources:
        sources = [TOYOTA_MAINTENANCE, TOYOTA_MANUALS]
    if "prado" in article["slug"]:
        sources = [PRADO_PAGE, TOYOTA_MAINTENANCE]
    elif "fortuner" in article["slug"]:
        sources = [FORTUNER_PAGE, TOYOTA_MAINTENANCE]
    elif "hilux" in article["slug"]:
        sources = [HILUX_SPECS, TOYOTA_MAINTENANCE]
    if article["slug"] == "toyota-consume-aceite-humo-azul":
        sources = [TOYOTA_MANUALS, TOYOTA_MAINTENANCE]
    elif article["slug"] == "toyota-no-enciende-causas":
        sources = [TOYOTA_BATTERY, TOYOTA_MANUALS]
    elif article["slug"] == "reparar-o-cambiar-motor-toyota":
        sources = [TOYOTA_MANUALS]
    article["sources"] = sources
    article["source_note"] = SOURCE_NOTES_BY_SERVICE[article["service_path"]]

RELATED_OVERRIDES = {
    "mantenimiento-preventivo-toyota-cartagena": ["bateria-toyota-senales-cambio-cartagena", "sistema-refrigeracion-toyota-cartagena", "frenos-toyota-mantenimiento-cartagena"],
    "accesorios-toyota-cartagena-guia": ["actualizacion-estetica-toyota-cartagena", "proteccion-interior-toyota-cuero-plasticos-cartagena", "transformaciones-toyota-hilux-4x4-cartagena"],
    "actualizacion-estetica-toyota-cartagena": ["latoneria-pintura-toyota-cartagena", "proteccion-interior-toyota-cuero-plasticos-cartagena", "accesorios-toyota-cartagena-guia"],
    "latoneria-pintura-toyota-cartagena": ["actualizacion-estetica-toyota-cartagena", "ppf-toyota-cartagena-proteccion-pintura", "recubrimiento-ceramico-cristal-liquido-toyota-cartagena"],
    "ppf-toyota-cartagena-proteccion-pintura": ["recubrimiento-ceramico-cristal-liquido-toyota-cartagena", "proteccion-anticorrosiva-toyota-cartagena", "latoneria-pintura-toyota-cartagena"],
    "recubrimiento-ceramico-cristal-liquido-toyota-cartagena": ["ppf-toyota-cartagena-proteccion-pintura", "proteccion-interior-toyota-cuero-plasticos-cartagena", "actualizacion-estetica-toyota-cartagena"],
    "proteccion-anticorrosiva-toyota-cartagena": ["ppf-toyota-cartagena-proteccion-pintura", "mantenimiento-toyota-cartagena", "recubrimiento-ceramico-cristal-liquido-toyota-cartagena"],
    "proteccion-interior-toyota-cuero-plasticos-cartagena": ["actualizacion-estetica-toyota-cartagena", "recubrimiento-ceramico-cristal-liquido-toyota-cartagena", "accesorios-toyota-cartagena-guia"],
    "cambio-aceite-toyota-cartagena": ["aceite-recomendado-toyota-hilux-diesel", "mantenimiento-preventivo-toyota-cartagena", "repuestos-toyota-originales-homologados-cartagena"],
    "cada-cuanto-cambiar-aceite-toyota": ["mantenimiento-toyota-cartagena", "mantenimiento-preventivo-toyota-cartagena", "aceite-recomendado-toyota-hilux-diesel"],
    "aceite-recomendado-toyota-hilux-diesel": ["cambio-aceite-toyota-cartagena", "cada-cuanto-cambiar-aceite-toyota", "transformaciones-toyota-hilux-4x4-cartagena"],
    "mantenimiento-toyota-prado-cartagena": ["suspension-toyota-prado-cartagena", "rines-toyota-prado-medidas-recomendadas", "llantas-toyota-prado-medida-presion"],
    "suspension-toyota-prado-cartagena": ["suspension-toyota-ruidos-vibraciones-cartagena", "mantenimiento-toyota-prado-cartagena", "llantas-toyota-prado-medida-presion"],
    "rines-toyota-prado-medidas-recomendadas": ["llantas-toyota-prado-medida-presion", "mantenimiento-toyota-prado-cartagena", "suspension-toyota-prado-cartagena"],
    "llantas-toyota-prado-medida-presion": ["rines-toyota-prado-medidas-recomendadas", "suspension-toyota-prado-cartagena", "mantenimiento-toyota-prado-cartagena"],
    "mantenimiento-toyota-fortuner-cartagena": ["mantenimiento-preventivo-toyota-cartagena", "senales-transmision-toyota", "mantenimiento-toyota-cartagena"],
    "mecanica-avanzada-toyota-cartagena": ["check-engine-diagnostico-electronico-toyota", "senales-transmision-toyota", "aire-acondicionado-toyota-cartagena"],
    "aire-acondicionado-toyota-cartagena": ["mecanica-avanzada-toyota-cartagena", "sistema-refrigeracion-toyota-cartagena", "mantenimiento-toyota-cartagena"],
    "suspension-toyota-ruidos-vibraciones-cartagena": ["suspension-toyota-prado-cartagena", "frenos-toyota-mantenimiento-cartagena", "llantas-toyota-prado-medida-presion"],
    "senales-transmision-toyota": ["mecanica-avanzada-toyota-cartagena", "check-engine-diagnostico-electronico-toyota", "mantenimiento-toyota-fortuner-cartagena"],
    "mantenimiento-toyota-cartagena": ["mantenimiento-preventivo-toyota-cartagena", "aire-acondicionado-toyota-cartagena", "proteccion-anticorrosiva-toyota-cartagena"],
    "toyota-consume-aceite-humo-azul": ["reparar-o-cambiar-motor-toyota", "sistema-refrigeracion-toyota-cartagena", "cambio-aceite-toyota-cartagena"],
    "toyota-no-enciende-causas": ["check-engine-diagnostico-electronico-toyota", "bateria-toyota-senales-cambio-cartagena", "reparar-o-cambiar-motor-toyota"],
    "reparar-o-cambiar-motor-toyota": ["toyota-consume-aceite-humo-azul", "mecanica-avanzada-toyota-cartagena", "repuestos-toyota-originales-homologados-cartagena"],
}

CONCLUSIONS_BY_SERVICE = {
    "/servicios/mantenimiento-general/": (
        "Convierte la revisión en un plan",
        "El resultado útil no es una lista de piezas, sino un orden de trabajo basado en seguridad, condición e historial. Documenta lo realizado y deja fecha o criterio de seguimiento para cada pendiente."
    ),
    "/servicios/mecanica-avanzada/": (
        "Exige evidencia antes de reparar",
        "Una hipótesis debe convertirse en una causa comprobada mediante inspección, datos o mediciones. Autoriza el alcance cuando puedas relacionar el síntoma, la prueba y la intervención propuesta."
    ),
    "/servicios/repuestos/": (
        "Compatibilidad antes que apariencia",
        "Una pieza parecida no necesariamente corresponde a la versión. Confirma identificación, referencia, especificación y condiciones de instalación antes de comparar únicamente precio o disponibilidad."
    ),
    "/servicios/modificaciones/": (
        "Piensa en el vehículo como un conjunto",
        "Rines, llantas, suspensión, carga, iluminación y accesorios se afectan entre sí. Define el objetivo, comprueba compatibilidades y revisa el resultado completo después de instalar."
    ),
    "/servicios/actualizacion-estetica/": (
        "Primero el estado; después el diseño",
        "Corregir daños, fijaciones y superficies envejecidas crea una base mejor para cualquier actualización. Elige elementos que respeten funciones, proporciones y mantenimiento futuro."
    ),
    "/servicios/frenos-suspension/": (
        "Un síntoma no identifica la pieza",
        "Ruido, vibración, deriva o rebote pueden involucrar más de un conjunto. Reproduce la condición, inspecciona holguras y ruedas, y confirma el resultado después de intervenir."
    ),
    "/servicios/motor-refrigeracion/": (
        "La temperatura no admite improvisación",
        "Si existe recalentamiento, pérdida de refrigerante o una alerta, detén el diagnóstico por su causa y evita limitarte a rellenar. Una prueba posterior debe confirmar presión, circulación y control térmico."
    ),
    "/servicios/diagnostico-electronico/": (
        "El código orienta; las pruebas confirman",
        "Conserva la información de la falla y relaciona códigos con datos, cableado, alimentación y condición mecánica. Borrar una advertencia no demuestra que el sistema haya quedado corregido."
    ),
    "/servicios/aceite-filtros/": (
        "Manual, versión y uso real",
        "La decisión correcta combina especificación e intervalo aplicables con el historial y la utilización del vehículo. Registra producto, filtro, fecha y kilometraje para que el siguiente servicio parta de información verificable."
    ),
    "/servicios/latoneria-pintura/": (
        "El acabado empieza en la preparación",
        "Alineación, reparación del sustrato, preparación y control de color importan tanto como el brillo final. Revisa también armado, sellos, luces y piezas cercanas antes de recibir el vehículo."
    ),
    "/servicios/ppf/": (
        "Cobertura y preparación definen el resultado",
        "Acordar zonas, condición previa de la pintura, bordes y cuidados evita expectativas equivocadas. El PPF reduce ciertos daños de uso, pero no sustituye mantenimiento ni corrige defectos debajo de la película."
    ),
    "/servicios/recubrimiento-ceramico/": (
        "Brillo no equivale a blindaje",
        "El recubrimiento facilita ciertos cuidados de la superficie, pero su desempeño depende de preparación, aplicación y mantenimiento. Compara la promesa con la ficha técnica del producto elegido."
    ),
    "/servicios/proteccion-anticorrosiva/": (
        "La inspección define dónde intervenir",
        "Limpieza, acceso a drenajes y condición de los bajos determinan el alcance. Después de aplicar, programa revisiones para detectar golpes, desprendimientos o zonas que necesiten corrección."
    ),
    "/servicios/proteccion-interior/": (
        "Cada material necesita un tratamiento distinto",
        "Cuero, textil, vinilo y plástico no se limpian ni protegen de la misma forma. Prueba compatibilidad, evita residuos y conserva instrucciones para el cuidado cotidiano."
    ),
    "/servicios/transmision/": (
        "Diagnostica antes de abrir o cambiar fluido",
        "Registra cuándo aparece el síntoma y comprueba nivel, condición, temperatura, códigos y soportes según el diseño. El alcance debe responder a la causa encontrada, no solo a la sensación al conducir."
    ),
    "/servicios/reparacion-motor/": (
        "Mide antes de desmontar y compara alcances completos",
        "La decisión responsable relaciona el síntoma con pruebas, tolerancias y causa raíz. Compara piezas, mecanizados, armado, verificaciones y garantía, no únicamente el precio inicial."
    ),
}

def article_sections(article):
    category_extras = extras.get(article["category"], []) if article["slug"] in CATEGORY_EXTRA_OWNERS else []
    return article["sections"] + ARTICLE_EXTRAS.get(article["slug"], category_extras)

def article_related(article):
    lookup = {candidate["slug"]: candidate for candidate in articles}
    candidates = [lookup[slug] for slug in RELATED_OVERRIDES.get(article["slug"], []) if slug in lookup and slug != article["slug"]]
    candidates += [candidate for candidate in articles if candidate["slug"] != article["slug"] and candidate["service_path"] == article["service_path"] and candidate not in candidates]
    candidates += [candidate for candidate in articles if candidate["slug"] != article["slug"] and candidate["category"] == article["category"] and candidate not in candidates]
    candidates += [candidate for candidate in articles if candidate["slug"] != article["slug"] and candidate not in candidates]
    return candidates[:3]

def reading_minutes(article):
    conclusion_title, conclusion_text = CONCLUSIONS_BY_SERVICE[article["service_path"]]
    parts = [article["title"], article["intro"], conclusion_title, conclusion_text, article["source_note"]]
    for section_title, paragraphs in article_sections(article):
        parts.append(section_title)
        parts.extend(paragraphs)
    for question, answer in article["faqs"]:
        parts.extend((question, answer))
    word_count = len(re.findall(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", " ".join(parts), flags=re.UNICODE))
    return max(3, math.ceil(word_count / 200))


def spanish_date(value):
    year, month, day = value.split("-")
    months = {
        "01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
        "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
        "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre",
    }
    return f"{int(day)} de {months[month]} de {year}"

for article in articles:
    article["read_minutes"] = reading_minutes(article)
    article["read"] = f'{article["read_minutes"]} min'

required_related_inbound = {
    "actualizacion-estetica-toyota-cartagena",
    "aire-acondicionado-toyota-cartagena",
    "latoneria-pintura-toyota-cartagena",
    "proteccion-anticorrosiva-toyota-cartagena",
    "proteccion-interior-toyota-cuero-plasticos-cartagena",
}
related_inbound = {
    target: sum(target in {candidate["slug"] for candidate in article_related(article)} for article in articles)
    for target in required_related_inbound
}
if any(count == 0 for count in related_inbound.values()):
    raise ValueError(f"Guías sin enlaces relacionados entrantes: {related_inbound}")

header = '''<header class="site-header"><nav class="nav container"><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg" alt="" width="60" height="40" /><span>TOYO <span>SERVICES</span></span></a><button class="menu" aria-expanded="false" aria-label="Abrir menú">☰</button><div class="nav-links"><a href="/">Inicio</a><a href="/servicios/">Servicios</a><a href="/modelos/">Modelos</a><a aria-current="page" href="/blog/">Guía Toyota</a><a href="/#ubicacion">Área de atención</a></div></nav></header>'''
footer = '''<footer class="footer"><div class="container"><div class="footer-grid"><div><a class="brand" href="/"><img class="brand-logo" src="/assets/images/toyo-services-logo.svg" alt="" width="60" height="40" /><span>TOYO <span>SERVICES</span></span></a><p class="muted">Mantenimiento, mecánica, repuestos y acabados premium en Cartagena.</p><p class="footer-contact"><a href="tel:+573018638164">+57 301 863 8164</a> · <a href="https://wa.me/573018638164?text=Hola%20Toyo%20Services.%20Quiero%20informaci%C3%B3n%20para%20mi%20Toyota." target="_blank" rel="noopener">WhatsApp</a></p></div><div><h3>Explora</h3><a href="/servicios/">Servicios</a><a href="/modelos/">Modelos Toyota</a><a href="/blog/">Guía Toyota</a><a href="/nosotros/">Nosotros</a></div><div><h3>Información</h3><a href="/metodologia/">Metodología editorial</a><a href="/preguntas-frecuentes/">Preguntas frecuentes</a><a href="/legal/">Condiciones del servicio</a><a href="/privacidad/">Privacidad y datos</a><a href="/creditos-imagenes/">Créditos visuales</a></div></div><div class="legal"><span>© <span data-year></span> Toyo Services.</span><span>Taller independiente no afiliado a Toyota Motor Corporation.</span></div></div></footer><a class="wa-float" href="https://wa.me/573018638164?text=Hola%20Toyo%20Services.%20Quiero%20informaci%C3%B3n%20para%20mi%20Toyota." target="_blank" rel="noopener" title="Escribir a Toyo Services por WhatsApp" aria-label="Escribir a Toyo Services por WhatsApp"><img src="/assets/images/whatsapp-logo.png" width="96" height="96" alt="" aria-hidden="true"></a><script src="/assets/js/main.js?v=19" defer></script>'''

def article_page(a):
    canonical=f"{BASE}/blog/{a['slug']}/"
    faq_schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a["faqs"]]}
    posting={"@context":"https://schema.org","@type":"BlogPosting","headline":a["title"],"description":a["description"],"datePublished":a.get("datePublished","2026-08-09"),"dateModified":a["dateModified"],"timeRequired":f'PT{a["read_minutes"]}M',"inLanguage":"es-CO","articleSection":a["category"],"keywords":a["intent"],"author":{"@type":"Organization","@id":BUSINESS_ID,"name":"Toyo Services","url":f"{BASE}/nosotros/"},"publisher":{"@type":"Organization","@id":BUSINESS_ID,"name":"Toyo Services","url":BASE},"about":{"@type":"Service","@id":f"{BASE}{a['service_path']}#service","name":a["service_label"],"url":f"{BASE}{a['service_path']}"},"image":f"{BASE}/assets/images/{a['image']}","mainEntityOfPage":{"@type":"WebPage","@id":canonical}}
    if a["sources"]:
        posting["citation"] = [url for _, url in a["sources"]]
    breadcrumb_schema={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":f"{BASE}/"},{"@type":"ListItem","position":2,"name":"Guía Toyota","item":f"{BASE}/blog/"},{"@type":"ListItem","position":3,"name":a["title"],"item":canonical}]}
    all_sections=article_sections(a)
    toc=''.join(f'<li><a href="#s{i}">{html.escape(title)}</a></li>' for i,(title,_) in enumerate(all_sections,1))
    body=''
    for i,(title,paragraphs) in enumerate(all_sections,1):
        body+=f'<h2 id="s{i}">{html.escape(title)}</h2>'+''.join(f'<p>{html.escape(p)}</p>' for p in paragraphs)
        if i == 1:
            body += (
                '<aside class="article-service-context"><strong>Del diagnóstico a una solución concreta.</strong> '
                f'Si necesitas evaluar este punto en tu vehículo, conoce el <a href="{a["service_path"]}">'
                f'servicio de {html.escape(a["service_label"])}</a> para Toyota en Cartagena.</aside>'
            )
    faqs=''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(ans)}</p></details>' for q,ans in a['faqs'])
    related=''.join(f'<li><a href="/blog/{x["slug"]}/">{html.escape(x["title"])}</a></li>' for x in article_related(a))
    source_links=''.join(f'<li><a href="{html.escape(url)}" rel="noopener">{html.escape(label)}</a></li>' for label,url in a['sources'])
    source_heading="Fuentes y documentos para verificar" if source_links else "Qué verificar antes del servicio"
    source_section=(
        f'<section class="article-sources"><h2>{source_heading}</h2>'
        f'<p>{html.escape(a["source_note"])}</p>'
        + (f'<ul>{source_links}</ul>' if source_links else '')
        + '</section>'
    )
    conclusion_heading, conclusion_text = CONCLUSIONS_BY_SERVICE[a["service_path"]]
    cta_label=f'Conocer el servicio de {a["service_label"]}'
    eyebrow = a["category"] if a["category"].endswith("Toyota") else f'{a["category"]} Toyota'
    image_attrs = responsive_attrs(a["image"], "(max-width: 720px) calc(100vw - 40px), 920px")
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(a['title'])}</title><meta name="description" content="{html.escape(a['description'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Toyo Services"><meta property="og:title" content="{html.escape(a['title'])}"><meta property="og:description" content="{html.escape(a['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/images/{a['image']}"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#080a0d"><link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="48x48"><link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="/site.webmanifest"><link rel="stylesheet" href="/assets/css/styles.min.css?v=22"><script type="application/ld+json">{json.dumps(posting,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(faq_schema,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(breadcrumb_schema,ensure_ascii=False)}</script></head><body>{header}<main class="article"><nav class="breadcrumb" aria-label="Migas de pan"><a href="/">Inicio</a> / <a href="/blog/">Guía Toyota</a> / {html.escape(a['category'])}</nav><span class="eyebrow">{html.escape(eyebrow)}</span><h1>{html.escape(a['title'])}</h1><p class="article-byline">Contenido elaborado por <a href="/nosotros/">Toyo Services</a> · <time datetime="2026-08-13">actualizado el 13 de agosto de 2026</time></p><p class="lead">{html.escape(a['intro'])}</p><img src="/assets/images/{a['image']}" {image_attrs} width="1200" height="800" alt="{html.escape(a['title'])}" fetchpriority="high"><aside class="article-toc"><strong>En esta guía</strong><ol>{toc}</ol></aside>{body}<h2>{html.escape(conclusion_heading)}</h2><p>{html.escape(conclusion_text)}</p>{source_section}<section class="faq article-faq"><h2>Preguntas frecuentes</h2>{faqs}</section><aside class="related-guides"><h2>Guías relacionadas</h2><ul>{related}</ul></aside><div class="actions"><a class="btn btn-primary" href="{a['service_path']}">{html.escape(cta_label)}</a><a class="btn btn-outline" href="/#ubicacion">Ver área de atención</a></div></main>{footer}</body></html>'''

for article in articles:
    folder=ROOT/'blog'/article['slug']; folder.mkdir(parents=True,exist_ok=True)
    page=article_page(article).replace('/assets/images/toyo-services-logo.svg','/assets/images/toyo-services-logo.svg?v=3')
    page=page.replace('</a> · <time datetime=', '</a> · <a href="/metodologia/">Metodología editorial</a> · <time datetime=', 1)
    if article["dateModified"] != "2026-08-13":
        page=page.replace(
            'datetime="2026-08-13">actualizado el 13 de agosto de 2026',
            f'datetime="{article["dateModified"]}">actualizado el {spanish_date(article["dateModified"])}',
        )
    page=page.replace(f'<span class="eyebrow">{html.escape(article["category"])} Toyota Toyota</span>', f'<span class="eyebrow">{html.escape(article["category"])} Toyota</span>')
    page=sync_html_image_dimensions(page, ROOT)
    (folder/'index.html').write_text(page,encoding='utf-8')

cards=[]
for a in articles:
    cards.append((a['slug'],a['title'],a['category'],a['read'],a['image'],a['description']))
card_html=''.join(f'''<article class="card blog-card"><a class="blog-card-content" href="/blog/{slug}/"><img loading="lazy" src="/assets/images/{img}" {responsive_attrs(img, "(max-width: 700px) calc(100vw - 40px), (max-width: 1100px) 46vw, 360px")} width="800" height="500" alt="{html.escape(title)}"><div class="blog-body"><span class="tag">{html.escape(cat)} · {read}</span><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p><span class="card-link" aria-hidden="true">Leer artículo →</span></div></a></article>''' for slug,title,cat,read,img,desc in cards)
item_schema={"@context":"https://schema.org","@type":"CollectionPage","@id":f"{BASE}/blog/#collection","name":"Guía Toyota de Toyo Services","url":f"{BASE}/blog/","publisher":{"@id":BUSINESS_ID},"hasPart":[{"@type":"BlogPosting","headline":title,"url":f"{BASE}/blog/{slug}/"} for slug,title,*_ in cards]}
blog_breadcrumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":f"{BASE}/"},{"@type":"ListItem","position":2,"name":"Guía Toyota","item":f"{BASE}/blog/"}]}
blog=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guía Toyota en Cartagena | Toyo Services</title><meta name="description" content="Guías de Toyo Services sobre mantenimiento, diagnóstico, repuestos, aceite, Prado, Fortuner, Hilux y cuidado Toyota en Cartagena."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}/blog/"><meta property="og:type" content="website"><meta property="og:locale" content="es_CO"><meta property="og:site_name" content="Toyo Services"><meta property="og:title" content="Guía Toyota en Cartagena | Toyo Services"><meta property="og:description" content="Información útil sobre mantenimiento, diagnóstico, repuestos y cuidado Toyota."><meta property="og:url" content="{BASE}/blog/"><meta property="og:image" content="{BASE}/assets/images/blog-maintenance-guide.webp"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#080a0d"><link rel="icon" href="/favicon.ico" type="image/x-icon" sizes="48x48"><link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png" sizes="180x180"><link rel="manifest" href="/site.webmanifest"><link rel="stylesheet" href="/assets/css/styles.min.css?v=22"><script type="application/ld+json">{json.dumps(item_schema,ensure_ascii=False)}</script><script type="application/ld+json">{json.dumps(blog_breadcrumb,ensure_ascii=False)}</script></head><body>{header}<main><header class="page-hero blog-hero"><div class="container"><div class="breadcrumb"><a href="/">Inicio</a> / Guía Toyota</div><span class="eyebrow">Conocimiento especializado</span><h1>Guías para cuidar y mantener tu Toyota en Cartagena.</h1><p>{len(cards)} guías para tomar mejores decisiones sobre mantenimiento, diagnóstico, repuestos, seguridad, modificaciones y conservación.</p></div></header><section><div class="container"><div class="blog-grid">{card_html}</div></div></section></main>{footer}</body></html>'''
blog=blog.replace('/assets/images/toyo-services-logo.svg','/assets/images/toyo-services-logo.svg?v=3')
blog=sync_html_image_dimensions(blog, ROOT)
(ROOT/'blog'/'index.html').write_text(blog,encoding='utf-8')
print(f"Generated {len(articles)} articles and blog index with {len(cards)} entries")
