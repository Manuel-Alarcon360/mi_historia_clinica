# Ejemplos de Uso de API - Sistema de Historia Clínica

Este documento contiene ejemplos prácticos de uso de todas las APIs del sistema.

---

## 📋 Tabla de Contenidos

1. [Autenticación y Gestión de Sesiones](#autenticación-y-gestión-de-sesiones)
2. [Flujo Completo de Registro de Usuario](#flujo-completo-de-registro-de-usuario)
3. [Flujo Completo de Gestión de Pacientes](#flujo-completo-de-gestión-de-pacientes)
4. [Flujo Completo de Creación de Formularios](#flujo-completo-de-creación-de-formularios)
5. [Flujo Completo de Historia Clínica](#flujo-completo-de-historia-clínica)
6. [Integración con DoCalendar](#integración-con-docalendar)
7. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## 🔐 Autenticación y Gestión de Sesiones

### Ejemplo 1: Login y Obtención de Tokens

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor@ejemplo.com",
    "password": "MiPassword123"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMzA4NDgwMCwianRpIjoiYWJjMTIzIiwidXNlcl9pZCI6NX0.xyz789",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMzMDgxMjAwLCJqdGkiOiJkZWYzNDUiLCJ1c2VyX2lkIjo1fQ.abc456",
  "usuario": {
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "doctor@ejemplo.com",
    "groups": [1],
    "name_group": "Médico"
  }
}
```

### Ejemplo 2: Refrescar Token Expirado

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.nuevo_token.xyz"
}
```

### Ejemplo 3: Usar Token en Peticiones Protegidas

**Request:**
```bash
curl -X GET http://localhost:8000/api/usuario/list_usuarios/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## 👤 Flujo Completo de Registro de Usuario

### Paso 1: Obtener Roles Disponibles

**Request:**
```bash
curl -X GET http://localhost:8000/api/usuario/list_groups_available/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Médico"
    },
    {
      "id": 2,
      "name": "Enfermero"
    },
    {
      "id": 3,
      "name": "Administrador"
    }
  ]
}
```

### Paso 2: Registrar Nuevo Usuario (Médico)

**Request:**
```bash
curl -X POST http://localhost:8000/api/usuario/registra_usuarios/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "María",
    "last_name": "González Rodríguez",
    "email": "maria.gonzalez@clinica.com",
    "password": "PasswordSeguro123!",
    "id_rol": 1
  }'
```

**Response:**
```json
{
  "detail": "Usuario registrado exitosamente.",
  "user_id": 10,
  "username": "maria.gonzalez@clinica.com",
  "rol": "Médico"
}
```

### Paso 3: Subir Firma Digital (Opcional)

**Request (usando FormData):**
```bash
curl -X POST http://localhost:8000/api/usuario/controlador_firma_digital/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "imagen=@/path/to/firma.png"
```

**Response:**
```json
{
  "detail": "Firma digital creada exitosamente.",
  "data": {
    "id": 5,
    "usuario": 10,
    "imagen": "/media/firmas_digitales/firma_usuario_10.png"
  }
}
```

### Paso 4: Actualizar Información del Usuario

**Request:**
```bash
curl -X PUT http://localhost:8000/api/usuario/update_empleado/10/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "María Carolina",
    "last_name": "González Rodríguez",
    "email": "maria.gonzalez@clinica.com",
    "id_rol": 1
  }'
```

### Paso 5: Cambiar Contraseña

**Request:**
```bash
curl -X PUT http://localhost:8000/api/usuario/update_contrasenia/10/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "NuevaPasswordSegura456!"
  }'
```

**Response:**
```json
{
  "detail": "Contraseña cambiada exitosamente."
}
```

### Paso 6: Desactivar Usuario

**Request:**
```bash
curl -X PUT http://localhost:8000/api/usuario/update_estado_empleado/10/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

---

## 🏥 Flujo Completo de Gestión de Pacientes

### Escenario 1: Crear Nuevo Paciente

**Request:**
```bash
curl -X POST http://localhost:8000/api/paciente/create_pacientes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha_nacimiento": "1985-03-20",
    "estado_civil": "casado",
    "eps": "Sanitas EPS",
    "vinculacion": "Contributivo",
    "ocupacion": "Ingeniero de Software",
    "responsable": "Ana Pérez García",
    "tel_responsable": "3101234567",
    "cliente_FK": 505
  }'
```

