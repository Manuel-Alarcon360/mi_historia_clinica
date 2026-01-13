# Arquitectura del Sistema - Historia Clínica

## 📐 Visión General de la Arquitectura

El sistema de Historia Clínica sigue los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**, organizado en módulos independientes que se comunican a través de interfaces bien definidas.

---

## 🏗️ Capas de la Arquitectura

### 1. Capa de Presentación (API Layer)
**Responsabilidad:** Exponer endpoints RESTful y manejar requests/responses HTTP.

**Componentes:**
- `views.py`: Controladores que manejan las peticiones HTTP
- `urls.py`: Definición de rutas y endpoints
- Validación de entrada
- Serialización de respuestas

**Tecnologías:**
- Django REST Framework
- JWT Authentication

### 2. Capa de Aplicación (Business Logic Layer)
**Responsabilidad:** Implementar la lógica de negocio y orquestar casos de uso.

**Componentes:**
- Validaciones de negocio
- Transformación de datos
- Coordinación entre modelos
- Manejo de transacciones

**Ejemplo:**
```python
# En views.py - Lógica de negocio
def _crear_paciente_si_no_existe(data):
    # Validar existencia
    paciente_existente = _validar_paciente_existente(cliente)
    if paciente_existente:
        return _actualizar_paciente_existente(paciente_existente, data)
    # Crear nuevo
    return _crear_nuevo_paciente(data)
```

### 3. Capa de Dominio (Domain Layer)
**Responsabilidad:** Definir las entidades del negocio y sus relaciones.

**Componentes:**
- `models.py`: Modelos de Django que representan entidades del dominio
- Propiedades calculadas
- Métodos de dominio

**Ejemplo:**
```python
class Paciente(models.Model):
    # Campos del modelo
    fecha_nacimiento = models.DateField()
    
    @property
    def edad(self):
        # Lógica de dominio
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year
        return None
```

### 4. Capa de Infraestructura (Infrastructure Layer)
**Responsabilidad:** Implementar comunicación con recursos externos.

**Componentes:**
- Base de datos (MySQL)
- Sistema de archivos (firmas digitales)
- APIs externas (DoCalendar)
- Logging y auditoría

---

## 📦 Estructura Modular

### Módulos del Sistema

```
apps/
├── usuario/           # Gestión de usuarios y autenticación
├── paciente/          # Gestión de pacientes
├── formulario/        # Formularios dinámicos
├── historias/         # Historias clínicas
├── integracion/       # Integración externa
└── auditoria/         # Auditoría y trazabilidad
```

### Principios de Modularidad

1. **Alta Cohesión:** Cada módulo tiene una responsabilidad única y bien definida
2. **Bajo Acoplamiento:** Los módulos se comunican a través de interfaces estables
3. **Independencia:** Cada módulo puede funcionar de forma autónoma
4. **Escalabilidad:** Facilita la adición de nuevas funcionalidades

---

## 🔄 Flujo de Datos

### Flujo de una Petición HTTP

```
Cliente HTTP
    ↓
[Middleware - CORS, Auth]
    ↓
[URL Dispatcher]
    ↓
[View - Validación de entrada]
    ↓
[Serializer - Validación de datos]
    ↓
[Business Logic - Procesamiento]
    ↓
[Model - Persistencia]
    ↓
[Database]
    ↓
[Model - Recuperación]
    ↓
[Serializer - Transformación]
    ↓
[View - Preparación de respuesta]
    ↓
[Response HTTP]
```

### Ejemplo Concreto: Crear Historia Clínica

```
POST /api/historia/crear_historia_clinica/
    ↓
1. JWT Middleware valida token
    ↓
2. create_historias.post() recibe request
    ↓
3. _crear_paciente_si_no_existe() valida/crea paciente
    ↓
4. HistoriaClinicaSerializer valida datos
    ↓
5. HistoriaClinica.objects.create() persiste
    ↓
6. _registrar_detalle_historia_clinica() crea detalles
    ↓
7. DetalleHistoria.objects.create() persiste cada campo
    ↓
8. Logger registra operación
    ↓
9. Response con IDs creados
```

