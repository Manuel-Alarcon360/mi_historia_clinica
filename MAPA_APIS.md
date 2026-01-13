# 🗺️ Mapa Visual de APIs - Sistema Historia Clínica

## 📊 Estructura General de URLs

```
http://localhost:8000/
│
├─── /admin/                              # Panel de administración Django
│
├─── /api/auth/                          # Autenticación (JWT)
│    ├─── /login/                        [POST] Iniciar sesión
│    ├─── /refresh/                      [POST] Refrescar token
│    └─── /verify/                       [POST] Verificar token
│
├─── /api/usuario/                       # Gestión de usuarios
│    ├─── /login/                        [POST] Login (alternativo)
│    ├─── /token/refresh/                [POST] Refresh token
│    ├─── /logout/                       [POST] Logout
│    ├─── /registra_usuarios/            [POST] Registrar usuario
│    ├─── /list_groups_available/        [GET]  Listar roles
│    ├─── /list_usuarios/                [GET]  Listar usuarios
│    ├─── /update_estado_empleado/{id}/  [PUT]  Activar/desactivar
│    ├─── /update_empleado/{id}/         [PUT]  Actualizar usuario
│    ├─── /update_contrasenia/{id}/      [PUT]  Cambiar contraseña
│    ├─── /obtener_firma_digital/        [GET]  Obtener firma
│    └─── /controlador_firma_digital/    [POST] Crear/actualizar firma
│
├─── /api/paciente/                      # Gestión de pacientes
│    ├─── /get_pacientes/{cliente_fk}/   [GET]  Obtener paciente
│    ├─── /create_pacientes/             [POST] Crear paciente
│    └─── /update_pacientes/{id}/        [PUT]  Actualizar paciente
│
├─── /api/formulario/                    # Formularios dinámicos
│    ├─── /create_formulario/            [POST]   Crear formulario
│    ├─── /obtener_formulario/{id}/      [GET]    Obtener formulario
│    ├─── /obtener_formulario/principal/ [GET]    Obtener principal
│    ├─── /actualizar_campos/{id}/       [PUT]    Actualizar campos
│    ├─── /list_formularios/             [GET]    Listar formularios
│    └─── /delete_formulario/{id}/       [DELETE] Eliminar formulario
│
├─── /api/historia/                      # Historias clínicas
│    ├─── /crear_historia_clinica/       [POST] Crear/actualizar historia
│    ├─── /obtener_historia/{pac_id}/    [GET]  Obtener historia
│    └─── /obtener_detalle_historia/{h_id}/ [GET] Obtener detalles
│
└─── /api/integracion/                   # Integración externa
     ├─── /list_integracion/             [GET, POST] Listar/crear tokens
     ├─── /list_integracion/{id}/        [GET, PUT, DELETE] CRUD token
     ├─── /obtener_clientes_externos/    [GET]  Obtener clientes
     ├─── /buscar_cliente/               [GET]  Buscar cliente
     ├─── /crear_cliente/                [POST] Crear cliente
     ├─── /obtener_citas/                [GET]  Obtener citas
     └─── /obtener_urls_clientes/        [GET]  URLs (público)
```

---

## 🔐 Autenticación Requerida

### Públicos (No requieren autenticación)
```
✅ POST /api/auth/login/
✅ POST /api/auth/refresh/
✅ GET  /api/integracion/obtener_urls_clientes/
```

### Protegidos (Requieren Bearer Token)
```
🔒 Todos los demás endpoints
```

---

## 📋 Mapa por Funcionalidad

### 1️⃣ AUTENTICACIÓN Y SESIÓN

```
┌─────────────────────────────────────────────┐
│           FLUJO DE AUTENTICACIÓN            │
├─────────────────────────────────────────────┤
│                                             │
│  1. POST /api/auth/login/                   │
│     ↓ Recibe username + password            │
│     ↓ Retorna access + refresh tokens       │
│                                             │
│  2. Usar access token en headers            │
│     Authorization: Bearer <access_token>    │
│                                             │
│  3. POST /api/auth/refresh/                 │
│     ↓ Cuando access token expira            │
│     ↓ Enviar refresh token                  │
│     ↓ Recibir nuevo access token            │
│                                             │
│  4. POST /api/auth/verify/                  │
│     ↓ Verificar si token es válido          │
│                                             │
└─────────────────────────────────────────────┘
```

