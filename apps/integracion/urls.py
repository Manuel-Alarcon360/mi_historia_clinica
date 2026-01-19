from django.urls import path
from .views import TokenIntegracionListCreateView, TokenIntegracionDetailView, obtener_clientes_externos, obtener_citas, create_cliente_externo, consultar_cliente, obtener_urls_clientes,test_requests

urlpatterns = [
    path("list_integracion/", TokenIntegracionListCreateView.as_view(), name="list_integracion"),
    path("crear_integracion/", TokenIntegracionListCreateView.as_view(), name="crear_integracion"),
    #path("list_integracion/<int:pk>/", TokenIntegracionDetailView.as_view(), name="detail_integracion"),
    path("obtener_clientes_externos/", obtener_clientes_externos, name="clientes_integracion"),
    path("obtener_citas/", obtener_citas, name="citas_integracion"),
    path("crear_cliente/", create_cliente_externo, name="crear_cliente_externo"),
    path("buscar_cliente/", consultar_cliente, name="buscar_cliente_externo"),  # Nueva ruta para buscar cliente
    path("obtener_urls_clientes/", obtener_urls_clientes, name="urls_clientes_integracion"),
    path("obtener_clientes_externos/", test_requests, name="test_requests"),
]