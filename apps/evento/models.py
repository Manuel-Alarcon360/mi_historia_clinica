from django.db import models
import logging
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
logger = logging.getLogger(__name__)
class Evento(models.Model):
    TIPO_EVENTO = [
        ('promo', 'Promoción'),
        ('aviso', 'Aviso'),
        ('evento', 'Evento'),
        ('campania', 'Campaña de salud visual'),
        ('horario', 'Horario especial'),
        ('servicio', 'Nuevo servicio'),
    ]
    titulo = models.CharField(max_length=200)
    tipo_evento = models.CharField(max_length=30,choices=TIPO_EVENTO,default='evento')
    descripcion = models.TextField()
    imagen_evento = models.ImageField(upload_to='eventos/',null=True,blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    mostrar_en_landing = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User,on_delete=models.CASCADE,related_name='eventos')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    es_principal = models.BooleanField(default=False,null=True)
    
    class Meta:
        db_table = 'Eventos'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_inicio', '-id']
        
    def __str__(self):
        return f"Evento {self.id}"