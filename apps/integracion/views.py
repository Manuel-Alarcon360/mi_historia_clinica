import requests
import json
from rest_framework import generics
from .models import TokenIntegracion, UrlCliente
from .serializer import TokenIntegracionSerializer, UrlClienteSerializer
import historia_clinica.settings as settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Create your views here.


class TokenIntegracionListCreateView(generics.ListCreateAPIView):
    queryset = TokenIntegracion.objects.all()
    serializer_class = TokenIntegracionSerializer


class TokenIntegracionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TokenIntegracion.objects.all()
    serializer_class = TokenIntegracionSerializer


def obtener_token_aplicacion(nombre_aplicacion):
    try:
        token_obj = TokenIntegracion.objects.get(nombre_aplicacion=nombre_aplicacion)
        return token_obj.token_aplicacion
    except TokenIntegracion.DoesNotExist:
        return None


def _construir_uri_con_paginacion(request, uri: str):
    page_number = request.GET.get("page")

    if page_number and page_number.isdigit() and int(page_number) > 0:
        uri += f"?page={page_number}"
    return uri


def _construir_uri_con_filtros(request, uri: str):
    filtros = request.GET.get("query")
    if filtros:
        uri += f"?query={filtros}"
    return uri


def _realizar_peticion_externa(token, uri):
    headers = {
        "Authorization": f"token_app {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    url = settings.URL_CLIENTES_EXTERNOS + uri

    return requests.get(url=url, headers=headers, timeout=30)


def _peticion_post_externa(token, uri, data):
    headers = {
        "Authorization": f"token_app {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    url = settings.URL_CLIENTES_EXTERNOS + uri

    return requests.post(url=url, headers=headers, json=data, timeout=30)


def _procesar_respuesta_externa(response):
    if response.status_code == 200:
        try:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response(
                {"error": "Respuesta inválida del servicio externo"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
    elif response.status_code == 401:
        return Response(
            {"error": "Token de autenticación inválido o expirado"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    elif response.status_code == 404:
        return Response(
            {"error": "Recurso no encontrado en el servicio externo"},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        return Response(
            {"error": f"Error del servicio externo: {response.status_code}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )


@api_view(["GET"])
def obtener_clientes_externos(request):
    try:
        token = obtener_token_aplicacion("DoCalendar")
        if not token:
            return Response(
                {"error": "Token de autenticación no encontrado para DoCalendar"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        uri = _construir_uri_con_paginacion(request, "clientes/list_cliente/")
        response = _realizar_peticion_externa(token, uri)
        return _procesar_respuesta_externa(response)

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Error de conexión con el servicio externo: {str(e)}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except Exception as e:
        return Response(
            {"error": f"Error interno del servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def obtener_citas(request):
    try:
        token = obtener_token_aplicacion("DoCalendar")
        if not token:
            return Response(
                {"error": "Token de autenticación no encontrado para DoCalendar"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        uri = _construir_uri_con_paginacion(request, "compania/dashboard/")
        response = _realizar_peticion_externa(token, uri)

        data = {
            "results": response.json().get("citas", {}).get("citas_agendadas", []),
            "count": len(response.json().get("citas", {}).get("citas_agendadas", [])),
            "next": None,
            "previous": None,
        }
        return Response(data, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Error de conexión con el servicio externo: {str(e)}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except Exception as e:
        return Response(
            {"error": f"Error interno del servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def create_cliente_externo(request):
    try:
        token = obtener_token_aplicacion("DoCalendar")
        if not token:
            return Response(
                {"error": "Token de autenticación no encontrado para DoCalendar"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        uri = "clientes/create_cliente/"
        data = request.data
        response = _peticion_post_externa(token, uri, data)
        return Response(response.json(), status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Error de conexión con el servicio externo: {str(e)}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET"])
def consultar_cliente(request):
    try:
        token = obtener_token_aplicacion("DoCalendar")
        if not token:
            return Response({"error": "Token de autenticación no encontrado para DoCalendar"}, status=status.HTTP_401_UNAUTHORIZED)
        uri = _construir_uri_con_filtros(request, "clientes/busqueda_clientes/")
        response = _realizar_peticion_externa(token, uri)
        data = {
            "results": response.json(),
            "count": len(response.json()),
            "next": None,
            "previous": None,
        }
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Error de conexión con el servicio externo: {str(e)}"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def obtener_urls_clientes(request): 
    url_disponible = UrlCliente.objects.all()
    serializer_data = UrlClienteSerializer(url_disponible, many=True)
    return Response({
        "details": "Lista de URLs de clientes",
        "data": serializer_data.data
    }, status=status.HTTP_200_OK)