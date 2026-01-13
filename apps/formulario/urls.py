from django.urls import path
from .views import obtener_formulario, crear_formulario, ListFormulariosAPIView, DeleteFormularioAPIView, actualizar_campos_formulario

urlpatterns = [
    path('create_formulario/', crear_formulario, name='create_formulario'),
    path('obtener_formulario/<pk>/', obtener_formulario, name='obtener_formulario'),
    path('actualizar_campos/<int:formulario_id>/', actualizar_campos_formulario, name='actualizar_campos_formulario'),
    path('list_formularios/', ListFormulariosAPIView.as_view(), name='list_formularios'),
    path('delete_formulario/<int:pk>/', DeleteFormularioAPIView.as_view(), name='delete_formulario'),
]   