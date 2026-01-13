from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FirmaDigital(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.TextField(max_length=4294967295)  # LONGTEXT en MySQL - Almacena la imagen en base64
    
    class Meta:
        verbose_name = 'Firma Digital'
        verbose_name_plural = 'Firmas Digitales'
    
    def __str__(self):
        return f"Firma de {self.usuario.get_full_name() or self.usuario.username}"