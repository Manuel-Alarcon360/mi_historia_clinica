from django.contrib import admin
from .models import HistoriaClinica, DetalleHistoria


class DetalleHistoriaInline(admin.TabularInline):
    model = DetalleHistoria
    extra = 0
    fields = ['formulario_fk', 'campo_fk', 'respuesta_campo']
    readonly_fields = ['fecha_creacion']


@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'doctor', 'fecha_creacion',
        'fecha_actualizacion'
    ]
    list_filter = ['doctor', 'fecha_creacion', 'fecha_actualizacion']
    search_fields = [
        'paciente_fk__cliente_FK__nombre', 
        'paciente_fk__cliente_FK__apellidos',
        'doctor', 'motivo_consulta'
    ]
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [DetalleHistoriaInline]
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('paciente_fk',)
        }),
        ('Información Médica', {
            'fields': ('doctor', 'motivo_consulta', 'antecedentes', 'observaciones')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion')
        }),
    )
    


@admin.register(DetalleHistoria)
class DetalleHistoriaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'get_campo_nombre', 
        'respuesta_campo', 'fecha_creacion'
    ]
    list_filter = ['formulario_fk', 'fecha_creacion']
    search_fields = [
        'historia_fk__paciente_fk__cliente_FK__nombre',
        'campo_fk__nombre_campo', 'respuesta_campo'
    ]
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']
    
    def get_campo_nombre(self, obj):
        return obj.campo_fk.nombre_campo
    get_campo_nombre.short_description = 'Campo'