**Response:**
```json
{
  "detail": "Paciente creado exitosamente.",
  "data": {
    "id": 25,
    "fecha_nacimiento": "1985-03-20",
    "estado_civil": "casado",
    "eps": "Sanitas EPS",
    "vinculacion": "Contributivo",
    "ocupacion": "Ingeniero de Software",
    "responsable": "Ana Pérez García",
    "tel_responsable": "3101234567",
    "cliente_FK": 505,
    "edad": 39
  }
}
```

### Escenario 2: Consultar Paciente Existente

**Request:**
```bash
curl -X GET http://localhost:8000/api/paciente/get_pacientes/505/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "detail": "Paciente encontrado con éxito.",
  "data": {
    "id": 25,
    "fecha_nacimiento": "1985-03-20",
    "estado_civil": "casado",
    "eps": "Sanitas EPS",
    "vinculacion": "Contributivo",
    "ocupacion": "Ingeniero de Software",
    "responsable": "Ana Pérez García",
    "tel_responsable": "3101234567",
    "cliente_FK": 505,
    "edad": 39
  }
}
```

### Escenario 3: Actualizar Información del Paciente

**Request:**
```bash
curl -X PUT http://localhost:8000/api/paciente/update_pacientes/25/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eps": "Compensar EPS",
    "ocupacion": "Arquitecto de Software",
    "tel_responsable": "3109876543"
  }'
```

**Response:**
```json
{
  "detail": "Paciente actualizado exitosamente.",
  "data": {
    "id": 25,
    "fecha_nacimiento": "1985-03-20",
    "estado_civil": "casado",
    "eps": "Compensar EPS",
    "vinculacion": "Contributivo",
    "ocupacion": "Arquitecto de Software",
    "responsable": "Ana Pérez García",
    "tel_responsable": "3109876543",
    "cliente_FK": 505,
    "edad": 39
  }
}
```

---

## 📝 Flujo Completo de Creación de Formularios

### Escenario 1: Crear Formulario Principal de Historia Clínica

**Request:**
```bash
curl -X POST http://localhost:8000/api/formulario/create_formulario/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_formulario": "Historia Clínica General",
    "principal": true,
    "campos": [
      {
        "nombre_campo": "Motivo de Consulta",
        "tipo": "textarea",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "Tipo de Sangre",
        "tipo": "select",
        "requerido": true,
        "opciones": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
      },
      {
        "nombre_campo": "Peso (kg)",
        "tipo": "number",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "Altura (cm)",
        "tipo": "number",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "¿Fuma?",
        "tipo": "checkbox",
        "requerido": false,
        "opciones": null
      },
      {
        "nombre_campo": "¿Consume Alcohol?",
        "tipo": "checkbox",
        "requerido": false,
        "opciones": null
      },
      {
        "nombre_campo": "Alergias Conocidas",
        "tipo": "textarea",
        "requerido": false,
        "opciones": null
      },
      {
        "nombre_campo": "Medicamentos Actuales",
        "tipo": "textarea",
        "requerido": false,
        "opciones": null
      }
    ]
  }'
```

**Response:**
```json
{
  "detail": "Formulario creado con éxito.",
  "id": 1
}
```

### Escenario 2: Crear Formulario Especializado (Control Prenatal)

**Request:**
```bash
curl -X POST http://localhost:8000/api/formulario/create_formulario/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_formulario": "Control Prenatal",
    "principal": false,
    "campos": [
      {
        "nombre_campo": "Semanas de Gestación",
        "tipo": "number",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "Fecha Última Menstruación",
        "tipo": "text",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "Presión Arterial",
        "tipo": "text",
        "requerido": true,
        "opciones": null
      },
      {
        "nombre_campo": "Trimestre",
        "tipo": "select",
        "requerido": true,
        "opciones": ["Primer Trimestre", "Segundo Trimestre", "Tercer Trimestre"]
      },
      {
        "nombre_campo": "Movimientos Fetales",
        "tipo": "checkbox",
        "requerido": false,
        "opciones": null
      }
    ]
  }'
```

