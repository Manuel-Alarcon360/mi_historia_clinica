import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "historia_clinica.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@admin.com",
        password="admin12345"   # Cambiar esta contraseña por una más segura en producción o en la terminal de render crear un admin conuna contraseña mas segura
    )
    print("Superuser creado")
else:
    print("El superuser ya existe")
