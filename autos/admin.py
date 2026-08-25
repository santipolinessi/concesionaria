from django.contrib import admin
from .models import Auto, FotoAuto, Consulta


class FotoAutoInline(admin.TabularInline):
    model = FotoAuto
    extra = 3  # muestra 3 espacios vacíos para subir fotos de una


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "anio", "precio", "moneda", "condicion", "activo", "fecha_publicacion")
    list_filter = ("condicion", "marca", "activo", "moneda")
    search_fields = ("marca", "modelo")
    inlines = [FotoAutoInline]


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "auto", "email", "telefono", "fecha")
    list_filter = ("fecha",)
    readonly_fields = ("fecha",)
