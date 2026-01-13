from django.db import models


class TokenIntegracion(models.Model):
    """
    Modelo para manejar tokens de integración con aplicaciones externas
    """
    id = models.BigAutoField(primary_key=True)
    nombre_aplicacion = models.CharField(max_length=100, null=False, blank=False)
    token_aplicacion = models.CharField(max_length=300, null=False, blank=False)

    class Meta:
        db_table = 'token_integracion'

    def __str__(self):
        return f"Token para {self.nombre_aplicacion}"

class UrlCliente(models.Model):
    """
    Modelo para manejar URLs de clientes asociados a integraciones
    """
    id = models.BigAutoField(primary_key=True)
    url_cliente = models.URLField(max_length=300, null=False, blank=False)

    class Meta:
        db_table = 'url_cliente'