### 2️⃣ GESTIÓN DE USUARIOS

```
┌─────────────────────────────────────────────┐
│           CICLO DE VIDA USUARIO             │
├─────────────────────────────────────────────┤
│                                             │
│  Crear                                      │
│  ↓ POST /api/usuario/registra_usuarios/     │
│  │                                          │
│  Consultar                                  │
│  ↓ GET /api/usuario/list_usuarios/          │
│  │                                          │
│  Actualizar                                 │
│  ↓ PUT /api/usuario/update_empleado/{id}/   │
│  │                                          │
│  Gestionar Firma                            │
│  ↓ POST /api/usuario/controlador_firma_digital/ │
│  │                                          │
│  Cambiar Password                           │
│  ↓ PUT /api/usuario/update_contrasenia/{id}/│
│  │                                          │
│  Activar/Desactivar                         │
│  ↓ PUT /api/usuario/update_estado_empleado/{id}/ │
│                                             │
└─────────────────────────────────────────────┘
```

### 3️⃣ GESTIÓN DE PACIENTES

```
┌─────────────────────────────────────────────┐
│          CICLO DE VIDA PACIENTE             │
├─────────────────────────────────────────────┤
│                                             │
│  Consultar Existente                        │
│  ↓ GET /api/paciente/get_pacientes/{fk}/    │
│  │                                          │
│  Si no existe → Crear                       │
│  ↓ POST /api/paciente/create_pacientes/     │
│  │                                          │
│  Actualizar Información                     │
│  ↓ PUT /api/paciente/update_pacientes/{id}/ │
│                                             │
└─────────────────────────────────────────────┘
```

### 4️⃣ FORMULARIOS DINÁMICOS

```
┌─────────────────────────────────────────────┐
│       GESTIÓN DE FORMULARIOS                │
├─────────────────────────────────────────────┤
│                                             │
│  Crear Formulario + Campos                  │
│  ↓ POST /api/formulario/create_formulario/  │
│  │  {nombre, principal, campos[]}           │
│  │                                          │
│  Consultar Formulario                       │
│  ↓ GET /api/formulario/obtener_formulario/{id}/ │
│  │  O /obtener_formulario/principal/        │
│  │                                          │
│  Actualizar Campos                          │
│  ↓ PUT /api/formulario/actualizar_campos/{id}/ │
│  │  {campos_datos, campos_editados,         │
│  │   campos_inactivar}                      │
│  │                                          │
│  Listar Todos                               │
│  ↓ GET /api/formulario/list_formularios/    │
│  │                                          │
│  Eliminar                                   │
│  ↓ DELETE /api/formulario/delete_formulario/{id}/ │
│                                             │
└─────────────────────────────────────────────┘
```

### 5️⃣ HISTORIAS CLÍNICAS

```
┌─────────────────────────────────────────────┐
│        FLUJO HISTORIA CLÍNICA               │
├─────────────────────────────────────────────┤
│                                             │
│  1. Obtener Formulario                      │
│     GET /api/formulario/obtener_formulario/principal/ │
│     ↓                                       │
│                                             │
│  2. Verificar/Crear Paciente                │
│     GET /api/paciente/get_pacientes/{fk}/   │
│     ↓ Si no existe                          │
│     POST /api/paciente/create_pacientes/    │
│     ↓                                       │
│                                             │
│  3. Crear Historia Clínica                  │
│     POST /api/historia/crear_historia_clinica/ │
│     {                                       │
│       paciente: {...},                      │
│       historia_clinica: {...},              │
│       detalle_historia: {                   │
│         formulario_fk: 1,                   │
│         campos: [...]                       │
│       }                                     │
│     }                                       │
│     ↓                                       │
│                                             │
│  4. Consultar Historia                      │
│     GET /api/historia/obtener_historia/{pac_id}/ │
│     ↓                                       │
│                                             │
│  5. Ver Detalles (agrupados por fecha)      │
│     GET /api/historia/obtener_detalle_historia/{h_id}/ │
│                                             │
└─────────────────────────────────────────────┘
```

