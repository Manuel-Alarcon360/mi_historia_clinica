from rest_framework import serializers
from .models import Paciente

class SerializerPaciente(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField() 
    class Meta:
        model = Paciente
        fields = '__all__'

    # def create(self, validated_data):
    #     return Paciente.objects.create(**validated_data)