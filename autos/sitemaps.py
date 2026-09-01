from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Auto


class AutoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Auto.objects.filter(activo=True)

    def location(self, obj):
        return reverse('detalle_auto', args=[obj.id])

    def lastmod(self, obj):
        return obj.fecha_publicacion


class CatalogoSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['catalogo']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'catalogo': CatalogoSitemap,
    'autos': AutoSitemap,
}
