from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = [
        'id',  'fecha_nacimiento', 'estado_civil', 
        'eps', 'vinculacion', 'ocupacion'
    ]
    list_filter = ['estado_civil', 'vinculacion', 'eps']
    search_fields = ['estado_civil', 'vinculacion', 'eps']
    ordering = ['-id']
    
    fieldsets = (
        ('Información Médica', {
            'fields': ('fecha_nacimiento', 'estado_civil', 'eps', 'vinculacion')
        }),
        ('Información Adicional', {
            'fields': ('ocupacion', 'responsable', 'tel_responsable')
        }),
    )
    