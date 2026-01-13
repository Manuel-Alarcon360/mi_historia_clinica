# 🚀 Guía Rápida de Referencia - Historia Clínica API

**Cheatsheet para desarrollo rápido**

---

## 🔑 Autenticación

### Obtener Token
```bash
POST /api/auth/login/
{
  "username": "usuario@ejemplo.com",
  "password": "contraseña"
}
# Respuesta: { "access": "...", "refresh": "...", "usuario": {...} }
```

### Usar Token
```bash
Authorization: Bearer <access_token>
```

### Refrescar Token
```bash
POST /api/auth/refresh/
{ "refresh": "<refresh_token>" }
```

---

## 👤 Usuarios

```bash
# Listar roles
GET /api/usuario/list_groups_available/

# Crear usuario
POST /api/usuario/registra_usuarios/
{ "first_name": "...", "last_name": "...", "email": "...", "password": "...", "id_rol": 1 }

# Listar usuarios
GET /api/usuario/list_usuarios/

# Actualizar usuario
PUT /api/usuario/update_empleado/{id}/
{ "first_name": "...", "last_name": "...", "email": "...", "id_rol": 1 }

# Cambiar contraseña
PUT /api/usuario/update_contrasenia/{id}/
{ "password": "nueva_password" }

# Activar/Desactivar
PUT /api/usuario/update_estado_empleado/{id}/
{ "is_active": true }

# Firma digital
GET /api/usuario/obtener_firma_digital/
POST /api/usuario/controlador_firma_digital/
FormData: { imagen: file }
```

---

## 🏥 Pacientes

```bash
# Obtener paciente
GET /api/paciente/get_pacientes/{cliente_fk}/

# Crear paciente
POST /api/paciente/create_pacientes/
{
  "fecha_nacimiento": "1990-01-15",
  "estado_civil": "soltero",
  "eps": "Sanitas",
  "vinculacion": "Contributivo",
  "ocupacion": "Ingeniero",
  "responsable": "...",
  "tel_responsable": "...",
  "cliente_FK": 123
}

# Actualizar paciente
PUT /api/paciente/update_pacientes/{id}/
{ "eps": "Nueva EPS", ... }
```

**Estados civiles:** `soltero`, `casado`, `union_libre`, `divorciado`, `viudo`, `separado`

---

## 📝 Formularios

```bash
# Crear formulario
POST /api/formulario/create_formulario/
{
  "nombre_formulario": "...",
  "principal": true,
  "campos": [
    {
      "nombre_campo": "...",
      "tipo": "text|textarea|number|select|checkbox",
      "requerido": true,
      "opciones": ["opcion1", "opcion2"] // solo para select
    }
  ]
}

# Obtener formulario
GET /api/formulario/obtener_formulario/{id}/
GET /api/formulario/obtener_formulario/principal/

# Listar formularios
GET /api/formulario/list_formularios/

# Actualizar formulario
PUT /api/formulario/actualizar_campos/{id}/
{
  "nombre_formulario": "...",
  "principal": true,
  "campos_datos": [...],        // Campos nuevos o existentes
  "campos_editados": [...],      // Solo campos modificados
  "campos_inactivar": [1, 2, 3]  // IDs a inactivar
}

# Eliminar formulario
DELETE /api/formulario/delete_formulario/{id}/
```

**Tipos de campo:** `text`, `textarea`, `number`, `select`, `checkbox`

---

## 📋 Historias Clínicas

```bash
# Crear historia clínica
POST /api/historia/crear_historia_clinica/
{
  "paciente": {
    "fecha_nacimiento": "1990-01-15",
    "estado_civil": "soltero",
    "eps": "...",
    "vinculacion": "...",
    "ocupacion": "...",
    "cliente_FK": 123
  },
  "historia_clinica": {
    "motivo_consulta": "...",
    "doctor": 5
  },
  "detalle_historia": {
    "formulario_fk": 1,
    "campos": [
      { "campo_fk": 1, "respuesta_campo": "..." },
      { "campo_fk": 2, "respuesta_campo": "..." }
    ]
  }
}

# Actualizar historia (mismo endpoint, agregar id)
POST /api/historia/crear_historia_clinica/
{
  "paciente": { ... },
  "historia_clinica": {
    "id": 35,  // ID de historia existente
    "motivo_consulta": "...",
    "doctor": 5
  },
  "detalle_historia": { ... }
}

# Obtener historia
GET /api/historia/obtener_historia/{paciente_id}/

# Obtener detalles (agrupados por fecha)
GET /api/historia/obtener_detalle_historia/{historia_id}/
```

---

## 🔗 Integración (DoCalendar)

```bash
# Configurar token
POST /api/integracion/crear_integracion/
{ "nombre_aplicacion": "DoCalendar", "token_aplicacion": "..." }

# Listar tokens
GET /api/integracion/list_integracion/

# Obtener clientes externos
GET /api/integracion/obtener_clientes_externos/?page=1

# Buscar cliente
GET /api/integracion/buscar_cliente/?query=Juan

# Crear cliente externo
POST /api/integracion/crear_cliente/
{ "nombre": "...", "identificacion": "...", ... }

# Obtener citas
GET /api/integracion/obtener_citas/

# URLs de clientes (público)
GET /api/integracion/obtener_urls_clientes/
```