### Escenario 3: Obtener Formulario Principal

**Request:**
```bash
curl -X GET http://localhost:8000/api/formulario/obtener_formulario/principal/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "detail": "Formulario obtenido con éxito.",
  "data": {
    "formulario": {
      "id": 1,
      "nombre_formulario": "Historia Clínica General",
      "principal": true,
      "fecha_creacion": "2025-11-03",
      "fecha_actualizacion": "2025-11-03"
    },
    "campos": [
      {
        "id": 1,
        "nombre_campo": "Motivo de Consulta",
        "tipo": "textarea",
        "requerido": true,
        "estado_campo": true,
        "formulario_FK": 1,
        "opciones": null,
        "fecha_creacion": "2025-11-03",
        "fecha_actualizacion": "2025-11-03"
      },
      {
        "id": 2,
        "nombre_campo": "Tipo de Sangre",
        "tipo": "select",
        "requerido": true,
        "estado_campo": true,
        "formulario_FK": 1,
        "opciones": "A+,A-,B+,B-,O+,O-,AB+,AB-",
        "fecha_creacion": "2025-11-03",
        "fecha_actualizacion": "2025-11-03"
      }
    ]
  }
}
```

### Escenario 4: Actualizar Formulario (Agregar, Editar, Eliminar Campos)

**Request:**
```bash
curl -X PUT http://localhost:8000/api/formulario/actualizar_campos/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_formulario": "Historia Clínica General Actualizada",
    "principal": true,
    "campos_datos": [
      {
        "id": 1,
        "nombre_campo": "Motivo de Consulta",
        "tipo": "textarea",
        "requerido": true,
        "opciones": null
      },
      {
        "id": "campo_nuevo_1",
        "nombre_campo": "Antecedentes Familiares",
        "tipo": "textarea",
        "requerido": false,
        "opciones": null
      },
      {
        "id": "campo_nuevo_2",
        "nombre_campo": "Nivel de Actividad Física",
        "tipo": "select",
        "requerido": false,
        "opciones": ["Sedentario", "Ligero", "Moderado", "Intenso"]
      }
    ],
    "campos_editados": [
      {
        "id": 2,
        "nombre_campo": "Grupo Sanguíneo",
        "tipo": "select",
        "requerido": true,
        "opciones": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
      }
    ],
    "campos_inactivar": [5, 6]
  }'
```

**Response:**
```json
{
  "detail": "Campos actualizados con éxito.",
  "mensaje": "2 campo(s) creado(s), 1 campo(s) actualizado(s), 2 campo(s) inactivado(s)",
  "resultados": {
    "campos_creados": [
      {
        "id": 15,
        "nombre": "Antecedentes Familiares"
      },
      {
        "id": 16,
        "nombre": "Nivel de Actividad Física"
      }
    ],
    "campos_actualizados": [
      {
        "id": 2,
        "nombre": "Grupo Sanguíneo"
      }
    ],
    "campos_inactivados": [
      {
        "id": 5,
        "nombre": "¿Fuma?"
      },
      {
        "id": 6,
        "nombre": "¿Consume Alcohol?"
      }
    ],
    "campos_omitidos": [],
    "errores": []
  }
}
```

### Escenario 5: Listar Todos los Formularios

**Request:**
```bash
curl -X GET http://localhost:8000/api/formulario/list_formularios/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre_formulario": "Historia Clínica General Actualizada",
      "principal": true,
      "fecha_creacion": "2025-11-03",
      "fecha_actualizacion": "2025-11-03"
    },
    {
      "id": 2,
      "nombre_formulario": "Control Prenatal",
      "principal": false,
      "fecha_creacion": "2025-11-03",
      "fecha_actualizacion": "2025-11-03"
    }
  ]
}
```

---

## 📋 Flujo Completo de Historia Clínica

### Escenario Completo: Primera Consulta de Paciente Nuevo

