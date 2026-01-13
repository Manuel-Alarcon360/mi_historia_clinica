from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from .models import Paciente
from .serializer import SerializerPaciente
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_pacientes(request, pk): 
    if not pk:
        return Response({
            "detail": "Error al obtener el paciente.",
            "errors": "Este campo pk es obligatorio."
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        paciente = Paciente.objects.get(cliente_FK=pk)
        logger.info(f"Paciente encontrado: {paciente}")
        serializer = SerializerPaciente(paciente)
        
    except Paciente.DoesNotExist:
        logger.error(f"Paciente no encontrado: {pk}")
        return Response({
            "detail": "Error al obtener el paciente.",
            "errors": "No se encontró un paciente con el ID proporcionado."
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "detail": "Paciente encontrado con éxito.", 
        "data": serializer.data
    }, status=status.HTTP_200_OK)

class CreatePaciente(generics.CreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = SerializerPaciente

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Paciente creado exitosamente: ID {response.data.get('id', 'N/A')}")
            return Response({
                "detail": "Paciente creado exitosamente.",
                "data": response.data
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            logger.warning(f"Error de validación al crear paciente: {e}")
            return Response({
                "detail": "Error de validación al crear el paciente.",
                "errors": e.detail if hasattr(e, 'detail') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error inesperado al crear paciente: {str(e)}", exc_info=True)
            return Response({
                "detail": "Error interno del servidor al crear el paciente.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdatePaciente(generics.UpdateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = SerializerPaciente
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        try:
            paciente = self.get_object()
            response = super().update(request, *args, **kwargs)
            logger.info(f"Paciente actualizado exitosamente: ID {paciente.id}")
            return Response({
                "detail": "Paciente actualizado exitosamente.",
                "data": response.data
            }, status=status.HTTP_200_OK)
            
        except Paciente.DoesNotExist:
            logger.error(f"Paciente no encontrado para actualización: {self.kwargs.get('pk')}")
            return Response({
                "detail": "Error al actualizar el paciente.",
                "errors": "No se encontró un paciente con el ID proporcionado."
            }, status=status.HTTP_404_NOT_FOUND)
            
        except ValidationError as e:
            logger.warning(f"Error de validación al actualizar paciente: {e}")
            return Response({
                "detail": "Error de validación al actualizar el paciente.",
                "errors": e.detail if hasattr(e, 'detail') else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            