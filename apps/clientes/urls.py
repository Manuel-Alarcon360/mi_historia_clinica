from django.urls import path
from .views import   prioridades_cliente, ClienteCreateView, ClientesAdminView,cambio_mostrar_landing, DeleteClienteAPIView, obtener_cliente, ClienteViewSet,ClientesLandingView


urlpatterns = [
   path('clientes_landing/', ClientesLandingView.as_view(), name='clientes_landing'), 
   path('list_clientes/', ClientesAdminView.as_view(), name='list_clientes'),
   path('delete_cliente/<int:pk>/', DeleteClienteAPIView.as_view(), name='delete_cliente'),
   path('create_cliente/', ClienteCreateView.as_view(), name='create_cliente'),
   path('detalle_cliente/<int:pk>/', obtener_cliente, name='detalle_cliente'),
   path('update_cliente/<int:pk>/', ClienteViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='update_cliente'),
   path('cambio_mostrar_landing/<int:pk>/', cambio_mostrar_landing, name='cambio_mostrar_landing'),
   path('prioridades_cliente/', prioridades_cliente, name='prioridades_cliente'),
]