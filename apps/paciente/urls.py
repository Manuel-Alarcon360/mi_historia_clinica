from django.urls import path
from .views import get_pacientes, CreatePaciente, UpdatePaciente

urlpatterns = [
    path('get_pacientes/<int:pk>/', get_pacientes, name='get_pacientes'),
    path('create_pacientes/', CreatePaciente.as_view(), name='create_paciente'),
    path('update_pacientes/<int:pk>/', UpdatePaciente.as_view(), name='update_paciente'),
]