### 6️⃣ INTEGRACIÓN EXTERNA (DoCalendar)

```
┌─────────────────────────────────────────────┐
│        FLUJO DE INTEGRACIÓN                 │
├─────────────────────────────────────────────┤
│                                             │
│  Configurar Token (una vez)                 │
│  ↓ POST /api/integracion/crear_integracion/ │
│  │  {nombre_aplicacion, token_aplicacion}   │
│  │                                          │
│  Obtener Clientes                           │
│  ↓ GET /api/integracion/obtener_clientes_externos/ │
│  │  ?page=1                                 │
│  │                                          │
│  Buscar Cliente Específico                  │
│  ↓ GET /api/integracion/buscar_cliente/     │
│  │  ?query=nombre                           │
│  │                                          │
│  Crear Cliente Nuevo                        │
│  ↓ POST /api/integracion/crear_cliente/     │
│  │  {nombre, identificacion, ...}           │
│  │                                          │
│  Obtener Citas Agendadas                    │
│  ↓ GET /api/integracion/obtener_citas/      │
│  │                                          │
│  Obtener URLs (público)                     │
│  ↓ GET /api/integracion/obtener_urls_clientes/ │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔄 Flujos Completos End-to-End

### Flujo 1: Nueva Consulta Médica Completa

```
┌─────────────┐
│   INICIO    │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│  1. LOGIN            │
│  POST /api/auth/login/│
└──────┬───────────────┘
       │ access_token
       ▼
┌──────────────────────────┐
│  2. OBTENER CITAS        │
│  GET /integracion/       │
│      obtener_citas/      │
└──────┬───────────────────┘
       │ lista de citas
       ▼
┌──────────────────────────┐
│  3. SELECCIONAR CITA     │
│  cliente_fk = cita.paciente_id │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  4. BUSCAR PACIENTE      │
│  GET /paciente/          │
│      get_pacientes/{fk}/ │
└──────┬───────────────────┘
       │
       ├─── ✅ Existe ────────┐
       │                      │
       └─── ❌ No existe      │
              ▼               │
       ┌──────────────────┐  │
       │ 5a. CREAR        │  │
       │ POST /paciente/  │  │
       │ create_pacientes/│  │
       └──────┬───────────┘  │
              │              │
              ▼              │
       ┌─────────────────────┘
       │
       ▼
┌──────────────────────────┐
│  6. OBTENER FORMULARIO   │
│  GET /formulario/        │
│      obtener_formulario/ │
│      principal/          │
└──────┬───────────────────┘
       │ campos del formulario
       ▼
┌──────────────────────────┐
│  7. LLENAR FORMULARIO    │
│  (Frontend/Usuario)      │
└──────┬───────────────────┘
       │ respuestas
       ▼
┌──────────────────────────┐
│  8. CREAR HISTORIA       │
│  POST /historia/         │
│      crear_historia_     │
│      clinica/            │
└──────┬───────────────────┘
       │ historia_id
       ▼
┌──────────────────────────┐
│  9. FIRMAR (OPCIONAL)    │
│  POST /usuario/          │
│      controlador_firma_  │
│      digital/            │
└──────┬───────────────────┘
       │
       ▼
┌──────────────┐
│   FINALIZADO │
└──────────────┘
```

### Flujo 2: Consultar Historial Médico

```
┌─────────────┐
│   INICIO    │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│  1. BUSCAR PACIENTE      │
│  GET /integracion/       │
│      buscar_cliente/     │
│      ?query=nombre       │
└──────┬───────────────────┘
       │ cliente_fk
       ▼
┌──────────────────────────┐
│  2. OBTENER PACIENTE     │
│  GET /paciente/          │
│      get_pacientes/{fk}/ │
└──────┬───────────────────┘
       │ paciente_id
       ▼
