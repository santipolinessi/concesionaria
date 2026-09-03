from django.db import models
from django.utils import timezone
from datetime import timedelta


class Auto(models.Model):
    CONDICION_CHOICES = [
        ("0km", "0km"),
        ("usado", "Usado"),
    ]
    MONEDA_CHOICES = [
        ("ARS", "Pesos (ARS)"),
        ("USD", "Dólares (USD)"),
    ]

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField(verbose_name="Año")
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default="ARS")
    condicion = models.CharField(max_length=10, choices=CONDICION_CHOICES)
    kilometraje = models.PositiveIntegerField(null=True, blank=True, help_text="Dejar vacío si es 0km")
    combustible = models.CharField(max_length=30, blank=True)
    transmision = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=30, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True, help_text="Desmarcar para ocultar del catálogo sin borrar")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

    @property
    def foto_principal(self):
        return self.fotos.first()

    @property
    def es_nuevo(self):
        """True si se publicó en los últimos 7 días, para mostrar el badge 'Nuevo'."""
        return timezone.now() - self.fecha_publicacion <= timedelta(days=7)


class FotoAuto(models.Model):
    auto = models.ForeignKey(Auto, related_name="fotos", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="autos/")
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Foto de {self.auto}"


class Consulta(models.Model):
    auto = models.ForeignKey(Auto, related_name="consultas", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    mensaje = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.nombre} - {self.auto}"