**Request:**
```bash
curl -X POST http://localhost:8000/api/historia/crear_historia_clinica/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente": {
      "fecha_nacimiento": "1990-07-15",
      "estado_civil": "soltero",
      "eps": "Sanitas EPS",
      "vinculacion": "Contributivo",
      "ocupacion": "Profesor",
      "responsable": "Rosa López",
      "tel_responsable": "3158765432",
      "cliente_FK": 707
    },
    "historia_clinica": {
      "motivo_consulta": "Dolor de cabeza recurrente, mareos ocasionales",
      "doctor": 5
    },
    "detalle_historia": {
      "formulario_fk": 1,
      "campos": [
        {
          "campo_fk": 1,
          "respuesta_campo": "Presenta dolores de cabeza intensos hace 2 semanas, acompañados de mareos al levantarse"
        },
        {
          "campo_fk": 2,
          "respuesta_campo": "O+"
        },
        {
          "campo_fk": 3,
          "respuesta_campo": "75"
        },
        {
          "campo_fk": 4,
          "respuesta_campo": "170"
        },
        {
          "campo_fk": 5,
          "respuesta_campo": false
        },
        {
          "campo_fk": 6,
          "respuesta_campo": false
        },
        {
          "campo_fk": 7,
          "respuesta_campo": "Alergia a la penicilina"
        },
        {
          "campo_fk": 8,
          "respuesta_campo": "Losartán 50mg (1 vez al día)"
        }
      ]
    }
  }'
```

**Response:**
```json
{
  "detail": "Historia clínica creada exitosamente",
  "historia_clinica_id": 35,
  "paciente_id": 28,
  "detalle_id": 120
}
```

### Escenario: Actualizar Historia Clínica Existente

**Request:**
```bash
curl -X POST http://localhost:8000/api/historia/crear_historia_clinica/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente": {
      "fecha_nacimiento": "1990-07-15",
      "estado_civil": "soltero",
      "eps": "Sanitas EPS",
      "vinculacion": "Contributivo",
      "ocupacion": "Profesor",
      "responsable": "Rosa López",
      "tel_responsable": "3158765432",
      "cliente_FK": 707
    },
    "historia_clinica": {
      "id": 35,
      "motivo_consulta": "Control - Seguimiento dolor de cabeza",
      "doctor": 5
    },
    "detalle_historia": {
      "formulario_fk": 1,
      "campos": [
        {
          "campo_fk": 1,
          "respuesta_campo": "Mejoría significativa del dolor de cabeza. Mareos desaparecieron después del tratamiento."
        },
        {
          "campo_fk": 3,
          "respuesta_campo": "74"
        },
        {
          "campo_fk": 8,
          "respuesta_campo": "Losartán 50mg (1 vez al día), Ibuprofeno 400mg (según necesidad)"
        }
      ]
    }
  }'
```

### Escenario: Consultar Historia Clínica de un Paciente

**Request:**
```bash
curl -X GET http://localhost:8000/api/historia/obtener_historia/28/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "detail": "Historias clínicas obtenidas exitosamente",
  "data": {
    "id": 35,
    "paciente_fk": 28,
    "motivo_consulta": "Control - Seguimiento dolor de cabeza",
    "doctor": "5",
    "fecha_creacion": "2025-11-03",
    "fecha_actualizacion": "2025-11-03"
  }
}
```

### Escenario: Obtener Detalle Completo de Historia Clínica

