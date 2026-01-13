# Guía de Configuración y Deployment

## 🚀 Guía Rápida de Instalación

### Requisitos del Sistema

**Hardware Mínimo:**
- CPU: 2 cores
- RAM: 4 GB
- Almacenamiento: 20 GB

**Software Requerido:**
- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes)
- Git

---

## 📦 Instalación Paso a Paso

### 1. Preparar el Entorno

**Windows:**
```powershell
# Verificar versión de Python
python --version

# Crear directorio del proyecto
mkdir C:\proyectos\historia_clinica
cd C:\proyectos\historia_clinica

# Clonar repositorio
git clone <url-repositorio> .

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Verificar versión de Python
python3 --version

# Crear directorio del proyecto
mkdir -p ~/proyectos/historia_clinica
cd ~/proyectos/historia_clinica

# Clonar repositorio
git clone <url-repositorio> .

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

**Si hay errores con mysqlclient:**

**Windows:**
```powershell
# Descargar e instalar MySQL Connector
# Desde: https://dev.mysql.com/downloads/connector/python/
pip install mysqlclient
```

**Linux:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**Mac:**
```bash
brew install mysql
pip install mysqlclient
```

### 3. Configurar Base de Datos MySQL

**Crear base de datos:**
```sql
-- Conectarse a MySQL
mysql -u root -p

-- Crear base de datos
CREATE DATABASE historia_clinica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario (opcional)
CREATE USER 'hc_user'@'localhost' IDENTIFIED BY 'password_seguro';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON historia_clinica.* TO 'hc_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Seguridad
SECRET_KEY=django-insecure-tu-clave-secreta-aqui-cambiar-en-produccion
DEBUG=True

# Base de Datos
DB_NAME=historia_clinica
DB_USER=hc_user
DB_PASSWORD=password_seguro
DB_HOST=localhost
DB_PORT=3306

# Integración Externa
URL_CLIENTES_EXTERNOS=http://127.0.0.1:8000/api/
```

**Generar SECRET_KEY segura:**
```python
# En terminal Python
python
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### 5. Ejecutar Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar estado de migraciones
python manage.py showmigrations
```

**Salida esperada:**
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
...
usuario
 [X] 0001_initial
paciente
 [X] 0001_initial
 [X] 0002_alter_paciente_fecha_nacimiento_and_more
...
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Proporcionar:
- **Username:** admin@ejemplo.com
- **Email:** admin@ejemplo.com
- **Password:** (contraseña segura)
- **Password (again):** (repetir contraseña)

### 7. Cargar Datos Iniciales (Opcional)

**Crear grupos/roles:**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group

# Crear grupos
Group.objects.create(name='Médico')
Group.objects.create(name='Enfermero')
Group.objects.create(name='Administrador')

# Verificar
print(Group.objects.all())

# Salir
exit()
```

### 8. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

**Verificar que el servidor esté corriendo:**
- Backend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

---

## 🔧 Configuración Avanzada

### Configurar CORS para Frontend

Editar `historia_clinica/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",      # Angular
    "http://localhost:3000",      # React
    "http://localhost:8080",      # Vue
    "http://192.168.1.100:4200", # IP local
]

CORS_ALLOW_CREDENTIALS = True
```

### Configurar Archivos Media

Los archivos de firma digital se almacenan en:

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'firmas_digitales'
```

**Crear directorio:**
```bash
mkdir firmas_digitales
```

### Configurar Logging Avanzado

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

**Crear directorio de logs:**
```bash
mkdir logs
```

---

## 🌐 Deployment en Producción

### Preparación para Producción

#### 1. Actualizar settings.py

```python
# settings.py - Producción
DEBUG = False

ALLOWED_HOSTS = [
    'tudominio.com',
    'www.tudominio.com',
    'api.tudominio.com',
]

# Seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Base de datos optimizada
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 600,  # Conexiones persistentes
    }
}
```

#### 2. Configurar Archivos Estáticos

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'
```

**Recopilar archivos estáticos:**
```bash
python manage.py collectstatic
```

### Deployment con Gunicorn + Nginx

#### 1. Instalar Gunicorn

```bash
pip install gunicorn
pip freeze > requirements.txt
```

#### 2. Crear archivo de configuración Gunicorn

