# Toyo Services

Sitio estático de un taller independiente especializado exclusivamente en mantenimiento y mecánica Toyota en Cartagena, Colombia.

## Publicación

Importa este repositorio en Vercel como proyecto estático. No requiere comando de compilación.

La URL canónica de producción es `https://toyoservicescartagena.com`. Los canonical, datos estructurados, `sitemap.xml` y `robots.txt` deben conservar este dominio.

Los botones de WhatsApp usan el número comercial +57 301 863 8164. El formulario prepara una solicitud; el visitante debe enviarla desde WhatsApp. No hay un sistema de analítica configurado en el repositorio.

## Imágenes

- `toyota-corolla.webp`: derivada de “Toyota COROLLA Sport G (3BA-NRE210H-BHXNZ) front.jpg”, Wikimedia Commons, autor Tokumeigakarinoaoshima, CC BY-SA 4.0.
- `motor-toyota.webp`: derivada de “The engineroom of Toyota COROLLA Sport G (3BA-NRE210H-BHXNZ).jpg”, Wikimedia Commons, autor Tokumeigakarinoaoshima, CC BY-SA 4.0.
- `land-cruiser-prado.webp`: derivada de “TOYOTA LAND CRUISER PRADO (J150) China.jpg”, Wikimedia Commons, autor Dinkun Chen, CC BY-SA 4.0.
- `prado-baku.webp`: derivada de “Toyota Land Cruiser Prado, Baku (P1090223).jpg”, Wikimedia Commons, autor Matti Blume, CC BY-SA 4.0.
- `toyota-fortuner.webp`: derivada de “TOYOTA FORTUNER (AN150,AN160) China.jpg”, Wikimedia Commons, autor Dinkun Chen, CC BY-SA 4.0.
- `fortuner-cape-town.webp`: derivada de “Toyota Fortuner, Cape Town (P1060077).jpg”, Wikimedia Commons, autor Matti Blume, CC BY-SA 4.0.
- `hilux-4x4.webp`: derivada de “Toyota Hilux 4x4 J 2020.jpg”, Wikimedia Commons, autor Captainmorlypogi1959, CC BY-SA 4.0.
- `hilux-catalog-premium.webp`: composición fotorealista generada para el sitio; es representativa y no documenta un vehículo de cliente ni un trabajo real.

Las fotografías públicas fueron redimensionadas, adaptadas y convertidas a WebP. La atribución completa se conserva en `/creditos-imagenes/`.

## Comprobación antes de publicar

```powershell
python scripts\generate_services.py
python scripts\generate_blog.py
python scripts\sync_image_dimensions.py
python scripts\generate_sitemap.py
python scripts\validate_site.py
python scripts\generate_sitemap.py --check
```