**Request:**
```bash
curl -X GET http://localhost:8000/api/historia/obtener_detalle_historia/35/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "results": {
    "2025-11-03 09:30": [
      {
        "id": 120,
        "historia_fk": 35,
        "respuesta_campo": "Presenta dolores de cabeza intensos hace 2 semanas, acompañados de mareos al levantarse",
        "formulario_fk": 1,
        "campo_fk": 1,
        "fecha_creacion": "2025-11-03T14:30:00Z",
        "fecha_actualizacion": "2025-11-03T14:30:00Z",
        "label_input": "Motivo de Consulta"
      },
      {
        "id": 121,
        "historia_fk": 35,
        "respuesta_campo": "O+",
        "formulario_fk": 1,
        "campo_fk": 2,
        "fecha_creacion": "2025-11-03T14:30:00Z",
        "fecha_actualizacion": "2025-11-03T14:30:00Z",
        "label_input": "Tipo de Sangre"
      },
      {
        "id": 122,
        "historia_fk": 35,
        "respuesta_campo": "75",
        "formulario_fk": 1,
        "campo_fk": 3,
        "fecha_creacion": "2025-11-03T14:30:00Z",
        "fecha_actualizacion": "2025-11-03T14:30:00Z",
        "label_input": "Peso (kg)"
      }
    ],
    "2025-11-03 14:15": [
      {
        "id": 128,
        "historia_fk": 35,
        "respuesta_campo": "Mejoría significativa del dolor de cabeza. Mareos desaparecieron después del tratamiento.",
        "formulario_fk": 1,
        "campo_fk": 1,
        "fecha_creacion": "2025-11-03T19:15:00Z",
        "fecha_actualizacion": "2025-11-03T19:15:00Z",
        "label_input": "Motivo de Consulta"
      },
      {
        "id": 129,
        "historia_fk": 35,
        "respuesta_campo": "74",
        "formulario_fk": 1,
        "campo_fk": 3,
        "fecha_creacion": "2025-11-03T19:15:00Z",
        "fecha_actualizacion": "2025-11-03T19:15:00Z",
        "label_input": "Peso (kg)"
      }
    ]
  },
  "count": 5,
  "groups_count": 2,
  "next": null,
  "previous": null
}
```

---

## 🔗 Integración con DoCalendar

### Paso 1: Configurar Token de Integración

**Request:**
```bash
curl -X POST http://localhost:8000/api/integracion/crear_integracion/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_aplicacion": "DoCalendar",
    "token_aplicacion": "abc123xyz789token_super_secreto"
  }'
```

### Paso 2: Obtener Clientes desde DoCalendar

**Request:**
```bash
curl -X GET "http://localhost:8000/api/integracion/obtener_clientes_externos/?page=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/integracion/obtener_clientes_externos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 101,
      "nombre": "Carlos Méndez",
      "identificacion": "1012345678",
      "telefono": "3201234567",
      "email": "carlos.mendez@ejemplo.com",
      "fecha_nacimiento": "1988-05-20",
      "direccion": "Calle 50 #20-30"
    },
    {
      "id": 102,
      "nombre": "Laura Ramírez",
      "identificacion": "1087654321",
      "telefono": "3159876543",
      "email": "laura.ramirez@ejemplo.com",
      "fecha_nacimiento": "1992-08-15",
      "direccion": "Carrera 15 #40-50"
    }
  ]
}
```

### Paso 3: Buscar Cliente Específico

**Request:**
```bash
curl -X GET "http://localhost:8000/api/integracion/buscar_cliente/?query=Carlos" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "results": [
    {
      "id": 101,
      "nombre": "Carlos Méndez",
      "identificacion": "1012345678",
      "telefono": "3201234567",
      "email": "carlos.mendez@ejemplo.com"
    },
    {
      "id": 145,
      "nombre": "Carlos Alberto Gómez",
      "identificacion": "1098765432",
      "telefono": "3107654321",
      "email": "carlos.gomez@ejemplo.com"
    }
  ],
  "count": 2,
  "next": null,
  "previous": null
}
```

### Paso 4: Crear Cliente en DoCalendar

**Request:**
```bash
curl -X POST http://localhost:8000/api/integracion/crear_cliente/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pedro Sánchez",
    "identificacion": "1023456789",
    "telefono": "3115678901",
    "email": "pedro.sanchez@ejemplo.com",
    "fecha_nacimiento": "1985-12-10",
    "direccion": "Avenida 30 #45-67"
  }'
```

### Paso 5: Obtener Citas Agendadas

**Request:**
```bash
curl -X GET http://localhost:8000/api/integracion/obtener_citas/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "results": [
    {
      "id": 501,
      "paciente": "Carlos Méndez",
      "paciente_id": 101,
      "fecha": "2025-11-05",
      "hora": "10:00",
      "servicio": "Consulta General",
      "doctor": "Dr. Juan Pérez",
      "estado": "Agendada"
    },
    {
      "id": 502,
      "paciente": "Laura Ramírez",
      "paciente_id": 102,
      "fecha": "2025-11-05",
      "hora": "11:30",
      "servicio": "Control Prenatal",
      "doctor": "Dra. María González",
      "estado": "Confirmada"
    }
  ],
  "count": 2,
  "next": null,
  "previous": null
}
```

---