---

## 🐍 Comandos Django Útiles

```bash
# Servidor de desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic

# Tests
python manage.py test
python manage.py test apps.usuario
```

---

## 🗄️ Modelos Principales

### User (Django Auth)
- `username`, `email`, `password`
- `first_name`, `last_name`
- `is_active`, `groups`

### Paciente
- `fecha_nacimiento`, `estado_civil`
- `eps`, `vinculacion`, `ocupacion`
- `responsable`, `tel_responsable`
- `cliente_FK`

### Formulario
- `nombre_formulario`
- `principal` (boolean)
- `campos` (relación)

### Campo
- `nombre_campo`, `tipo`
- `requerido`, `estado_campo`
- `opciones` (string separado por comas)
- `formulario_FK`

### HistoriaClinica
- `paciente_fk`, `doctor`
- `motivo_consulta`
- `detalles` (relación)

### DetalleHistoria
- `historia_fk`, `campo_fk`
- `formulario_fk`
- `respuesta_campo`

---

## 📊 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Éxito |
| 201 | Created - Creado |
| 204 | No Content - Eliminado |
| 400 | Bad Request - Error validación |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - No encontrado |
| 500 | Internal Server Error |

---

## 🔍 Query Params Comunes

```bash
# Paginación
?page=2

# Búsqueda (integración)
?query=texto_busqueda
```

---

## 🐛 Debugging Rápido

```python
# En views.py
import logging
logger = logging.getLogger(__name__)

logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error", exc_info=True)

# Debug en consola
print(f"Variable: {variable}")

# Django shell
python manage.py shell
>>> from apps.paciente.models import Paciente
>>> Paciente.objects.all()
```

---

## 📝 Tips Rápidos

### 1. Validar JSON antes de enviar
```javascript
JSON.parse(JSON.stringify(data)) // Asegura que sea JSON válido
```

### 2. Fechas siempre en formato ISO
```
YYYY-MM-DD
2025-11-03
```

### 3. Campos booleanos
```json
true  // No "true" como string
false
```

### 4. Headers requeridos
```
Authorization: Bearer <token>
Content-Type: application/json
```

### 5. FormData para archivos
```javascript
const formData = new FormData();
formData.append('imagen', file);
```

---

## 🔐 Seguridad Quick Checks

- [ ] Siempre usar HTTPS en producción
- [ ] Token en header, nunca en URL
- [ ] Validar todos los inputs
- [ ] No exponer SECRET_KEY
- [ ] DEBUG=False en producción
- [ ] CORS configurado correctamente

---

## 🚨 Errores Comunes y Soluciones

### "Authentication credentials were not provided"
➡️ Agregar header: `Authorization: Bearer <token>`

### "Token is invalid or expired"
➡️ Refrescar token con endpoint `/api/auth/refresh/`

### "CSRF verification failed"
➡️ Agregar dominio a `CSRF_TRUSTED_ORIGINS` en settings.py

### "No se encontró un paciente con el ID proporcionado"
➡️ Verificar que `cliente_FK` exista

### "Ya existe un formulario principal"
➡️ Solo puede haber un formulario con `principal=true`

---

## 💡 Patrones de Respuesta

### Respuesta Exitosa
```json
{
  "detail": "Operación exitosa",
  "data": {...}
}
```

### Respuesta con Error
```json
{
  "detail": "Descripción del error",
  "errors": {
    "campo": ["Mensaje específico"]
  },
  "error_code": "CODIGO_ERROR"
}
```

### Respuesta con Lista
```json
{
  "count": 50,
  "next": "url_siguiente_pagina",
  "previous": "url_pagina_anterior",
  "results": [...]
}
```

---

## 🔄 Workflow Común

### Crear Primera Historia Clínica

1. **Login**
   ```
   POST /api/auth/login/
   ```

2. **Obtener formulario principal**
   ```
   GET /api/formulario/obtener_formulario/principal/
   ```

3. **Verificar/Crear paciente**
   ```
   GET /api/paciente/get_pacientes/{cliente_fk}/
   O
   POST /api/paciente/create_pacientes/
   ```

4. **Crear historia**
   ```
   POST /api/historia/crear_historia_clinica/
   ```

5. **Verificar**
   ```
   GET /api/historia/obtener_detalle_historia/{historia_id}/
   ```

---

## 📱 Testing con cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario@ejemplo.com","password":"pass123"}'

# Con token
curl -X GET http://localhost:8000/api/usuario/list_usuarios/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# POST con datos
curl -X POST http://localhost:8000/api/paciente/create_pacientes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fecha_nacimiento":"1990-01-15",...}'
```

---

## 🔧 Variables de Entorno (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=historia_clinica
DB_USER=usuario
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
URL_CLIENTES_EXTERNOS=http://external-api.com/
```

---

## 📚 Más Información

- **README.md**: Documentación completa
- **EJEMPLOS_API.md**: Ejemplos detallados
- **ARQUITECTURA.md**: Diseño del sistema
- **DEPLOYMENT.md**: Deployment y configuración

---

**Última actualización: 3 de noviembre de 2025**

**💡 Tip:** Guarda este documento para referencia rápida durante el desarrollo.
