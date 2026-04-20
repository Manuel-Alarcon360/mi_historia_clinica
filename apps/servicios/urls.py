from django.urls import path
from .views import prioridades_servicio, ServicioLandingView,ServiciosAdminView,DeleteServicioAPIView,ServicioCreateView,obtener_servicio,ServicioViewSet,cambio_mostrar_landing
urlpatterns = [
   path('prioridades_servicio/', prioridades_servicio, name='prioridades_servicio'),
   path('servicio_landing/', ServicioLandingView.as_view(), name='servicio_landing'),
   path('list_servicios/', ServiciosAdminView.as_view(), name='list_servicios'),
   path('delete_servicio/<int:pk>/', DeleteServicioAPIView.as_view(), name='delete_servicio'),
   path('create_servicio/', ServicioCreateView.as_view(), name='create_servicio'),
   path('detalle_servicio/<int:pk>/', obtener_servicio, name='detalle_servicio'),
   path('update_servicio/<int:pk>/', ServicioViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='update_servicio'),
   path('cambio_mostrar_landing/<int:pk>/', cambio_mostrar_landing, name='cambio_mostrar_landing'),
]