---

## 🗄️ Diseño de Base de Datos

### Diagrama Entidad-Relación (Simplificado)

```
┌─────────────────┐
│      User       │
│ (Django Auth)   │
└────────┬────────┘
         │ 1
         │
         │ 1
┌────────▼────────┐
│ FirmaDigital    │
└─────────────────┘

┌─────────────────┐         ┌──────────────────┐
│   Formulario    │ 1     * │      Campo       │
│                 ├─────────┤                  │
└─────────────────┘         └────────┬─────────┘
                                     │ *
                                     │
                                     │ 1
                            ┌────────▼─────────┐
┌─────────────────┐         │ DetalleHistoria  │
│    Paciente     │ 1       │                  │
│                 │         └────────┬─────────┘
└────────┬────────┘                  │ *
         │ 1                         │
         │                           │ 1
         │ *               ┌─────────▼──────────┐
         └─────────────────┤ HistoriaClinica    │
                           │                    │
                           └────────────────────┘
```

### Relaciones Clave

1. **Usuario → FirmaDigital** (1:1)
   - Cada usuario puede tener una firma digital

2. **Paciente → HistoriaClinica** (1:N)
   - Un paciente puede tener múltiples historias clínicas

3. **Formulario → Campo** (1:N)
   - Un formulario contiene múltiples campos

4. **HistoriaClinica → DetalleHistoria** (1:N)
   - Una historia tiene múltiples detalles/respuestas

5. **Campo → DetalleHistoria** (1:N)
   - Un campo puede tener múltiples respuestas en diferentes historias

---

## 🔐 Seguridad

### Estrategia de Autenticación

```
┌──────────────┐
│   Cliente    │
└──────┬───────┘
       │ 1. POST /api/auth/login/
       │    {username, password}
       ▼
┌──────────────────────┐
│  TokenObtainPairView │
│  (SimpleJWT)         │
└──────┬───────────────┘
       │ 2. Valida credenciales
       │    contra User model
       ▼
┌──────────────────────┐
│   MyTokenObtain      │
│   PairSerializer     │
└──────┬───────────────┘
       │ 3. Genera tokens JWT
       │    + datos de usuario
       ▼
┌──────────────────────┐
│   Response           │
│   {access, refresh,  │
│    usuario: {...}}   │
└──────────────────────┘
```

### Protección de Endpoints

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**Todos los endpoints requieren autenticación por defecto**, excepto:
- Login
- Refresh token
- URLs de clientes (público)

### Permisos por Rol

```python
# Ejemplo de control de acceso
class HistoriaClinicaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if user.groups.filter(name='Médico').exists():
            # Acceso completo
        elif user.groups.filter(name='Enfermero').exists():
            # Solo lectura
```

---

## 🔄 Patrones de Diseño Implementados

### 1. Repository Pattern (Implícito)
Django ORM actúa como repository para acceso a datos.

```python
# Abstracción del acceso a datos
Paciente.objects.get(cliente_FK=pk)
HistoriaClinica.objects.filter(paciente_fk=paciente_id)
```

### 2. Serializer Pattern
Transformación entre representaciones de datos.

```python
class SerializerPaciente(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
```

### 3. Factory Pattern
Creación de tokens JWT personalizados.

```python
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token["usuario"] = SerializerReadUsuario(user).data
        return token
```

### 4. Strategy Pattern
Diferentes estrategias para tipos de campos en formularios.

```python
def _normalizar_tipo_campo(tipo_frontend):
    tipo_mapping = {
        'Agregar campo de texto': 'text',
        'Agregar área de texto': 'textarea',
        'Agregar campo numérico': 'number',
        'Agregar lista desplegable': 'select',
        'Agregar casilla de verificación': 'checkbox'
    }
    return tipo_mapping.get(tipo_frontend, tipo_frontend)
```

