from django.db import models
from datetime import date

class Paciente(models.Model):
    """
    Modelo para representar los pacientes del sistema
    """
    ESTADO_CIVIL_CHOICES = [
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('union_libre', 'Unión Libre'),
        ('divorciado', 'Divorciado/a'),
        ('viudo', 'Viudo/a'),
        ('separado', 'Separado/a'),
    ]
    id = models.BigAutoField(primary_key=True)
    fecha_nacimiento = models.DateField(null=False, blank=False, default=date.today)
    estado_civil = models.CharField(
        max_length=20, 
        choices=ESTADO_CIVIL_CHOICES, 
        null=False, 
        blank=False
    )
    eps = models.CharField(max_length=100, null=False, blank=False)
    vinculacion = models.CharField(
        max_length=15,  
        null=False, 
        blank=False
    )
    ocupacion = models.CharField(max_length=250, null=False, blank=False)
    responsable = models.CharField(max_length=250, null=True, blank=True)
    tel_responsable = models.CharField(max_length=30, null=True, blank=True)
    cliente_FK = models.IntegerField(null=False, blank=False)
    class Meta:
        db_table = 'paciente'

    def __str__(self):
        return f"Paciente {self.id}"

    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
