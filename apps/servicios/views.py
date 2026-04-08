from urllib import request
from venv import logger
from django.shortcuts import render
from django.db.models import Q
from apps.servicios.models import ServicioLanding
from apps.servicios.serializers import ServicioSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from rest_framework import status,viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, DestroyAPIView
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.files.storage import default_storage


# Create your views here.




class ServicioLandingView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        servicios = ServicioLanding.objects.filter(mostrar_serv_landing=True)
        serializer = ServicioSerializer(
            servicios, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    
class ServiciosAdminView(ListAPIView):
    queryset = ServicioLanding.objects.all()
    serializer_class = ServicioSerializer
    def list(self, request, *args, **kwargs):
        logger.info("Lista de servicios obtenida con éxito")
        return super().list(request, *args, **kwargs) 
    
    
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = ServicioLanding.objects.all()
    serializer_class = ServicioSerializer
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['put', 'patch'], url_path='update_servicio')
    def update_servicio(self, request, pk=None):

        servicio = self.get_object()
        serializer = self.get_serializer(
            servicio,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtener_servicio(request, pk ):
    servicio = ServicioLanding.objects.get(id=pk)
    if servicio:
        servicio_serializer = ServicioSerializer(servicio,context={'request': request})
        response_data = {
            "servicio": servicio_serializer.data,
        }
        logger.info(f"Servicio obtenido con éxito: ID {pk}")
        return Response({
            "detail": "Servicio obtenido con éxito.",
            "data": response_data
        }, status=status.HTTP_200_OK)
        
    else:
        logger.error(f"Servicio no encontrado: ID {pk}")
        return Response({
            "detail": "Error al obtener el servicio.",
            "errors":  "No se proporciono id del servicio"
        }, status=status.HTTP_404_NOT_FOUND)

class DeleteServicioAPIView(DestroyAPIView):
    queryset = ServicioLanding.objects.all()
    serializer_class = ServicioSerializer
    def delete(self, request, *args, **kwargs):
        logger.info("Servicio eliminado con éxito")
        return super().delete(request, *args, **kwargs)

    

class ServicioCreateView(CreateAPIView):
    queryset = ServicioLanding.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        return super().create(request, *args, **kwargs)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cambio_mostrar_landing(request, pk):
    try: 
        servicio = ServicioLanding.objects.get(pk=pk)
    except ServicioLanding.DoesNotExist:
        return Response(
            {"detail": "Servicio no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )

    mostrar = request.data.get('mostrar_serv_landing')

    if mostrar is None:
        return Response(
            {"detail": "mostrar_serv_landing es requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    servicio.mostrar_serv_landing = mostrar
    servicio.save()

    return Response(
        {"mostrar_serv_landing": servicio.mostrar_serv_landing},
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
def prioridades_servicio(request):  
    prioridades = [
        {"id": key, "label": label}
        for key, label in ServicioLanding.PRIORIDAD_SERVICIO
    ]
    return Response(prioridades)