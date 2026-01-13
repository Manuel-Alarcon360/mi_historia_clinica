from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from apps.usuario.serializer import SerializerUsuario, SerializerEmpleado, SerializerGroups, SerializerUpdateUsuario, FirmaDigitalSerializer
from .models import FirmaDigital
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

# Register users
class Register(APIView):
    def post(self, request):
        data = request.data.copy()
        role_id = data.get('id_rol')
        
        # Si id_rol viene como lista, extraer el primer elemento
        if isinstance(role_id, list):
            role_id = role_id[0] if role_id else None
        
        if not role_id:
            return Response({
                "detail": "El campo id_rol es obligatorio.",
                "errors": {"id_rol": ["Este campo es obligatorio."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            role_id = int(role_id)
        except (ValueError, TypeError):
            return Response({
                "detail": "El id_rol debe ser un número válido.",
                "errors": {"id_rol": ["El id_rol debe ser un número válido."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        role = get_object_or_404(Group, id=role_id)
        
        # Preparar datos para el serializador
        data['groups'] = [role_id]  # Asignar directamente como lista
        data['is_active'] = True
        data['username'] = data.get("email", "")
        
        logger.info(f"Datos para registro: {data}")
        
        info = {
             'first_name': data.get('first_name', ''),
             'last_name': data.get('last_name', ''),
             'password': data.get('password', ''),
             'email': data.get('email', ''),
             'groups': [role_id],
             'is_active': True,
             'username': data.get("email", "")
         }
        serializer = SerializerUsuario(data=info)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"Usuario {user.username} registrado exitosamente con rol {role.name}")
            
            # Crear firma digital si se proporciona imagen en base64
            if 'imagen' in data:
                try:
                    crear_firma_digital({'usuario': user.id, 'imagen': data['imagen']})
                except Exception as e:
                    logger.error(f"Error al crear firma digital: {str(e)}", exc_info=True)
            
            return Response({
                "detail": "Usuario registrado exitosamente.",
                "user_id": user.id,
                "username": user.username,
                "rol": role.name
            }, status=status.HTTP_201_CREATED)

        logger.error(f"Error en la validación de datos: {str(serializer.errors)}", exc_info=True)
        return Response({
            "detail": "Error en la validación de datos.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateEstadoEmpleado(generics.UpdateAPIView):
    queryset = User
    serializer_class = SerializerEmpleado
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            response = super().update(request, *args, **kwargs)
            
            action = "activado" if user.is_active else "desactivado"
            logger.info(f"Usuario {user.username} {action} exitosamente")
            
            return response
            
        except Exception as e:
            logger.error(f"Error al actualizar estado de usuario: {str(e)}", exc_info=True)
            return Response({
                "detail": "Error interno del servidor.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListGroupsAvailable(generics.ListAPIView):
    queryset = Group.objects.all().order_by('name')
    serializer_class = SerializerGroups
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f"Lista de grupos disponible: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error al listar grupos: {str(e)}", exc_info=True)
            return Response({
                "detail": "Error interno del servidor.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class listUsuarios(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = SerializerUsuario
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f"Lista de usuarios obtenida exitosamente")
            return response
        except Exception as e:
            logger.error(f"Error al listar usuarios: {str(e)}", exc_info=True)
            return Response({
                "detail": "Error interno del servidor.",
                "error_code": "INTERNAL_SERVER_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['PUT'])
def update_colaboradores(request, pk):
    try:
        role_id = request.data.get('id_rol')
        if not role_id:
            logger.error(f"Campo id_rol faltante en la solicitud de actualización: {request.data}")
            return Response({
                "detail": "El campo id_rol es obligatorio.",
                "errors": {"id_rol": ["Este campo es obligatorio."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.get(id=pk)
        logger.info(f"Colaborador obtenido exitosamente: {users.username}")
        request.data['username'] = request.data.get('email')
        request.data['groups'] = [request.data.get('id_rol')]
        serializer = SerializerUpdateUsuario(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
                      
            # Manejar firma digital en base64
            if 'imagen' in request.data:
                logger.info("Actualizando o creando firma digital...")
                try:
                    firma = FirmaDigital.objects.filter(usuario__id=pk).first()
                    firma_data = {'imagen': request.data['imagen']}
                    
                    if firma:
                        actualizar_firma_digital(firma_data, firma)
                    else:
                        data_firma = {'usuario': pk, 'imagen': request.data['imagen']}
                        crear_firma_digital(data_firma)
                except Exception as e:
                    logger.error(f"Error al procesar firma digital: {str(e)}", exc_info=True)
            
            logger.info(f"Colaborador actualizado exitosamente: {users.username}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error al listar colaboradores: {str(e)}", exc_info=True)
        return Response({
            "detail": "Error interno del servidor.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def change_password(request, pk):
    try:
        user = User.objects.get(id=pk)
        logger.info(f"Usuario para cambio de contraseña obtenido exitosamente: {user.username}")
        new_password = request.data.get('password')
        if not new_password:
            logger.error(f"Campo password faltante en la solicitud de cambio de contraseña: {request.data}")
            return Response({
                "detail": "El campo password es obligatorio.",
                "errors": {"password": ["Este campo es obligatorio."]}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        logger.info(f"Contraseña cambiada exitosamente para el usuario: {user.username}")
        return Response({"detail": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        logger.error(f"Usuario con id {pk} no encontrado para cambio de contraseña.")
        return Response({
            "detail": "Usuario no encontrado.",
            "error_code": "USER_NOT_FOUND"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error al cambiar la contraseña: {str(e)}", exc_info=True)
        return Response({
            "detail": "Error interno del servidor.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def obtener_firma_digital(request):
        logger.info(f"Solicitud para obtener firma digital del usuario: {request.user.username}")
        usuario = request.user.id
        firma = get_object_or_404(FirmaDigital, usuario__id=usuario)
        serializer = FirmaDigitalSerializer(firma, context={'request': request})
        return Response({
            "detail": "Firma digital obtenida exitosamente.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def controller_firma_digital(request):
    try:
        usuario = request.user.id
        firma = FirmaDigital.objects.filter(usuario__id=usuario).first()
        data = {'usuario': usuario, 'imagen': request.data.get('imagen')}
        
        if firma:
            return actualizar_firma_digital(data, firma)
        else:
            return crear_firma_digital(data)
    except Exception as e:
        logger.error(f"Error en el controlador de firma digital: {str(e)}", exc_info=True)
        return Response({
            "detail": "Error interno del servidor.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def crear_firma_digital(request):
    try:
        logger.info(f"Solicitud para crear firma digital del usuario: {request.get('usuario')}")
        data = request
        serializer = FirmaDigitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Firma digital creada exitosamente para el usuario: {request.get('usuario')}")
            return Response({
                "detail": "Firma digital creada exitosamente.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        logger.error(f"Error en la validación de datos para crear firma digital: {str(serializer.errors)}", exc_info=True)
        return Response({
            "detail": "Error en la validación de datos.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error al crear la firma digital: {str(e)}", exc_info=True)
        return Response({
            "detail": "Error interno del servidor.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def actualizar_firma_digital(request, object: FirmaDigital):
    try:
        logger.info(f"Solicitud para actualizar firma digital del usuario: {object.usuario.id}")
        data = request
        serializer = FirmaDigitalSerializer(object, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Firma digital actualizada exitosamente para el usuario: {object.usuario.id}")
            return Response({
                "detail": "Firma digital actualizada exitosamente.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        logger.error(f"Error en la validación de datos para actualizar firma digital: {str(serializer.errors)}", exc_info=True)
        return Response({
            "detail": "Error en la validación de datos.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error al actualizar la firma digital: {str(e)}", exc_info=True)
        return Response({
            "detail": "Error interno del servidor.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)