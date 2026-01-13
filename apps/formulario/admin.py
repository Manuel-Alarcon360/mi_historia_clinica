from django.contrib import admin
from .models import Formulario, Campo


class CampoInline(admin.TabularInline):
    model = Campo
    extra = 1
    fields = ['nombre_campo', 'tipo', 'requerido', 'estado_campo']


@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_creacion', 'fecha_actualizacion', 'get_num_campos']
    list_filter = ['fecha_creacion', 'fecha_actualizacion']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [CampoInline]
    
    def get_num_campos(self, obj):
        return obj.campos.count()
    get_num_campos.short_description = 'Número de Campos'


@admin.register(Campo)
class CampoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'nombre_campo', 'tipo', 'requerido', 
        'estado_campo', 'formulario_FK'
    ]
    list_filter = ['tipo', 'requerido', 'estado_campo']
    search_fields = ['nombre_campo']
    ordering = ['formulario_FK', 'id']
