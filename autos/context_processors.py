from django.conf import settings


def datos_contacto(request):
    return {
        'whatsapp_numero': settings.WHATSAPP_NUMERO,
        'instagram_usuario': settings.INSTAGRAM_USUARIO,
    }
