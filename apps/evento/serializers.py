from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):    #ok
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError(
                "La fecha fin no puede ser menor que la fecha inicio."
            )

        return data


