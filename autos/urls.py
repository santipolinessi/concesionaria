from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('auto/<int:auto_id>/', views.detalle_auto, name='detalle_auto'),
    path('auto/<int:auto_id>/consulta/', views.enviar_consulta, name='enviar_consulta'),
]
