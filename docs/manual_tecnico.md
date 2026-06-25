# Manual Técnico — CumpleAviso

## Descripción general

CumpleAviso es una aplicación web de gestión de cumpleaños corporativos. El sistema detecta automáticamente qué colaboradores cumplen años cada día y dispara un flujo de notificaciones por correo electrónico.

**URL de producción:**
- Frontend: `https://cumpleaviso.vercel.app`
- Backend/API: `https://cumpleaviso-production.up.railway.app`

---

## Stack tecnológico

### Backend
| Tecnología      | Versión   | Rol                                      |
|-----------------|-----------|------------------------------------------|
| Python          | 3.11+     | Lenguaje principal                       |
| FastAPI         | ≥ 0.100   | Framework web y definición de API REST   |
| SQLAlchemy      | ≥ 2.0     | ORM para acceso a base de datos          |
| Pydantic v2     | ≥ 2.0     | Validación de esquemas y serialización   |
| APScheduler     | ≥ 3.10    | Scheduler en background para job diario  |
| Uvicorn         | ≥ 0.23    | Servidor ASGI                            |
| psycopg2-binary | ≥ 2.9     | Driver PostgreSQL                        |
| pytest + httpx  | ≥ 8.0     | Framework de testing                     |

### Frontend
| Tecnología    | Versión | Rol                                     |
|---------------|---------|-----------------------------------------|
| React         | 18      | Librería de interfaz de usuario         |
| Vite          | 6       | Bundler y servidor de desarrollo        |
| Tailwind CSS  | 3       | Framework de estilos utilitarios        |
| Lucide React  | —       | Iconografía                             |

### Infraestructura
| Servicio  | Rol                                               |
|-----------|---------------------------------------------------|
| Railway   | Hosting del backend + base de datos PostgreSQL    |
| Vercel    | Hosting del frontend (SPA estático)               |

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────┐
│               Frontend (Vercel)              │
│         React + Vite + Tailwind CSS          │
│  cumpleaviso.vercel.app                      │
└──────────────────┬──────────────────────────┘
                   │ HTTPS + HTTP Basic Auth
                   ▼
