from venv import logger
from django.shortcuts import render
from django.db.models import Q
from apps.evento.models import Evento
from apps.evento.serializers import EventoSerializer
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

# Create your views here.


class EventoChoicesView(APIView):   #ok
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            "tipo_evento": [
                {"value": key, "label": label}
                for key, label in Evento.TIPO_EVENTO
            ]
        })
    
    
# @method_decorator(csrf_exempt, name='dispatch')    
# def create(self, request, *args, **kwargs):     # REVISAR SI NO SE UTILIZA

#     data = request.data.copy()
#     data['creado_por'] = request.user.id

#     serializer = self.get_serializer(data=data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()

#     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# @method_decorator(csrf_exempt, name='dispatch')
# class EventoViewSet(ModelViewSet):                          #### reviasr si se usa 
   
#     serializer_class = EventoSerializer
#     queryset = Evento.objects.all()

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         data['creado_por'] = request.user.id

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
class EventoCreateView(CreateAPIView):    #Nuevo    #ok
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)
    
class EventosAdminView(ListAPIView):    #ok
    
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def list(self, request, *args, **kwargs):
        actualizar_estado_eventos()
        logger.info("Lista de eventos obtenida con éxito")
        return super().list(request, *args, **kwargs)
    
    
def list(self, request, *args, **kwargs):
    eventos = Evento.objects.filter(creado_por=request.user)
    serializer = self.get_serializer(eventos, many=True)
    return Response(serializer.data)

def retrieve(self, request, *args, **kwargs):
    evento = self.get_object()
    serializer = self.get_serializer(evento)
    return Response(serializer.data)

# def update_evento(self, request, *args, **kwargs):     #Revisar final para eliminar
#     print("SE EDITA EVENTO",request )
#     evento = self.get_object()
    
#     serializer = self.get_serializer(
#         evento,
#         data=request.data,
#         partial=True
#     )
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

class EventoViewSet(viewsets.ModelViewSet):   #ok
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['put', 'patch'], url_path='update_evento')
    def update_evento(self, request, pk=None):
        print("SE EDITA EVENTO", request.data)

        evento = self.get_object()
        serializer = self.get_serializer(
            evento,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # opcional pero explícito
def cambio_mostrar_landing(request, pk):
    actualizar_estado_eventos()
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response(
            {"detail": "Evento no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )

    mostrar = request.data.get('mostrar_en_landing')

    if mostrar is None:
        return Response(
            {"detail": "mostrar_en_landing es requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    evento.mostrar_en_landing = mostrar
    evento.save()

    return Response(
        {"mostrar_en_landing": evento.mostrar_en_landing},
        status=status.HTTP_200_OK
    )

class DeleteFormularioAPIView(DestroyAPIView):   #ok
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    def delete(self, request, *args, **kwargs):
        print("EVENTO ELIMINADO CORRECTAMENTE")
        logger.info("Evento eliminado con éxito")
        return super().delete(request, *args, **kwargs)
    
    
class EventosLandingView(APIView):   #ok en landing-page
    permission_classes = [AllowAny]
    
    def get(self, request):
        actualizar_estado_eventos()
        hoy = now().date()
        eventos = Evento.objects.filter(
            activo=True,
            mostrar_en_landing=True,
            fecha_inicio__lte=hoy
        ).filter(
            Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
        )
        serializer = EventoSerializer(
            eventos, 
            many=True,
            context={'request': request}
        )
        
        return Response(serializer.data)

@api_view(['GET'])
def obtener_evento(request, pk ):
    evento = Evento.objects.get(id=pk)
    if evento:
        evento_serializer = EventoSerializer(evento,context={'request': request})
        response_data = {
            "evento": evento_serializer.data,
        }
        logger.info(f"Evento obtenido con éxito: ID {pk}")
        return Response({
            "detail": "Evento obtenido con éxito.",
            "data": response_data
        }, status=status.HTTP_200_OK)
        
    else:
        logger.error(f"Evento no encontrado: ID {pk}")
        return Response({
            "detail": "Error al obtener el evento.",
            "errors":  "No se proporciono id del evento"
        }, status=status.HTTP_404_NOT_FOUND)
def actualizar_estado_eventos():
    hoy = now().date()
    Evento.objects.filter(
        fecha_inicio__lte=hoy
    ).filter(
        Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
    ).update(activo=True)
    Evento.objects.filter(
        mostrar_en_landing=True
    ).exclude(
        Q(fecha_inicio__lte=hoy) &
        (Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True))
    ).update(activo=False)