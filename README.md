# GYS Automotores

Catálogo web de compra y venta de autos usados y 0km, desarrollado en Django. Sitio en vivo: [gysautomotores.com.ar](https://gysautomotores.com.ar)

## Funcionalidades

- Catálogo público con filtros (marca, modelo, año, precio, kilómetros) y orden (más recientes, precio ascendente/descendente)
- Galería de fotos por auto, con navegación por flechas y miniaturas
- Contacto directo por WhatsApp (mensaje pre-armado por auto) e Instagram
- Botón de "compartir" por auto, con vista previa (Open Graph) al enviarlo por WhatsApp/redes
- Panel de administración (Django admin) para cargar autos y fotos sin tocar código
- SEO básico: `robots.txt`, `sitemap.xml` autogenerado, meta tags y datos estructurados (JSON-LD) para negocio local
- Página 404 personalizada

## Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Django 6.1 |
| Base de datos | PostgreSQL (producción) / SQLite (desarrollo local) |
| Almacenamiento de imágenes | Cloudinary |
| Archivos estáticos | WhiteNoise |
| Servidor de aplicación | Gunicorn |
| Hosting | Railway |
| DNS / CDN | Cloudflare |

## Estructura del proyecto

```
concesionaria/
├── autos/                      # App principal
│   ├── models.py               # Auto, FotoAuto, Consulta
│   ├── views.py                # Catálogo, detalle, robots.txt
│   ├── sitemaps.py             # Sitemap para SEO
│   ├── admin.py                # Configuración del panel /admin
│   ├── templatetags/           # Filtros custom (URLs absolutas para Open Graph)
│   ├── templates/autos/        # HTML del sitio
│   └── static/autos/           # CSS e imágenes (logo, mascota)
├── concesionaria/
│   ├── settings.py             # Configuración (lee variables de entorno)
│   └── urls.py
├── requirements.txt
├── Procfile                    # Comando de arranque en producción
└── .env.example                # Plantilla de variables de entorno
```

## Instalación local

Requisitos: Python 3.12+, pip.

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd concesionaria

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migrar la base de datos (SQLite local, no requiere configuración)
python manage.py migrate

# 5. Crear un usuario administrador
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

El sitio queda disponible en `http://127.0.0.1:8000` y el panel de administración en `http://127.0.0.1:8000/admin`.

En desarrollo local no hace falta configurar ninguna variable de entorno: el proyecto usa valores por defecto (SQLite, `DEBUG=True`, sin Cloudinary).

## Variables de entorno (producción)

Ver `.env.example` para la lista completa con comentarios. Las más importantes:

| Variable | Para qué sirve |
|---|---|
| `SECRET_KEY` | Clave de seguridad de Django |
| `DEBUG` | `False` en producción |
| `ALLOWED_HOSTS` | Dominios permitidos, separados por coma |
| `CSRF_TRUSTED_ORIGINS` | Dominios propios con `https://`, para que funcione el login al admin |
| `DATABASE_URL` | La inyecta Railway automáticamente al conectar el servicio de Postgres |
| `USE_CLOUDINARY` | `True` en producción, activa el almacenamiento de fotos en Cloudinary |
| `CLOUDINARY_CLOUD_NAME` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET` | Credenciales de Cloudinary |
| `WHATSAPP_NUMERO` / `INSTAGRAM_USUARIO` | Datos de contacto mostrados en el sitio |

## Comandos útiles

```bash
python manage.py createsuperuser       # Crear usuario admin
python manage.py migrate               # Aplicar migraciones
python manage.py collectstatic         # Recolectar archivos estáticos (solo necesario en producción)
```

En producción (Railway), para ejecutar comandos directo contra la base real, usar `railway ssh` (conecta al contenedor en producción) en vez de `railway run` (que ejecuta el comando localmente).

## Despliegue

El proyecto está desplegado en Railway, con PostgreSQL como base de datos y Cloudinary para el almacenamiento de fotos. El `Procfile` define el comando de arranque:

```
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn concesionaria.wsgi
```

Cada `git push` a la rama principal dispara un redeploy automático en Railway.

## Modelos principales

- **Auto**: marca, modelo, año, precio, moneda, condición (0km/usado), kilometraje, specs, descripción, estado activo/inactivo
- **FotoAuto**: galería de fotos asociada a cada auto (relación uno a muchos)
- **Consulta**: registro de contactos por formulario (actualmente sin uso activo en el frontend, preparado para retomarlo)