┌─────────────────────────────────────────────┐
│               Backend (Railway)              │
│            FastAPI + Uvicorn                 │
│  cumpleaviso-production.up.railway.app       │
│                                              │
│  ┌─────────────┐   ┌────────────────────┐   │
│  │  API REST   │   │  APScheduler       │   │
│  │  /api/*     │   │  job diario 06:00  │   │
│  └──────┬──────┘   └────────┬───────────┘   │
│         │                   │               │
│         ▼                   ▼               │
│  ┌────────────────────────────────────────┐ │
│  │        SQLAlchemy ORM                  │ │
│  └────────────────────┬───────────────────┘ │
└───────────────────────┼─────────────────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │   PostgreSQL (Railway)  │
          │   SQLite (desarrollo)   │
          └─────────────────────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │    SMTP (Gmail)         │
          │  Correos automáticos    │
          └─────────────────────────┘
```

---

## Estructura del proyecto

```
cumpleAviso/
├── backend/
│   ├── app/
│   │   ├── main.py              # Punto de entrada FastAPI, migraciones, SPA fallback
│   │   ├── database.py          # Configuración del engine SQLAlchemy
│   │   ├── models.py            # Modelos ORM (tablas de base de datos)
│   │   ├── schemas.py           # Schemas Pydantic (validación de entrada/salida)
│   │   ├── auth.py              # Autenticación HTTP Basic
│   │   ├── scheduler.py         # Configuración de APScheduler
│   │   ├── seed.py              # Datos de prueba para desarrollo
│   │   ├── routers/
│   │   │   ├── colaboradores.py # Endpoints CRUD de colaboradores
│   │   │   └── envios.py        # Endpoints de historial y ejecución manual
│   │   └── services/
│   │       ├── birthday_job.py  # Lógica del job diario de cumpleaños
│   │       └── email_service.py # Construcción y envío de correos HTML
│   ├── tests/
│   │   ├── conftest.py          # Fixtures de pytest (BD de test, cliente HTTP)
│   │   └── test_colaboradores.py# Tests unitarios de la API
│   ├── requirements.txt
│   └── run.py                   # Arranque local con hot-reload
├── frontend/
│   ├── src/
│   │   ├── main.jsx             # Punto de entrada React
│   │   ├── App.jsx              # Componente raíz, routing entre vistas
│   │   ├── api.js               # Capa de acceso a la API REST
│   │   └── views/
│   │       ├── LoginForm.jsx    # Formulario de autenticación
│   │       ├── RegisterForm.jsx # Formulario de registro de colaborador
│   │       ├── ColaboradoresList.jsx # Lista y gestión de colaboradores
│   │       ├── EnviosHistorial.jsx   # Historial de envíos de regalías
│   │       ├── JobLogs.jsx           # Historial de ejecuciones del job
│   │       ├── EmailPreview.jsx      # Vista previa de correos
│   │       └── GreetingPage.jsx      # Página de cumpleaños del colaborador
│   ├── vite.config.js
│   └── package.json
└── docs/
    ├── manual_usuario.md
    ├── manual_tecnico.md
    └── despliegue.md
```

---

## Modelo de datos

### Tabla `colaboradores`

| Columna        | Tipo      | Descripción                                     |
|----------------|-----------|-------------------------------------------------|
| id             | INTEGER   | Clave primaria autoincremental                  |
| nombre         | VARCHAR   | Nombre completo (obligatorio)                   |
| email          | VARCHAR   | Email único (obligatorio)                       |
| fec_nac        | DATE      | Fecha de nacimiento (obligatorio, no futura)    |
| regalo_pref    | VARCHAR   | Preferencia: `cine`, `spa` o `libro`            |
| activo         | BOOLEAN   | Si es falso, no recibe correos                  |
| avisar_empresa | BOOLEAN   | Si es verdadero, notifica a RR.HH.              |
| foto           | VARCHAR   | Nombre del archivo de foto (nullable)           |
| area           | VARCHAR   | Área o departamento (nullable)                  |
| fec_ingreso    | DATE      | Fecha de ingreso a la empresa (nullable)        |
| created_at     | DATETIME  | Timestamp de creación (automático)              |

### Tabla `logs_ejecucion`

| Columna             | Tipo     | Descripción                         |
|---------------------|----------|-------------------------------------|
| id                  | INTEGER  | Clave primaria                      |
| fecha               | DATETIME | Timestamp de ejecución              |
| resultado           | VARCHAR  | `ok` o `error`                      |
| cantidad_encontrados| INTEGER  | Colaboradores con cumpleaños ese día|
| detalle             | TEXT     | Resumen detallado de la ejecución   |

### Tabla `envios_regalias`

| Columna      | Tipo     | Descripción                              |
|--------------|----------|------------------------------------------|
| id           | INTEGER  | Clave primaria                           |
| id_colab     | INTEGER  | ID del colaborador                       |
| nombre_colab | VARCHAR  | Nombre al momento del envío              |
| email_colab  | VARCHAR  | Email al momento del envío               |
| fecha        | DATETIME | Timestamp del envío                      |
| codigo       | VARCHAR  | Código de canje único (ej: `CINE-3-A2B4C5D6`) |
| estado_envio | VARCHAR  | `enviado` o `fallido`                    |

### Tabla `envios_empresa`

| Columna      | Tipo     | Descripción                              |
|--------------|----------|------------------------------------------|
| id           | INTEGER  | Clave primaria                           |
| id_colab     | INTEGER  | ID del colaborador                       |
| nombre_colab | VARCHAR  | Nombre del colaborador                   |
| fecha        | DATETIME | Timestamp del envío                      |
| destinatario | VARCHAR  | Email de RR.HH. que recibió el aviso     |
| exito        | BOOLEAN  | Si el envío fue exitoso                  |
| tipo         | VARCHAR  | `cumpleanos` o `recordatorio`            |

---

## API REST

Todos los endpoints requieren autenticación HTTP Basic (`Authorization: Basic <base64(user:pass)>`).

### Colaboradores

| Método | Endpoint                         | Descripción                         |
|--------|----------------------------------|-------------------------------------|
| POST   | `/api/colaborador`               | Registrar nuevo colaborador         |
| GET    | `/api/colaboradores`             | Listar todos los colaboradores      |
| PATCH  | `/api/colaborador/{id}/inactivar`| Inactivar un colaborador            |
| POST   | `/api/colaborador/{id}/foto`     | Subir foto del colaborador          |

### Envíos y jobs

| Método | Endpoint           | Descripción                                   |
|--------|--------------------|-----------------------------------------------|
| GET    | `/api/envios`      | Últimos 50 envíos de regalías                 |
| GET    | `/api/logs`        | Últimas 20 ejecuciones del job                |
| POST   | `/api/jobs/ejecutar` | Disparar manualmente el job de cumpleaños   |

### Validaciones de entrada (422)

- `email` debe tener formato válido
- `regalo_pref` solo acepta `"cine"`, `"spa"` o `"libro"`
- `fec_nac` no puede ser una fecha presente o futura
- `fec_ingreso` no puede ser una fecha futura

---

## Autenticación

Se utiliza **HTTP Basic Authentication**. El token se calcula en el cliente como `btoa("usuario:contraseña")` y se envía en el header `Authorization: Basic <token>`.

La comparación de credenciales usa `secrets.compare_digest()` para prevenir ataques de timing.

Las credenciales se configuran en el servidor mediante variables de entorno:
- `ADMIN_USER` (por defecto: `test@gap.cl`)
- `ADMIN_PASS` (por defecto: `mvp1234`)

---

## Job de cumpleaños

El job se ejecuta diariamente a las **06:00 AM** usando APScheduler con un trigger cron. La lógica está en `backend/app/services/birthday_job.py`:

1. Consulta todos los colaboradores activos
2. Filtra los que cumplen años hoy (compara mes y día)
3. Para cada uno, genera un código de canje único (`PREFIX-ID-HEX8`)
4. Envía el correo de regalo (hasta 3 reintentos con 2 segundos entre cada uno)
5. Si `avisar_empresa` está activo, envía notificación al email corporativo
6. Filtra colaboradores con cumpleaños en 3 días y envía recordatorio
7. Registra el resultado en la tabla `logs_ejecucion`

---

## Migraciones

El sistema usa un mecanismo ligero de migraciones en `main.py`: al arrancar, ejecuta sentencias `ALTER TABLE` en conexiones independientes. Si la columna ya existe, el error se ignora silenciosamente.

> Cada migración usa su propia conexión porque PostgreSQL aborta toda la transacción al encontrar un error; con una sola conexión compartida, una migración fallida bloquearía las siguientes.

---

## Tests

Los tests se ubican en `backend/tests/` y usan pytest con FastAPI `TestClient`.

**Configuración (`conftest.py`):**
- Base de datos SQLite separada (`test_temp.db`) que se crea y destruye por sesión
- Override de la dependencia `get_db` para usar la BD de test
- Credenciales fijas mediante variables de entorno

**Cobertura de `test_colaboradores.py` (10 tests):**

| Test                                    | Caso                                    |
|-----------------------------------------|-----------------------------------------|
| `test_crear_colaborador_exitoso`        | Creación correcta → 201                 |
| `test_crear_colaborador_con_area_y_fec_ingreso` | Campos opcionales → 201         |
| `test_email_duplicado_retorna_409`      | Email repetido → 409                    |
| `test_email_invalido_retorna_422`       | Formato de email inválido → 422         |
| `test_regalo_pref_invalido_retorna_422` | Valor no permitido → 422                |
| `test_fecha_nacimiento_futura_retorna_422` | Fecha futura → 422                   |
| `test_fecha_ingreso_futura_retorna_422` | Fecha de ingreso futura → 422           |
| `test_listar_colaboradores_retorna_lista` | GET lista → 200 + array              |
| `test_sin_auth_retorna_401`             | Sin credenciales → 401                  |
| `test_credenciales_incorrectas_retorna_401` | Credenciales erróneas → 401         |

**Ejecutar tests:**
```bash
cd backend
pytest tests/ -v
```
