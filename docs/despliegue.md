# Documentación de Despliegue — CumpleAviso

## Requisitos previos

| Herramienta | Versión mínima | Instalación                     |
|-------------|----------------|---------------------------------|
| Python      | 3.11           | https://www.python.org/downloads |
| Node.js     | 18             | https://nodejs.org              |
| Git         | cualquiera     | https://git-scm.com             |

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/david-vasquez-o/cumpleAviso.git
cd cumpleAviso
```

---

## 2. Levantar el backend localmente

### 2.1 Crear entorno virtual

```bash
cd backend
python -m venv venv
```

**Activar el entorno:**
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### 2.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2.3 Configurar variables de entorno

Crear el archivo `backend/.env` con el siguiente contenido:

```env
# Base de datos (dejar vacío para usar SQLite local)
DATABASE_URL=

# Credenciales de administrador
ADMIN_USER=test@gap.cl
ADMIN_PASS=mvp1234

# SMTP para envío de correos (opcional en desarrollo)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
EMPRESA_EMAIL=rrhh@empresa.com
```

> Si `SMTP_USER` y `SMTP_PASS` están vacíos, el sistema simula los envíos imprimiendo en consola.

### 2.4 Ejecutar el servidor

```bash
python run.py
```

El servidor queda disponible en `http://localhost:8000`.

Al arrancar por primera vez:
1. Se crea la base de datos SQLite `backend/cumpleaviso.db`
2. Se insertan 5 colaboradores de prueba automáticamente
3. Se inicia el scheduler (job diario a las 06:00)

---

## 3. Levantar el frontend localmente

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

> En desarrollo local, la variable `VITE_API_URL` no es necesaria: las llamadas a la API van relativas (por defecto al mismo host). Si el backend corre en otro puerto, crear `frontend/.env.local`:
> ```
> VITE_API_URL=http://localhost:8000
> ```

---

## 4. Ejecutar los tests

```bash
cd backend
pytest tests/ -v
```

La suite crea una base de datos SQLite temporal (`test_temp.db`) que se elimina al finalizar.

---

## 5. Compilar el frontend para producción

```bash
cd frontend
npm run build
```

Esto genera la carpeta `frontend/dist/` con los archivos estáticos. El backend FastAPI sirve estos archivos directamente cuando existe esa carpeta.

---

## 6. Despliegue en Railway (backend + base de datos)

Railway es la plataforma donde corre el backend Python y la base de datos PostgreSQL.

### 6.1 Crear cuenta y proyecto

1. Ir a [railway.app](https://railway.app) y crear una cuenta
2. Crear un nuevo proyecto: **New Project → Deploy from GitHub repo**
3. Conectar el repositorio `cumpleAviso`

### 6.2 Agregar PostgreSQL

En el proyecto de Railway:
1. Clic en **+ New** → **Database** → **PostgreSQL**
2. Railway crea la BD y expone la variable `DATABASE_URL` automáticamente

### 6.3 Configurar el servicio de backend

En el servicio del repositorio, ir a **Settings**:

- **Root Directory:** `backend`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 6.4 Variables de entorno en Railway

En la pestaña **Variables** del servicio:

| Variable       | Valor                  |
|----------------|------------------------|
| `ADMIN_USER`   | `test@gap.cl`          |
| `ADMIN_PASS`   | `mvp1234`              |
| `SMTP_USER`    | tu correo Gmail        |
| `SMTP_PASS`    | contraseña de aplicación Gmail |
| `EMPRESA_EMAIL`| email de RR.HH.        |

> `DATABASE_URL` se inyecta automáticamente desde el servicio PostgreSQL.

### 6.5 Build del frontend antes del deploy

El backend sirve el frontend compilado desde `frontend/dist/`. Es necesario compilar el frontend antes de cada despliegue o incluirlo en el repositorio:

```bash
cd frontend
npm run build
git add frontend/dist
git commit -m "build: compilar frontend para deploy"
git push
```

---

## 7. Despliegue en Vercel (frontend)

Vercel sirve el frontend como una SPA estática, con redirecciones hacia `index.html` para el enrutamiento del cliente.

### 7.1 Conectar repositorio

1. Ir a [vercel.com](https://vercel.com) y crear una cuenta
2. **New Project → Import Git Repository** → seleccionar `cumpleAviso`
3. Configurar:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### 7.2 Variable de entorno en Vercel

| Variable       | Valor                                              |
|----------------|----------------------------------------------------|
| `VITE_API_URL` | `https://cumpleaviso-production.up.railway.app`    |

> Es obligatorio incluir `https://`. Sin el protocolo, la URL se trata como ruta relativa.

> Vite incorpora esta variable en el bundle en tiempo de build, no en tiempo de ejecución. Cambiar la variable requiere un nuevo deploy.

### 7.3 Configurar SPA fallback

Crear el archivo `frontend/public/vercel.json`:

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

Esto redirige cualquier ruta directa (p. ej., `cumpleaviso.vercel.app/cualquier-ruta`) al `index.html` para que React maneje el enrutamiento.

---

## 8. Configurar SMTP (Gmail)

Para envío real de correos:

1. Habilitar **Verificación en dos pasos** en la cuenta Gmail
2. Ir a **Gestionar tu cuenta Google → Seguridad → Contraseñas de aplicación**
3. Generar una contraseña de aplicación para "Correo"
4. Usar esa contraseña de 16 caracteres como `SMTP_PASS`

---

## 9. Verificar que el sistema funciona

1. Abrir `https://cumpleaviso.vercel.app`
2. Iniciar sesión con `test@gap.cl` / `mvp1234`
3. En la pestaña **Colaboradores** deberían aparecer los 5 colaboradores de prueba
4. Hacer clic en **"Ejecutar job ahora"** y revisar la pestaña **Logs del job**

---

## 10. Troubleshooting común

### Railway: `RuntimeError: Directory '/frontend' does not exist`

El backend intenta servir `frontend/dist/` pero no existe. Solución: compilar el frontend y subir `dist/` al repositorio, o quitar el mount condicional si solo se usa la API.

### Vercel: URL mal construida (concatenación de dominio)

Si `VITE_API_URL` se configura sin `https://`, Vite lo trata como ruta relativa. Verificar que el valor incluye el protocolo completo: `https://cumpleaviso-production.up.railway.app`.

### Railway: `psycopg2.errors.UndefinedColumn`

PostgreSQL aborta toda la transacción al encontrar un error. Si varias migraciones comparten una conexión, una falla bloquea las siguientes. La solución aplicada es ejecutar cada `ALTER TABLE` en una conexión independiente.

### Tests: `ImportError` al correr pytest

Verificar que el entorno virtual esté activo y que pytest se ejecuta desde la carpeta `backend/`:
```bash
cd backend
pytest tests/ -v
```
