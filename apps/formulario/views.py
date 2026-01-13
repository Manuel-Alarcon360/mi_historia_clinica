from django.shortcuts import render
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from .serializers import FormularioSerializer, CampoSerializer
from .models import Formulario, Campo
import logging

# Create your views here.
logger = logging.getLogger(__name__)

def _validate_principal_unique(request):
    form = Formulario.objects.filter(principal=True)
    if form.exists() and request.data.get('principal', False):
        logger.error(f"Error al crear el formulario: Ya existe un formulario principal.")
        print(form.exists(), request.data.get('principal', False))
        return Response({
            "detail": "Error al crear el formulario.",
            "errors": "Ya existe un formulario principal. Solo puede haber un formulario principal a la vez."
        }, status=status.HTTP_400_BAD_REQUEST)
    return None

@api_view(['POST'])
def crear_formulario(request):
    data = request.data.get('campos', [])
    
    validation_error = _validate_principal_unique(request)
    if validation_error:
        return validation_error
    
    creaFormulario = Formulario.objects.create(nombre_formulario=request.data.get('nombre_formulario', 'Formulario Sin Nombre'), principal=request.data.get('principal', False))
    formulario_id = creaFormulario.id

    for campo_data in data:
        campo_data_clean = _normalizar_campo_data(campo_data)
        campo_data_clean['formulario_FK'] = formulario_id
        
        serializer = CampoSerializer(data=campo_data_clean)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Campo creado con éxito: {serializer.data.get("nombre_campo")}")
        else:
            logger.error(f"Error crear campo: {serializer.errors}")
            return Response({
                "detail": "Error al crear el formulario.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Formulario creado con éxito.", "id": formulario_id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def obtener_formulario(request, pk ):
    try:
        if pk == 'principal':
            logger.error("ID de formulario no proporcionado")
            formulario = Formulario.objects.get(principal=True)
        else:
            formulario = Formulario.objects.get(id=pk)

        campos = Campo.objects.filter(formulario_FK=formulario.id, estado_campo = True)
        formulario_serializer = FormularioSerializer(formulario)
        campos_serializer = CampoSerializer(campos, many=True)

        response_data = {
            "formulario": formulario_serializer.data,
            "campos": campos_serializer.data
        }
        logger.info(f"Formulario obtenido con éxito: ID {pk}")
        return Response({
            "detail": "Formulario obtenido con éxito.",
            "data": response_data
        }, status=status.HTTP_200_OK)

    except Formulario.DoesNotExist:
        logger.error(f"Formulario no encontrado: ID {pk}")
        if pk == 'principal':
            error_msg = "No se encontró un formulario principal."
        return Response({
            "detail": "Error al obtener el formulario.",
            "errors": error_msg or "No se encontró un formulario con el ID proporcionado."
        }, status=status.HTTP_404_NOT_FOUND)


class ListFormulariosAPIView(ListAPIView):

    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    def list(self, request, *args, **kwargs):
        logger.info("Lista de formularios obtenida con éxito")
        return super().list(request, *args, **kwargs)

class DeleteFormularioAPIView(DestroyAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    def delete(self, request, *args, **kwargs):
        logger.info("Formulario eliminado con éxito")
        return super().delete(request, *args, **kwargs)


# ================== MÉTODOS AUXILIARES ==================

def _normalizar_campo_data(campo_data):
    """
    Normaliza los datos del campo para la base de datos
    - Convierte tipos de campo del frontend al formato de BD
    - Convierte opciones de array a string separado por comas
    """
    campo_normalizado = dict(campo_data)
    
    # Normalizar tipo
    campo_normalizado['tipo'] = _normalizar_tipo_campo(campo_normalizado.get('tipo'))
    
    # Normalizar opciones: convertir array a string
    opciones = campo_normalizado.get('opciones')
    if opciones is not None:
        if isinstance(opciones, list):
            # Convertir array a string separado por comas
            campo_normalizado['opciones'] = ','.join(str(opcion).strip() for opcion in opciones if opcion)
        elif isinstance(opciones, str):
            # Ya es string, mantener como está
            campo_normalizado['opciones'] = opciones.strip() if opciones else None
        else:
            # Otros tipos, convertir a string
            campo_normalizado['opciones'] = str(opciones) if opciones else None
    
    return campo_normalizado


def _normalizar_tipo_campo(tipo_frontend):

    tipo_mapping = {
        'Agregar campo de texto': 'text',
        'Agregar área de texto': 'textarea',
        'Agregar campo numérico': 'number',
        'Agregar lista desplegable': 'select',
        'Agregar casilla de verificación': 'checkbox'
    }
    return tipo_mapping.get(tipo_frontend, tipo_frontend)


def _es_campo_nuevo(campo_id):
    return isinstance(campo_id, str) and campo_id.startswith('campo_')


def _es_campo_existente(campo_id):
    try:
        return isinstance(campo_id, int) or (isinstance(campo_id, str) and campo_id.isdigit())
    except:
        return False


# ================== MÉTODO PRINCIPAL ==================

@api_view(['PUT'])
def actualizar_campos_formulario(request, formulario_id):
    try:
        try:
            validation_error = _validate_principal_unique(request)
            if validation_error:
                return validation_error
            formulario = Formulario.objects.get(id=formulario_id)
            formulario.principal = request.data.get('principal', formulario.principal)
            formulario.nombre_formulario = request.data.get('nombre_formulario', formulario.nombre_formulario)
            formulario.save()
            logger.info(f"Formulario actualizado con éxito: ID {formulario_id}")
        except Formulario.DoesNotExist:
            logger.error(f"Formulario no encontrado: ID {formulario_id}")
            return Response({
                "detail": "Error al actualizar campos.",
                "errors": "No se encontró un formulario con el ID proporcionado."
            }, status=status.HTTP_404_NOT_FOUND)

        campos_datos = request.data.get('campos_datos', [])
        campos_inactivar = request.data.get('campos_inactivar', [])
        campos_editados = request.data.get('campos_editados', [])

        resultados = {
            'campos_creados': [],
            'campos_actualizados': [],
            'campos_inactivados': [],
            'campos_omitidos': [], 
            'errores': []
        }

        with transaction.atomic():
            
            for campo_data in campos_datos:
                campo_id = campo_data.get('id')
                
                if campo_id in campos_inactivar:
                    resultados['campos_omitidos'].append({
                        'id': campo_id,
                        'nombre': campo_data.get('nombre_campo', 'Sin nombre'),
                        'razon': 'Marcado para eliminar'
                    })
                    logger.info(f"Campo {campo_id} omitido: está marcado para inactivar")
                    continue
                
                if _es_campo_nuevo(campo_id):
                    _crear_nuevo_campo(campo_data, formulario_id, resultados)
                elif _es_campo_existente(campo_id):
                    _actualizar_campo_existente(campo_data, resultados)

            for campo_data in campos_editados:
                campo_id = campo_data.get('id')
                
                if campo_id in campos_inactivar:
                    resultados['campos_omitidos'].append({
                        'id': campo_id,
                        'nombre': campo_data.get('nombre_campo', 'Sin nombre'),
                        'razon': 'Marcado para eliminar'
                    })
                    logger.info(f"Campo editado {campo_id} omitido: está marcado para inactivar")
                    continue
                
                if any(campo.get('id') == campo_id for campo in campos_datos):
                    resultados['campos_omitidos'].append({
                        'id': campo_id,
                        'nombre': campo_data.get('nombre_campo', 'Sin nombre'),
                        'razon': 'Ya procesado en campos_datos'
                    })
                    logger.info(f"Campo editado {campo_id} omitido: ya fue procesado en campos_datos")
                    continue
                
                if _es_campo_nuevo(campo_id):
                    _crear_nuevo_campo(campo_data, formulario_id, resultados)
                elif _es_campo_existente(campo_id):
                    _actualizar_campo_existente(campo_data, resultados)

            for campo_id in campos_inactivar:
                _inactivar_campo(campo_id, resultados)

        mensaje_respuesta = _generar_mensaje_respuesta(resultados)
        
        logger.info(f"Actualización de campos completada para formulario {formulario_id}: {mensaje_respuesta}")
        
        return Response({
            "detail": "Campos actualizados con éxito.",
            "mensaje": mensaje_respuesta,
            "resultados": resultados
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error al actualizar campos del formulario {formulario_id}: {str(e)}")
        return Response({
            "detail": "Error interno al actualizar campos.",
            "errors": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ================== FUNCIONES AUXILIARES PARA OPERACIONES ==================

def _crear_nuevo_campo(campo_data, formulario_id, resultados):
    """
    Crea un nuevo campo en la base de datos
    """
    try:
        # Preparar datos del campo
        campo_data_clean = _normalizar_campo_data(campo_data)
        campo_data_clean.pop('id', None)  # Remover el ID temporal del frontend
        campo_data_clean['formulario_FK'] = formulario_id
        
        # Validar y crear
        serializer = CampoSerializer(data=campo_data_clean)
        if serializer.is_valid():
            campo_creado = serializer.save()
            resultados['campos_creados'].append({
                'id': campo_creado.id,
                'nombre': campo_creado.nombre_campo
            })
            logger.info(f"Campo creado con éxito: {campo_creado.nombre_campo} (ID: {campo_creado.id})")
        else:
            error_msg = f"Error al crear campo '{campo_data.get('nombre_campo', 'Sin nombre')}': {serializer.errors}"
            resultados['errores'].append(error_msg)
            logger.error(error_msg)
            
    except Exception as e:
        error_msg = f"Error al crear campo '{campo_data.get('nombre_campo', 'Sin nombre')}': {str(e)}"
        resultados['errores'].append(error_msg)
        logger.error(error_msg)


def _actualizar_campo_existente(campo_data, resultados):
    """
    Actualiza un campo existente en la base de datos
    """
    try:
        campo_id = campo_data.get('id')

        try:
            campo = Campo.objects.get(id=campo_id)
        except Campo.DoesNotExist:
            error_msg = f"Campo con ID {campo_id} no encontrado para actualizar"
            resultados['errores'].append(error_msg)
            logger.error(error_msg)
            return

        # Preparar datos para actualización
        campo_data_clean = _normalizar_campo_data(campo_data)

        # Actualizar con serializer
        serializer = CampoSerializer(campo, data=campo_data_clean, partial=True)
        if serializer.is_valid():
            campo_actualizado = serializer.save()
            resultados['campos_actualizados'].append({
                'id': campo_actualizado.id,
                'nombre': campo_actualizado.nombre_campo
            })
            logger.info(f"Campo actualizado con éxito: {campo_actualizado.nombre_campo} (ID: {campo_actualizado.id})")
        else:
            error_msg = f"Error al actualizar campo ID {campo_id}: {serializer.errors}"
            resultados['errores'].append(error_msg)
            logger.error(error_msg)
            
    except Exception as e:
        error_msg = f"Error al actualizar campo ID {campo_data.get('id')}: {str(e)}"
        resultados['errores'].append(error_msg)
        logger.error(error_msg)


def _inactivar_campo(campo_id, resultados):
    try:
        if _es_campo_existente(campo_id):
            try:
                campo = Campo.objects.get(id=campo_id)
                campo.estado_campo = False
                campo.save(update_fields=['estado_campo', 'fecha_actualizacion'])
                resultados['campos_inactivados'].append({
                    'id': campo.id,
                    'nombre': campo.nombre_campo
                })
                logger.info(f"Campo inactivado con éxito: {campo.nombre_campo} (ID: {campo.id})")
            except Campo.DoesNotExist:
                logger.info(f"Campo ID {campo_id} no encontrado en BD (probablemente creado y eliminado en frontend)")
        else:
            logger.info(f"Campo temporal {campo_id} no requiere inactivación en BD")
            
    except Exception as e:
        error_msg = f"Error al inactivar campo ID {campo_id}: {str(e)}"
        resultados['errores'].append(error_msg)
        logger.error(error_msg)


def _generar_mensaje_respuesta(resultados):
    """
    Genera un mensaje descriptivo de los resultados de la operación
    """
    mensajes = []
    
    if resultados['campos_creados']:
        mensajes.append(f"{len(resultados['campos_creados'])} campo(s) creado(s)")
    
    if resultados['campos_actualizados']:
        mensajes.append(f"{len(resultados['campos_actualizados'])} campo(s) actualizado(s)")
    
    if resultados['campos_inactivados']:
        mensajes.append(f"{len(resultados['campos_inactivados'])} campo(s) inactivado(s)")
    
    if resultados['campos_omitidos']:
        mensajes.append(f"{len(resultados['campos_omitidos'])} campo(s) omitido(s)")
    
    if resultados['errores']:
        mensajes.append(f"{len(resultados['errores'])} error(es) encontrado(s)")
    
    return ", ".join(mensajes) if mensajes else "No se realizaron cambios"