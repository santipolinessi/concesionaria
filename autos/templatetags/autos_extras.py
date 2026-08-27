from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_absoluta(context, url):
    """
    Convierte una URL relativa (ej. /media/autos/foto.jpg) en absoluta
    usando el dominio del request actual. Si la URL ya es absoluta
    (ej. fotos servidas desde Cloudinary en producción), la deja igual.
    """
    if not url:
        return ''
    if url.startswith('http://') or url.startswith('https://'):
        return url
    request = context.get('request')
    if request:
        return request.build_absolute_uri(url)
    return url
