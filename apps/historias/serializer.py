from rest_framework import serializers 
from .models import HistoriaClinica, DetalleHistoria

class HistoriaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'


class DetalleHistoriaSerializer(serializers.ModelSerializer):
    label_input = serializers.CharField(read_only=True)
    class Meta:
        model = DetalleHistoria
        fields = '__all__'