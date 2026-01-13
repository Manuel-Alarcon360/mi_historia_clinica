from rest_framework import serializers
from .models import TokenIntegracion, UrlCliente

class TokenIntegracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenIntegracion
        fields = '__all__'


class ClientesSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    apellidos = serializers.CharField(max_length=150)
    numero_identificacion = serializers.CharField(max_length=150)
    tipo_documento = serializers.CharField(max_length=10)
    correo = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    pais = serializers.CharField(max_length=5, default="+57")
    telefono = serializers.CharField(max_length=20)
    direccion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tipo_registro = serializers.CharField(max_length=20, default="")
    compania = serializers.IntegerField()  # ID de la compañía
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class ClientesCreateSerializer(ClientesSerializer):
    """
    Serializer específico para creación de clientes.
    Excluye campos de auditoría que se generan automáticamente.
    """
    class Meta:
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover campos de solo lectura para creación
        self.fields.pop('created_at', None)
        self.fields.pop('updated_at', None)

class UrlClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlCliente
        fields = '__all__'