**gunicorn_config.py:**
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
loglevel = "info"
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
```

#### 3. Configurar Nginx

**/etc/nginx/sites-available/historia_clinica:**
```nginx
upstream historia_clinica {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name tudominio.com www.tudominio.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /ruta/completa/historia_clinica/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /ruta/completa/historia_clinica/mediafiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://historia_clinica;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

**Activar sitio:**
```bash
sudo ln -s /etc/nginx/sites-available/historia_clinica /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Configurar Systemd Service

**/etc/systemd/system/historia_clinica.service:**
```ini
[Unit]
Description=Historia Clinica Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/ruta/completa/historia_clinica
ExecStart=/ruta/completa/historia_clinica/venv/bin/gunicorn \
    --config gunicorn_config.py \
    historia_clinica.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Iniciar servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl start historia_clinica
sudo systemctl enable historia_clinica
sudo systemctl status historia_clinica
```

#### 5. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Renovación automática
sudo certbot renew --dry-run
```

---

## 🐳 Deployment con Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Crear directorios
RUN mkdir -p logs firmas_digitales staticfiles

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--config", "gunicorn_config.py", "historia_clinica.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: historia_clinica
      MYSQL_USER: hc_user
      MYSQL_PASSWORD: password_seguro
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    networks:
      - historia_network

  web:
    build: .
    command: gunicorn --config gunicorn_config.py historia_clinica.wsgi:application
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    networks:
      - historia_network

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web
    networks:
      - historia_network

volumes:
  mysql_data:
  static_volume:
  media_volume:

networks:
  historia_network:
    driver: bridge
```

### Comandos Docker

```bash
# Construir imagen
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

## 📊 Monitoreo y Mantenimiento

### Backup de Base de Datos

**Script de backup automático (backup.sh):**
```bash
#!/bin/bash

# Variables
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/backups/historia_clinica"
DB_NAME="historia_clinica"
DB_USER="hc_user"
DB_PASS="password_seguro"

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Realizar backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/backup_$DATE.sql

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completado: backup_$DATE.sql.gz"
```

**Configurar cron:**
```bash
# Editar crontab
crontab -e

# Backup diario a las 2 AM
0 2 * * * /ruta/completa/backup.sh
```

### Monitoreo de Logs

**Script de monitoreo (monitor.sh):**
```bash
#!/bin/bash

# Monitorear errores en logs
tail -f logs/django.log | grep -i error

# O usar herramientas como:
# - Logwatch
# - Logrotate
# - ELK Stack
```

### Health Check

**health_check.py:**
```python
# Crear endpoint de health check
# En urls.py principal

from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Verificar conexión a BD
        connection.ensure_connection()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)

# Agregar a urlpatterns
path('health/', health_check, name='health_check'),
```

---

## 🔍 Troubleshooting

### Problemas Comunes

#### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
# O en Ubuntu/Debian:
sudo apt-get install python3-dev default-libmysqlclient-dev
pip install mysqlclient
```

#### Error: "Can't connect to MySQL server"
```bash
# Verificar que MySQL esté corriendo
sudo systemctl status mysql

# Verificar credenciales en .env
# Verificar que el usuario tenga permisos
```

#### Error: "CSRF verification failed"
```python
# settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://tudominio.com',
    'https://www.tudominio.com',
]
```

#### Error: "Media files not found"
```python
# En urls.py (solo desarrollo)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📈 Optimización de Performance

### 1. Configurar Caché con Redis

**Instalar Redis:**
```bash
pip install django-redis
```

**Configurar en settings.py:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2. Optimizar Queries

```python
# Usar select_related para ForeignKey
pacientes = Paciente.objects.select_related('usuario_fk').all()

# Usar prefetch_related para ManyToMany
historias = HistoriaClinica.objects.prefetch_related('detalles').all()

# Usar only() para campos específicos
pacientes = Paciente.objects.only('id', 'nombre', 'apellido')
```

### 3. Configurar Connection Pooling

```python
# settings.py
DATABASES = {
    'default': {
        # ... otras configuraciones
        'CONN_MAX_AGE': 600,  # 10 minutos
    }
}
```

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad

- [ ] DEBUG=False
- [ ] SECRET_KEY única y segura
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS habilitado
- [ ] CSRF protección activa
- [ ] SQL Injection protección (ORM)
- [ ] XSS protección
- [ ] Firewall configurado
- [ ] Rate limiting implementado
- [ ] Logs de seguridad activos
- [ ] Backups automáticos
- [ ] Actualizaciones regulares

### Implementar Rate Limiting

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h')
def mi_vista(request):
    # ...
```

---

## 📞 Soporte y Recursos

- **Documentación Django:** https://docs.djangoproject.com/
- **Documentación DRF:** https://www.django-rest-framework.org/
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/django

---

**Última actualización: Noviembre 2025**