┌──────────────────────────┐
│  3. OBTENER HISTORIA     │
│  GET /historia/          │
│      obtener_historia/   │
│      {paciente_id}/      │
└──────┬───────────────────┘
       │ historia_id
       ▼
┌──────────────────────────┐
│  4. OBTENER DETALLES     │
│  GET /historia/          │
│      obtener_detalle_    │
│      historia/{h_id}/    │
└──────┬───────────────────┘
       │ detalles agrupados
       ▼
┌──────────────────────────┐
│  5. MOSTRAR HISTORIAL    │
│  (Frontend)              │
└──────────────────────────┘
```

### Flujo 3: Crear Formulario Personalizado

```
┌─────────────┐
│   INICIO    │
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│  1. DISEÑAR FORMULARIO   │
│  (Frontend/Usuario)      │
│  - Nombre                │
│  - Campos                │
│  - Tipos                 │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  2. CREAR FORMULARIO     │
│  POST /formulario/       │
│      create_formulario/  │
│  {nombre, principal,     │
│   campos[]}              │
└──────┬───────────────────┘
       │ formulario_id
       ▼
┌──────────────────────────┐
│  3. VERIFICAR CREACIÓN   │
│  GET /formulario/        │
│      obtener_formulario/ │
│      {id}/               │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  4. USAR EN HISTORIAS    │
│  POST /historia/         │
│      crear_historia_     │
│      clinica/            │
└──────────────────────────┘
```

---

## 📊 Resumen de Métodos HTTP por Módulo

| Módulo | GET | POST | PUT | DELETE |
|--------|-----|------|-----|--------|
| **Auth** | ✅ | ✅ | ❌ | ❌ |
| **Usuario** | ✅ | ✅ | ✅ | ❌ |
| **Paciente** | ✅ | ✅ | ✅ | ❌ |
| **Formulario** | ✅ | ✅ | ✅ | ✅ |
| **Historia** | ✅ | ✅ | ❌ | ❌ |
| **Integración** | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 Endpoints Más Usados

### Top 10 Endpoints Frecuentes

1. `POST /api/auth/login/` - Login
2. `GET /api/formulario/obtener_formulario/principal/` - Form principal
3. `POST /api/historia/crear_historia_clinica/` - Crear historia
4. `GET /api/historia/obtener_detalle_historia/{id}/` - Ver detalles
5. `GET /api/paciente/get_pacientes/{fk}/` - Obtener paciente
6. `GET /api/integracion/obtener_citas/` - Ver citas
7. `GET /api/integracion/obtener_clientes_externos/` - Ver clientes
8. `POST /api/usuario/registra_usuarios/` - Registrar usuario
9. `GET /api/usuario/list_usuarios/` - Listar usuarios
10. `POST /api/auth/refresh/` - Refrescar token

---

## 🔍 Búsqueda Rápida

**¿Necesitas...?**

- **Autenticarme:** → `POST /api/auth/login/`
- **Crear un usuario:** → `POST /api/usuario/registra_usuarios/`
- **Ver pacientes:** → `GET /api/paciente/get_pacientes/{fk}/`
- **Crear formulario:** → `POST /api/formulario/create_formulario/`
- **Ver historial:** → `GET /api/historia/obtener_detalle_historia/{id}/`
- **Ver citas:** → `GET /api/integracion/obtener_citas/`

---

## 📱 Códigos de Respuesta Rápidos

```
200 ✅ OK              - Operación exitosa
201 ✅ Created         - Recurso creado
204 ✅ No Content      - Eliminación exitosa
400 ❌ Bad Request     - Error de validación
401 ❌ Unauthorized    - Token inválido/expirado
403 ❌ Forbidden       - Sin permisos
404 ❌ Not Found       - Recurso no existe
500 ❌ Server Error    - Error del servidor
```

---

**Para más detalles, consulta:**
- [CHEATSHEET.md](./CHEATSHEET.md) - Referencia rápida
- [EJEMPLOS_API.md](./EJEMPLOS_API.md) - Ejemplos completos
- [README.md](./README.md) - Documentación completa

---

**Última actualización: 3 de noviembre de 2025**
