from django.db import models
from apps.paciente.models import Paciente
from apps.formulario.models import Formulario, Campo


class HistoriaClinica(models.Model):
    """
    Modelo para representar las historias clínicas
    """
    id = models.BigAutoField(primary_key=True)
    paciente_fk = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        db_column='paciente_fk',
        related_name='historias_clinicas'
    )
    motivo_consulta = models.CharField(max_length=500, null=False, blank=False)
    doctor = models.CharField(max_length=50, null=False, blank=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    class Meta:
        db_table = 'historia_clinica'

    def __str__(self):
        return f"Historia Clínica {self.id}"


class DetalleHistoria(models.Model):
    """
    Modelo para representar los detalles/respuestas de una historia clínica
    """
    id = models.BigAutoField(primary_key=True)
    historia_fk = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.PROTECT,
        db_column='historia_fk',
        related_name='detalles'
    )
    respuesta_campo = models.CharField(max_length=1000, null=False, blank=False)
    formulario_fk = models.ForeignKey(
        Formulario,
        on_delete=models.PROTECT,
        db_column='formulario_fk',
        related_name='respuestas'
    )
    campo_fk = models.ForeignKey(
        Campo,
        on_delete=models.PROTECT,
        db_column='campo_fk',
        related_name='respuestas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'detalle_historia'

    def __str__(self):
        return f"Detalle {self.id} - Historia {self.historia_fk.id} - Campo {self.campo_fk.nombre_campo}"
