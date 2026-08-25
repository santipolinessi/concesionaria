from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Auto, Consulta


def catalogo(request):
    autos = Auto.objects.filter(activo=True)

    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    anio = request.GET.get('anio', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')

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
