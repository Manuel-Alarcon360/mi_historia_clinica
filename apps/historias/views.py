from django.shortcuts import render
from rest_framework import generics
from .models import HistoriaClinica, DetalleHistoria
from .serializer import HistoriaClinicaSerializer, DetalleHistoriaSerializer
from apps.paciente.models import Paciente
from apps.paciente.serializer import SerializerPaciente
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import F
import logging
from datetime import datetime, date
from django.utils import timezone
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def _convertir_fecha_utc_a_utc5(fecha_utc_str):
    """
    Convierte una fecha/hora de UTC a UTC-5 (zona horaria de Colombia)
    """
    try:
        if not fecha_utc_str:
            return fecha_utc_str
        
        if isinstance(fecha_utc_str, datetime):
            fecha_utc = fecha_utc_str
        else:
            if 'T' in fecha_utc_str:
                if fecha_utc_str.endswith('Z'):
                    fecha_utc = datetime.fromisoformat(fecha_utc_str.replace('Z', '+00:00'))
                elif '+' not in fecha_utc_str and 'Z' not in fecha_utc_str:
                    fecha_utc = datetime.fromisoformat(fecha_utc_str).replace(tzinfo=ZoneInfo('UTC'))
                else:
                    fecha_utc = datetime.fromisoformat(fecha_utc_str)
            else:
                fecha_utc = datetime.strptime(fecha_utc_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo('UTC'))
        if fecha_utc.tzinfo is None:
            fecha_utc = fecha_utc.replace(tzinfo=ZoneInfo('UTC'))
        elif str(fecha_utc.tzinfo) != 'UTC':
            fecha_utc = fecha_utc.astimezone(ZoneInfo('UTC'))
        utc_menos_5 = ZoneInfo('America/Bogota')
        fecha_local = fecha_utc.astimezone(utc_menos_5)
        
        return fecha_local.strftime("%Y-%m-%d %H:%M")
        
    except Exception as e:
        logger.warning(f"Error al convertir fecha UTC a UTC-5 '{fecha_utc_str}': {str(e)}")
        if isinstance(fecha_utc_str, str):
            if 'T' in fecha_utc_str:
                fecha_hora_minuto = fecha_utc_str[:16]
                return fecha_hora_minuto.replace('T', ' ')
            else:
                return fecha_utc_str[:16]
        return str(fecha_utc_str)[:16]


def _convertir_fecha_nacimiento(fecha_str):
    if not fecha_str:
        return None
    try:
        if isinstance(fecha_str, date):
            return fecha_str
        if isinstance(fecha_str, str):
            if 'T' not in fecha_str:
                return datetime.strptime(fecha_str, "%Y-%m-%d").date()
            else:
                return datetime.fromisoformat(fecha_str.replace('Z', '+00:00')).date()
        logger.warning(f"Tipo inesperado para fecha_nacimiento: {type(fecha_str)}")
        return None
    except Exception as e:
        logger.warning(f"Error al convertir fecha '{fecha_str}': {str(e)}")
        return None

def _validar_paciente_existente(cliente):
    logger.info(f"Validando existencia de paciente con cliente_FK: {cliente}")
    try:
        paciente = Paciente.objects.get(cliente_FK=cliente)
        logger.info(f"Paciente encontrado con ID: {paciente.id}")
        return paciente
    except Paciente.DoesNotExist:
        logger.warning(f"Paciente no encontrado para cliente_FK: {cliente}")
        return None


def _crear_paciente_si_no_existe(data):
    cliente = data.get("cliente_FK")
    logger.info(f"Iniciando proceso de creación/actualización de paciente para cliente_FK: {cliente}")

    data["fecha_nacimiento"] = _convertir_fecha_nacimiento(data.get("fecha_nacimiento"))

    paciente_existente = _validar_paciente_existente(cliente)
    if paciente_existente:
        logger.info(f"Actualizando paciente existente con ID: {paciente_existente.id}")
        _actualizar_paciente_existente(paciente_existente, data)
        return paciente_existente
    
    logger.info(f"Creando nuevo paciente para cliente_FK: {cliente}")
    serializer = SerializerPaciente(data=data)
    if serializer.is_valid():
        nuevo_paciente = serializer.save()
        logger.info(f"Nuevo paciente creado exitosamente con ID: {nuevo_paciente.id}")
        return nuevo_paciente
    else:
        logger.error(f"Error en validación del serializer para crear paciente: {serializer.errors}")
    return None


def _actualizar_paciente_existente(paciente, data):
    logger.info(f"Actualizando datos del paciente con ID: {paciente.id}")
    
    # Convertir fecha si es necesario
    if 'fecha_nacimiento' in data:
        data["fecha_nacimiento"] = _convertir_fecha_nacimiento(data.get("fecha_nacimiento"))
    
    serializer = SerializerPaciente(paciente, data=data, partial=True)
    if serializer.is_valid():
        paciente_actualizado = serializer.save()
        logger.info(f"Paciente actualizado exitosamente con ID: {paciente_actualizado.id}")
        return paciente_actualizado
    else:
        logger.error(f"Error en validación del serializer para actualizar paciente ID {paciente.id}: {serializer.errors}")
    return paciente

def _convertir_respuesta_a_string(respuesta):
    if respuesta is None:
        return ""
    if isinstance(respuesta, bool):
        return "true" if respuesta else "false"
    if isinstance(respuesta, (int, float)):
        return str(respuesta)
    if isinstance(respuesta, str):
        return respuesta
    return str(respuesta)