### 5. Template Method Pattern
Patrón para actualización de formularios.

```python
def actualizar_campos_formulario(request, formulario_id):
    # Template method que define el algoritmo
    with transaction.atomic():
        for campo_data in campos_datos:
            if _es_campo_nuevo(campo_id):
                _crear_nuevo_campo(campo_data)
            elif _es_campo_existente(campo_id):
                _actualizar_campo_existente(campo_data)
        
        for campo_id in campos_inactivar:
            _inactivar_campo(campo_id)
```

---

## 📊 Gestión de Transacciones

### Atomic Transactions
Se utiliza `transaction.atomic()` para garantizar consistencia.

```python
from django.db import transaction

@api_view(['PUT'])
def actualizar_campos_formulario(request, formulario_id):
    with transaction.atomic():
        # Todas las operaciones son atómicas
        # Si falla una, se revierten todas
        _crear_nuevos_campos()
        _actualizar_campos_existentes()
        _inactivar_campos()
```

### Ventajas
- ✅ Consistencia de datos
- ✅ Rollback automático en caso de error
- ✅ Integridad referencial

---

## 🌐 Integración con Servicios Externos

### Arquitectura de Integración

```
┌──────────────────────┐
│  Historia Clínica    │
│      (Backend)       │
└──────────┬───────────┘
           │
           │ HTTP Request
           │ + Token Auth
           ▼
┌──────────────────────┐
│  Módulo Integración  │
│  - obtener_token()   │
│  - _realizar_peticion│
└──────────┬───────────┘
           │
           │ HTTP + Headers
           ▼
┌──────────────────────┐
│    DoCalendar API    │
│   (Servicio Externo) │
└──────────────────────┘
```

### Implementación

```python
def _realizar_peticion_externa(token, uri):
    headers = {
        "Authorization": f"token_app {token}",
        "Content-Type": "application/json",
    }
    url = settings.URL_CLIENTES_EXTERNOS + uri
    return requests.get(url=url, headers=headers, timeout=30)
```

### Manejo de Errores

```python
def _procesar_respuesta_externa(response):
    if response.status_code == 200:
        return Response(response.json(), status=200)
    elif response.status_code == 401:
        return Response({"error": "Token inválido"}, status=401)
    elif response.status_code == 404:
        return Response({"error": "Recurso no encontrado"}, status=404)
    else:
        return Response({"error": "Error del servicio externo"}, status=502)
```

---

## 📝 Logging y Auditoría

### Sistema de Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps.usuario': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
    },
}
```

### Niveles de Logging

| Nivel | Uso | Ejemplo |
|-------|-----|---------|
| INFO | Operaciones exitosas | `logger.info("Usuario creado")` |
| WARNING | Situaciones anómalas | `logger.warning("Token próximo a expirar")` |
| ERROR | Errores capturados | `logger.error("Error al conectar BD")` |

### Trazabilidad

El modelo `HistoriaClinicaAuditoria` registra:
- ✅ Quién realizó la acción (usuario)
- ✅ Qué se modificó (campo)
- ✅ Cuándo ocurrió (timestamp)
- ✅ Desde dónde (IP)
- ✅ Valores anteriores y nuevos

---

## 🚀 Escalabilidad

### Estrategias Implementadas

1. **Paginación Automática**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 20
   }
   ```

2. **Lazy Loading**
   - Los campos de formularios se cargan solo cuando se necesitan
   - Las historias clínicas se obtienen bajo demanda

3. **Optimización de Consultas**
   ```python
   # Uso de select_related y prefetch_related
   data = DetalleHistoria.objects.annotate(
       label_input=F('campo_fk__nombre_campo')
   ).filter(historia_fk=historia_id).prefetch_related('formulario_fk', 'campo_fk')
   ```

