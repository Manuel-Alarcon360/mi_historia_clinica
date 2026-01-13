from django.db import models
from django.contrib.auth.models import User
from apps.historias.models import HistoriaClinica
from apps.paciente.models import Paciente


class HistoriaClinicaAuditoria(models.Model):
    """
    Modelo para auditoría de cambios en historias clínicas
    """
    ACCION_CHOICES = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('VIEW', 'Consulta'),
    ]

    id = models.BigAutoField(primary_key=True)
    historia_id = models.IntegerField(null=False, blank=False)
    paciente_fk = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        db_column='paciente_fk',
        related_name='auditorias'
    )
    compania_id = models.IntegerField(null=False, blank=False)
    accion = models.CharField(
        max_length=20, 
        choices=ACCION_CHOICES, 
        null=False, 
        blank=False
    )
    campo_modificado = models.CharField(max_length=100, null=False, blank=False)
    valor_anterior = models.CharField(max_length=500, null=False, blank=False)
    valor_nuevo = models.CharField(max_length=500, null=False, blank=False)
    usuario_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='usuario_id',
        related_name='auditorias_historia'
    )
    ip_origen = models.GenericIPAddressField(null=False, blank=False)
    fecha_evento = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'historia_clinica_auditoria'

    def __str__(self):
        return f"Auditoría {self.id} - {self.accion} - Historia {self.historia_id}"