## 💡 Casos de Uso Comunes

### Caso 1: Workflow Completo - Nueva Consulta

1. **Obtener cita del día desde DoCalendar**
2. **Buscar o crear paciente**
3. **Obtener formulario principal**
4. **Crear historia clínica con respuestas**
5. **Guardar firma digital del médico**

**Ejemplo en JavaScript (Frontend):**
```javascript
// 1. Obtener citas del día
const citas = await fetch('/api/integracion/obtener_citas/', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 2. Seleccionar paciente de la cita
const citaActual = citas.results[0];
const clienteFK = citaActual.paciente_id;

// 3. Verificar si existe paciente
let paciente = await fetch(`/api/paciente/get_pacientes/${clienteFK}/`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json()).catch(() => null);

// 4. Obtener formulario principal
const formulario = await fetch('/api/formulario/obtener_formulario/principal/', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 5. Crear historia clínica
const historiaClinica = await fetch('/api/historia/crear_historia_clinica/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    paciente: paciente?.data || {
      fecha_nacimiento: "1990-01-15",
      estado_civil: "soltero",
      eps: "Sanitas",
      vinculacion: "Contributivo",
      ocupacion: "Empleado",
      cliente_FK: clienteFK
    },
    historia_clinica: {
      motivo_consulta: "Consulta programada",
      doctor: usuarioActual.id
    },
    detalle_historia: {
      formulario_fk: formulario.data.formulario.id,
      campos: respuestasFormulario
    }
  })
}).then(r => r.json());
```

### Caso 2: Búsqueda y Visualización de Historial Médico

```javascript
// 1. Buscar paciente
const busqueda = await fetch('/api/integracion/buscar_cliente/?query=Juan', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

const pacienteSeleccionado = busqueda.results[0];

// 2. Obtener datos completos del paciente
const paciente = await fetch(`/api/paciente/get_pacientes/${pacienteSeleccionado.id}/`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 3. Obtener historia clínica
const historia = await fetch(`/api/historia/obtener_historia/${paciente.data.id}/`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// 4. Obtener detalles agrupados por fecha
const detalles = await fetch(`/api/historia/obtener_detalle_historia/${historia.data.id}/`, {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Ahora detalles.results contiene el historial completo agrupado por fecha
```

### Caso 3: Gestión de Formularios Dinámicos

```javascript
// 1. Crear formulario base
const nuevoFormulario = await fetch('/api/formulario/create_formulario/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nombre_formulario: "Evaluación Cardiológica",
    principal: false,
    campos: [
      {
        nombre_campo: "Frecuencia Cardíaca",
        tipo: "number",
        requerido: true,
        opciones: null
      },
      {
        nombre_campo: "Presión Arterial",
        tipo: "text",
        requerido: true,
        opciones: null
      }
    ]
  })
}).then(r => r.json());

// 2. Posteriormente, agregar más campos
const actualizado = await fetch(`/api/formulario/actualizar_campos/${nuevoFormulario.id}/`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    campos_datos: [
      {
        id: "campo_nuevo_1",
        nombre_campo: "Electrocardiograma",
        tipo: "textarea",
        requerido: false,
        opciones: null
      }
    ]
  })
}).then(r => r.json());
```

---

## 🔍 Tips y Buenas Prácticas

### 1. Manejo de Tokens
- Almacenar el refresh token de forma segura
- Renovar el access token antes de que expire
- Manejar errores 401 para re-autenticar

### 2. Validación de Datos
- Siempre validar fechas en formato ISO (YYYY-MM-DD)
- Verificar que los IDs de relaciones existan antes de enviar

### 3. Paginación
- Usar el parámetro `page` para grandes conjuntos de datos
- Verificar los campos `next` y `previous` en las respuestas

### 4. Gestión de Errores
```javascript
async function handleApiCall(url, options) {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!response.ok) {
      // Manejar errores de validación
      if (response.status === 400) {
        console.error('Errores de validación:', data.errors);
      }
      // Manejar token expirado
      if (response.status === 401) {
        await refreshToken();
        return handleApiCall(url, options); // Reintentar
      }
      throw new Error(data.detail || 'Error en la petición');
    }
    
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

---

**Última actualización: 3 de noviembre de 2025**
