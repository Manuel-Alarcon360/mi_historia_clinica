from django.db import models


class Formulario(models.Model):
    """
    Modelo para representar formularios dinámicos
    """
    id = models.BigAutoField(primary_key=True)
    nombre_formulario = models.CharField(max_length=250, null=True, blank=True, default=None)
    principal = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)

    class Meta:
        db_table = 'formulario'

    def __str__(self):
        return f"Formulario {self.id} - {self.fecha_creacion}"


class Campo(models.Model):
    """
    Modelo para representar campos de formularios dinámicos
    """

    id = models.BigAutoField(primary_key=True)
    nombre_campo = models.CharField(max_length=250, null=False, blank=False)
    tipo = models.CharField(
        max_length=50, 
        null=False, 
        blank=False
    )
    requerido = models.BooleanField(default=False)
    estado_campo = models.BooleanField(default=True)  # True = activo, False = inactivo
    formulario_FK = models.ForeignKey(
        Formulario,
        on_delete=models.CASCADE,
        db_column='formulario_FK',
        related_name='campos'
    )
    opciones = models.CharField(max_length=2000, null=True, blank=True, default=None)  # Para campos como select, radio, checkbox
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    class Meta:
        db_table = 'campo'

    def __str__(self):
        return f"{self.nombre_campo} ({self.tipo})" 
