from django.db import models
import logging
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
logger = logging.getLogger(__name__)

class ServicioLanding(models.Model):
    PRIORIDAD_SERVICIO = [
        (1, 'Destacado'),
        (2, 'Relevante'),
        (3, 'General'),
    ]
    nombre_servicio = models.CharField(max_length=50)
    imagen_servicio = models.ImageField(upload_to='servicios/', null=True, blank=True)
    descripcion_servicio = models.CharField(max_length=150, null=True, blank=True)
    prioridad_servicio = models.IntegerField(choices=PRIORIDAD_SERVICIO,default=3)

    mostrar_serv_landing = models.BooleanField(default=True)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicios')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    es_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'Servicios_landing'
        verbose_name_plural = 'Servicios'
        ordering = ['prioridad_servicio', '-fecha_creacion']

    def __str__(self):
        return f"Servicio {self.id} - {self.nombre_servicio}"