4. **Indexación de Base de Datos**
   - Primary keys automáticas
   - Foreign keys indexadas
   - Índices en campos de búsqueda frecuente

### Preparación para Microservicios

La arquitectura modular facilita la migración futura a microservicios:

```
Monolito Actual → Microservicios Futuros

apps/usuario/     →  Servicio de Autenticación
apps/paciente/    →  Servicio de Pacientes  
apps/formulario/  →  Servicio de Formularios
apps/historias/   →  Servicio de Historias
apps/integracion/ →  API Gateway
```

---

## 🔧 Configuración y Deployment

### Variables de Entorno

```env
# Seguridad
SECRET_KEY=clave-secreta-django
DEBUG=False

# Base de Datos
DB_NAME=historia_clinica
DB_USER=usuario
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306

# Integración
URL_CLIENTES_EXTERNOS=https://api-externa.com/
```

### Configuración de Producción

**Recomendaciones:**
- ✅ DEBUG=False
- ✅ ALLOWED_HOSTS configurado
- ✅ HTTPS obligatorio
- ✅ Servidor de archivos estáticos (nginx)
- ✅ Servidor de aplicación (gunicorn/uwsgi)
- ✅ Base de datos en servidor dedicado
- ✅ Backup automatizado

### Arquitectura de Deployment

```
                    ┌─────────────┐
                    │   Nginx     │
                    │ (Proxy)     │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼────────┐    ┌──────────▼─────────┐
    │   Gunicorn       │    │   Static Files     │
    │  (App Server)    │    │   (CDN/nginx)      │
    └─────────┬────────┘    └────────────────────┘
              │
    ┌─────────▼────────┐
    │  Django App      │
    │  (Python)        │
    └─────────┬────────┘
              │
    ┌─────────▼────────┐
    │    MySQL         │
    │  (Database)      │
    └──────────────────┘
```

---

## 🧪 Testing

### Estrategia de Testing

1. **Unit Tests**
   - Pruebas de modelos
   - Pruebas de serializers
   - Pruebas de funciones auxiliares

2. **Integration Tests**
   - Pruebas de endpoints
   - Pruebas de flujos completos
   - Pruebas de integración externa

3. **Estructura de Tests**
   ```python
   # apps/paciente/tests.py
   class PacienteModelTest(TestCase):
       def test_edad_calculada(self):
           paciente = Paciente(fecha_nacimiento=date(1990, 1, 1))
           self.assertEqual(paciente.edad, 35)
   
   class PacienteAPITest(APITestCase):
       def test_crear_paciente(self):
           response = self.client.post('/api/paciente/create_pacientes/', data)
           self.assertEqual(response.status_code, 201)
   ```

---

## 📈 Métricas y Monitoreo

### KPIs del Sistema

1. **Performance**
   - Tiempo de respuesta promedio
   - Throughput (requests/segundo)
   - Tasa de error

2. **Negocio**
   - Historias clínicas creadas/día
   - Pacientes nuevos/mes
   - Usuarios activos

3. **Seguridad**
   - Intentos de login fallidos
   - Tokens expirados
   - Accesos no autorizados

### Herramientas Recomendadas

- **APM:** New Relic, DataDog
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Monitoring:** Prometheus + Grafana

---

## 🔮 Roadmap de Evolución

### Próximas Mejoras

1. **Caché**
   - Redis para formularios frecuentes
   - Caché de consultas comunes

2. **Asynchronous Tasks**
   - Celery para procesos largos
   - Notificaciones asíncronas

3. **GraphQL**
   - API GraphQL complementaria
   - Optimización de queries

4. **Websockets**
   - Actualizaciones en tiempo real
   - Notificaciones push

5. **Machine Learning**
   - Predicción de diagnósticos
   - Detección de anomalías

---

## 📚 Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

**Documentado por el equipo de Dosys - Noviembre 2025**
