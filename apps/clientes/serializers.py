from rest_framework import serializers
from .models import ClientesLanding 



class ClienteSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ClientesLanding
        fields = '__all__'