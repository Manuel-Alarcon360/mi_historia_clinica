from django.contrib import admin
from .models import TokenIntegracion


@admin.register(TokenIntegracion)
class TokenIntegracionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_aplicacion', 'token_masked']
    search_fields = ['nombre_aplicacion']
    ordering = ['nombre_aplicacion']
    
    def token_masked(self, obj):
        # Mostrar solo los primeros y últimos caracteres del token por seguridad
        token = obj.token_aplicacion
        if len(token) > 10:
            return f"{token[:5]}...{token[-5:]}"
        return token[:3] + "..."
    token_masked.short_description = 'Token (parcial)'
