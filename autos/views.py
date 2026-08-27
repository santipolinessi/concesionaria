from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Auto, Consulta


def catalogo(request):
    autos = Auto.objects.filter(activo=True)

    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    anio = request.GET.get('anio', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    km_min = request.GET.get('km_min', '')
    km_max = request.GET.get('km_max', '')

    if marca:
        autos = autos.filter(marca__iexact=marca)
    if modelo:
        autos = autos.filter(modelo__icontains=modelo)
    if anio:
        autos = autos.filter(anio=anio)
    if precio_min:
        autos = autos.filter(precio__gte=precio_min)
    if precio_max:
        autos = autos.filter(precio__lte=precio_max)
    if km_min:
        # Los 0km no tienen kilometraje cargado (None); si piden un mínimo
        # mayor a 0, quedan afuera correctamente (tienen 0 km reales).
        autos = autos.filter(kilometraje__gte=km_min)
    if km_max:
        # Acá sí hay que incluir los 0km a mano: tienen 0 km reales,
        # pero al ser None no pasarían un simple kilometraje__lte.
        autos = autos.filter(Q(kilometraje__lte=km_max) | Q(kilometraje__isnull=True))

    orden = request.GET.get('orden', '')
    if orden == 'precio_asc':
        autos = autos.order_by('precio')
    elif orden == 'precio_desc':
        autos = autos.order_by('-precio')
    # 'recientes' (o vacío) usa el orden por defecto del modelo: -fecha_publicacion

    # Para poblar los <select> de marca y año con valores que existen realmente
    marcas_disponibles = Auto.objects.filter(activo=True).values_list('marca', flat=True).distinct().order_by('marca')
    anios_disponibles = Auto.objects.filter(activo=True).values_list('anio', flat=True).distinct().order_by('-anio')

    contexto = {
        'autos': autos,
        'marcas_disponibles': marcas_disponibles,
        'anios_disponibles': anios_disponibles,
        'filtros': {
            'marca': marca, 'modelo': modelo, 'anio': anio,
            'precio_min': precio_min, 'precio_max': precio_max,
            'km_min': km_min, 'km_max': km_max, 'orden': orden,
        },
    }
    return render(request, 'autos/catalogo.html', contexto)


def detalle_auto(request, auto_id):
    auto = get_object_or_404(Auto, id=auto_id, activo=True)
    return render(request, 'autos/detalle.html', {'auto': auto})


def enviar_consulta(request, auto_id):
    auto = get_object_or_404(Auto, id=auto_id)
    if request.method == 'POST':
        Consulta.objects.create(
            auto=auto,
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono', ''),
            mensaje=request.POST.get('mensaje', ''),
        )
        messages.success(request, '¡Gracias! Te vamos a contactar a la brevedad.')
    return redirect('detalle_auto', auto_id=auto.id)


def robots_txt(request):
    contenido = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
    )
    return HttpResponse(contenido, content_type='text/plain')
