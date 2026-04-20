from urllib import request
from venv import logger
from django.shortcuts import render
from django.db.models import Q
from apps.clientes.models import ClientesLanding
from apps.clientes.serializers import ClienteSerializer
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



class ClientesLandingView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        clientes = ClientesLanding.objects.filter(mostrar_cl_landing=True)
        serializer = ClienteSerializer(
            clientes, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = ClientesLanding.objects.all()
    serializer_class = ClienteSerializer
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['put', 'patch'], url_path='update_cliente')
    def update_cliente(self, request, pk=None):

        cliente = self.get_object()
        serializer = self.get_serializer(
            cliente,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def obtener_cliente(request, pk ):
    cliente = ClientesLanding.objects.get(id=pk)
    if cliente:
        cliente_serializer = ClienteSerializer(cliente,context={'request': request})
        response_data = {
            "cliente": cliente_serializer.data,
        }
        logger.info(f"Cliente obtenido con éxito: ID {pk}")
        return Response({
            "detail": "Cliente obtenido con éxito.",
            "data": response_data
        }, status=status.HTTP_200_OK)
        
    else:
        logger.error(f"Cliente no encontrado: ID {pk}")
        return Response({
            "detail": "Error al obtener el cliente.",
            "errors":  "No se proporciono id del cliente"
        }, status=status.HTTP_404_NOT_FOUND)


class ClientesAdminView(ListAPIView):

    queryset = ClientesLanding.objects.all()
    serializer_class = ClienteSerializer
    def list(self, request, *args, **kwargs):
        logger.info("Lista de clientes obtenida con éxito")
        return super().list(request, *args, **kwargs) 


class DeleteClienteAPIView(DestroyAPIView):
    queryset = ClientesLanding.objects.all()
    serializer_class = ClienteSerializer
    def delete(self, request, *args, **kwargs):
        logger.info("Cliente eliminado con éxito")
        return super().delete(request, *args, **kwargs)

    

class ClienteCreateView(CreateAPIView):
    queryset = ClientesLanding.objects.all()
    serializer_class = ClienteSerializer
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
        cliente = ClientesLanding.objects.get(pk=pk)
    except ClientesLanding.DoesNotExist:
        return Response(
            {"detail": "Cliente no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )

    mostrar = request.data.get('mostrar_cl_landing')

    if mostrar is None:
        return Response(
            {"detail": "mostrar_cl_landing es requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cliente.mostrar_cl_landing = mostrar
    cliente.save()

    return Response(
        {"mostrar_cl_landing": cliente.mostrar_cl_landing},
        status=status.HTTP_200_OK
    )
    
@api_view(['GET'])
def prioridades_cliente(request):
    prioridades = [
        {"value": key, "label": label}
        for key, label in ClientesLanding.PRIORIDAD_CLIENTE
    ]
    return Response(prioridades)