def _registrar_detalle_historia_clinica(data):
    logger.info("Iniciando registro de detalle de historia clínica")
    
    campos = data.get("campos", [])
    formulario_fk = data.get("formulario_fk")
    historia_fk = data.get("historia_fk")
        
    detalles_creados = []
    for campo_data in campos:
        respuesta_original = campo_data.get("respuesta_campo")
        respuesta_convertida = _convertir_respuesta_a_string(respuesta_original)
        
        detalle_data = {
            "campo_fk": campo_data.get("campo_fk"),
            "respuesta_campo": respuesta_convertida,
            "formulario_fk": formulario_fk,
            "historia_fk": historia_fk
        }
        
        logger.info(f"Procesando campo {campo_data.get('campo_fk')}: {respuesta_original} -> {respuesta_convertida}")
        
        serializer = DetalleHistoriaSerializer(data=detalle_data)
        if serializer.is_valid():
            nuevo_detalle = serializer.save()
            detalles_creados.append(nuevo_detalle)
            logger.info(f"Detalle de historia clínica creado exitosamente con ID: {nuevo_detalle.id} para campo {campo_data.get('campo_fk')}")
        else:
            logger.error(f"Error en validación del serializer para detalle de historia clínica campo {campo_data.get('campo_fk')}: {serializer.errors}")
            return None
    
    logger.info(f"Se crearon {len(detalles_creados)} detalles de historia clínica exitosamente")
    return detalles_creados[0] if detalles_creados else None

class create_historias(generics.CreateAPIView):
    queryset = HistoriaClinica.objects.all()
    serializer_class = HistoriaClinicaSerializer

    def post(self, request, *args, **kwargs):
        logger.info("Iniciando proceso de creación de historia clínica")
        
        paciente = _crear_paciente_si_no_existe(request.data.get("paciente"))
        if not paciente:
            logger.error("Error al crear o actualizar el paciente")
            return Response({
            "detail": "Ocurrio un error al crear o actualizar el paciente",
            "error": "Verficar errores"
        }, status=400)
        
        logger.info(f"Creando historia clínica para paciente ID: {paciente.id}")
        historia_clinica = request.data.get("historia_clinica")
        historia_clinica["paciente_fk"] = paciente.id
        historia_clinica["doctor"] = request.user.id
        try:
            if not 'id' in historia_clinica:
                serializer = self.get_serializer(data=historia_clinica)
                serializer.is_valid(raise_exception=True)
                instancia_historia = serializer.save()
                logger.info(f"Historia clínica creada exitosamente con ID: {instancia_historia.id}")
                instancia_data = {"id": instancia_historia.id}
            else:
                instancia_data = {"id": historia_clinica['id']}

        except Exception as e:
            logger.error(f"Error al crear historia clínica: {str(e)}")
            return Response({
                "detail": "Error al crear la historia clínica",
                "error": str(e)
            }, status=400)
        
        request.data["detalle_historia"]["historia_fk"] = instancia_data["id"]   
        detalle = _registrar_detalle_historia_clinica(request.data.get("detalle_historia"))
        if not detalle:
            logger.error(f"Error al crear el detalle de la historia clínica para historia ID: {instancia_data['id']}")
            return Response({
                "detail": "Ocurrio un error al crear el detalle de la historia clinica",
                "error": "Verficar errores"
            },status=400)
        
        logger.info(f"Proceso completado exitosamente. Historia clínica ID: {instancia_data['id']}, Detalle ID: {detalle.id}")
        
        return Response({
            "detail": "Historia clínica creada exitosamente",
            "historia_clinica_id": instancia_data["id"],
            "paciente_id": paciente.id,
            "detalle_id": detalle.id
        }, status=201)
    

@api_view(['GET'])
def obtener_historia_clinica(request, paciente_id):
    logger.info(f"Obteniendo historia clínica para paciente ID: {paciente_id}")
    data = HistoriaClinica.objects.filter(paciente_fk=paciente_id)
    serializer_data = HistoriaClinicaSerializer(data, many=True)
    data = {
            "detail":"Historias clínicas obtenidas exitosamente",
            "data": serializer_data.data[0] if serializer_data.data else None
        }
    return Response(data, status=200)

@api_view(['GET'])
def obtener_detalle_historia_clinica(request, historia_id):
    logger.info(f"Obteniendo detalle de historia clínica para historia ID: {historia_id}")
    
    data = DetalleHistoria.objects.annotate(
        label_input=F('campo_fk__nombre_campo')
    ).filter(historia_fk=historia_id).prefetch_related('formulario_fk', 'campo_fk').order_by('fecha_creacion')
    serializer_data = DetalleHistoriaSerializer(data, many=True)
    grouped_data = {}
    total_count = 0
    
    for item in serializer_data.data:
        fecha_creacion_completa = item['fecha_creacion']
        fecha_hora_minuto = _convertir_fecha_utc_a_utc5(fecha_creacion_completa)
        
        if fecha_hora_minuto not in grouped_data:
            grouped_data[fecha_hora_minuto] = []
        
        grouped_data[fecha_hora_minuto].append(item)
        total_count += 1
    
    sorted_groups = dict(sorted(grouped_data.items()))
    
    logger.info(f"Detalles agrupados en {len(sorted_groups)} grupos por fecha/hora para historia ID: {historia_id}")
    
    response_data = {
        "results": sorted_groups,
        "count": total_count,
        "groups_count": len(sorted_groups),
        "next": None,
        "previous": None,
    }
    return Response(response_data, status=200)
