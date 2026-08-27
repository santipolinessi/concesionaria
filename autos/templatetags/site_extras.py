from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_url(context, url):
    """Convierte una URL relativa (ej. /media/autos/foto.jpg) en absoluta
    (ej. https://tudominio.com/media/autos/foto.jpg). Si la URL ya es
    absoluta (como las de Cloudinary), la devuelve sin cambios."""
    request = context.get('request')
    if not request or not url:
        return url
    return request.build_absolute_uri(url)
