from django.contrib import admin
from .models import HistoriaClinicaAuditoria


@admin.register(HistoriaClinicaAuditoria)
class HistoriaClinicaAuditoriaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'historia_id',  'accion', 
        'campo_modificado', 'get_usuario', 'ip_origen', 'fecha_evento'
    ]
    list_filter = ['accion', 'fecha_evento', 'campo_modificado']
    search_fields = [
        'historia_id', 'paciente_fk__cliente_FK__nombre',
        'usuario_id__username', 'campo_modificado'
    ]
    ordering = ['-fecha_evento']
    readonly_fields = [
        'historia_id', 'paciente_fk', 'compania_id', 'accion',
        'campo_modificado', 'valor_anterior', 'valor_nuevo',
        'usuario_id', 'ip_origen', 'fecha_evento'
    ]
    
    fieldsets = (
        ('Información de la Historia', {
            'fields': ('historia_id', 'paciente_fk', 'compania_id')
        }),
        ('Detalles del Cambio', {
            'fields': ('accion', 'campo_modificado', 'valor_anterior', 'valor_nuevo')
        }),
        ('Información de Auditoría', {
            'fields': ('usuario_id', 'ip_origen', 'fecha_evento')
        }),
    )
    
    
    def get_usuario(self, obj):
        return obj.usuario_id.username
    get_usuario.short_description = 'Usuario'
    
    def has_add_permission(self, request):
        # No permitir agregar registros de auditoría manualmente
        return False
    
    def has_change_permission(self, request, obj=None):
        # No permitir modificar registros de auditoría
        return False
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar registros de auditoría
        return False
