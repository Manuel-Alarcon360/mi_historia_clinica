from rest_framework import serializers
from .models import ServicioLanding

class ServicioSerializer(serializers.ModelSerializer):
    creado_por = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ServicioLanding
        fields = '__all__'