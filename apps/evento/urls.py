from django.urls import path
from .views import EventoChoicesView , EventosLandingView  ,EventosAdminView,EventoCreateView,DeleteFormularioAPIView,obtener_evento,EventoViewSet,cambio_mostrar_landing
urlpatterns = [
   path('choices/', EventoChoicesView.as_view(), name='choices'),
   path('eventos_landing/', EventosLandingView.as_view(), name='eventos_landing'),  #Muestra los eventos activos para la landing tab(eventos)
   path('list_eventos/', EventosAdminView.as_view(), name='list_evento'),
   path('delete_evento/<int:pk>/', DeleteFormularioAPIView.as_view(), name='delete_evento'),
   path('create_evento/', EventoCreateView.as_view(), name='create_evento'),
   path('detalle_evento/<int:pk>/', obtener_evento, name='detalle_evento'),
   path('update_evento/<int:pk>/', EventoViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='update_evento'),
   path('cambio_mostrar_landing/<int:pk>/', cambio_mostrar_landing, name='cambio_mostrar_landing'),
]