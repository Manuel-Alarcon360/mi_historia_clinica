from django.db import models
import logging
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
logger = logging.getLogger(__name__)

class ClientesLanding(models.Model):
    PRIORIDAD_CLIENTE = [
        (1, 'Destacado'),
        (2, 'Relevante'),
        (3, 'General'),
    ]
    nombre_cliente = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User,on_delete=models.CASCADE,related_name='clientes')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    descripcion_cliente = models.TextField(max_length=200)
    prioridad_cliente = models.IntegerField(choices=PRIORIDAD_CLIENTE,default=3)
    
    mostrar_cl_landing = models.BooleanField(default=True)
    imagen_cliente = models.ImageField(upload_to='clientes/',null=True,blank=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'Clientes_landing'
        verbose_name_plural = 'Clientes'
        ordering = ['prioridad_cliente', '-fecha_creacion']
        
    def __str__(self):
        return f"Cliente {self.id} - {self.nombre_cliente}"
