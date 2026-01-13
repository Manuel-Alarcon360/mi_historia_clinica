from django.urls import path
from .views import create_historias, obtener_detalle_historia_clinica, obtener_historia_clinica
urlpatterns = [
    path('crear_historia_clinica/', create_historias.as_view(), name='crear_historia'),
    path('obtener_historia/<int:paciente_id>/', obtener_historia_clinica, name='obtener_historia'),
    path('obtener_detalle_historia/<int:historia_id>/', obtener_detalle_historia_clinica, name='obtener_detalle_historia'),
]