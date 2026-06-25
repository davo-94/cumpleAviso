# Manual de Usuario — CumpleAviso

## ¿Qué es CumpleAviso?

CumpleAviso es un sistema de gestión de cumpleaños para equipos de trabajo. Permite registrar colaboradores, elegir su regalo preferido y enviarles automáticamente un correo de felicitación con un código de canje el día de su cumpleaños. También notifica a la empresa y envía recordatorios preventivos.

---

## Acceso al sistema

**URL de producción:** `https://cumpleaviso.vercel.app`

Al ingresar al sistema se muestra la pantalla de inicio de sesión.

### Credenciales

| Campo      | Valor           |
|------------|-----------------|
| Usuario    | test@gap.cl     |
| Contraseña | mvp1234         |

> Las credenciales predeterminadas son de demostración. En un entorno real se configuran mediante variables de entorno en el servidor.

---

## Pantalla principal

Después de iniciar sesión, aparece el panel de administración con cinco pestañas en la parte superior:

| Pestaña              | Función                                          |
|----------------------|--------------------------------------------------|
| **Registrar**        | Agregar un nuevo colaborador al sistema          |
| **Colaboradores**    | Ver, gestionar e inactivar colaboradores         |
| **Historial envíos** | Consultar los correos de regalo enviados         |
| **Logs del job**     | Ver el historial de ejecuciones del job diario   |
| **Vista correo**     | Previsualizar cómo se ven los correos generados  |

En la barra superior también hay un botón **"Ejecutar job ahora"** para disparar manualmente el proceso de cumpleaños (útil para pruebas).

---

## Registrar un colaborador

1. Hacer clic en la pestaña **Registrar**.
2. Completar el formulario:

| Campo              | Tipo       | Obligatorio | Descripción                                      |
|--------------------|------------|-------------|--------------------------------------------------|
| Nombre completo    | Texto      | Sí          | Nombre y apellido del colaborador                |
| Correo electrónico | Email      | Sí          | Debe ser único en el sistema                     |
| Fecha de nacimiento| Fecha      | Sí          | No puede ser futura                              |
| Regalo preferido   | Selección  | Sí          | Cine, Spa o Libro                                |
| Área               | Texto      | No          | Departamento o área de trabajo                   |
| Fecha de ingreso   | Fecha      | No          | Fecha de inicio en la empresa (no puede ser futura) |
| Avisar a empresa   | Checkbox   | No          | Si se activa, envía notificación al email de RR.HH. el día del cumpleaños |

3. Hacer clic en **"Registrar colaborador"**.

Si el email ya existe, el sistema muestra un error de duplicado.

---

## Gestionar colaboradores

En la pestaña **Colaboradores** se muestra la lista de todos los colaboradores registrados con:

- Nombre y foto (si fue subida)
- Email
- Fecha de nacimiento
- Regalo preferido
- Área y antigüedad calculada automáticamente
- Estado (activo / inactivo)

### Subir foto

En cada fila hay un botón de cámara que permite subir una imagen (JPG, PNG, GIF o WebP).

### Inactivar colaborador

Al hacer clic en el ícono de desactivar, el colaborador queda marcado como inactivo y ya no recibirá correos de cumpleaños.

---

## Historial de envíos

La pestaña **Historial de envíos** muestra los últimos 50 correos de regalo enviados, con:

- Nombre y email del colaborador
- Código de canje generado
- Fecha del envío
- Estado: **enviado** o **fallido**

---

## Logs del job

La pestaña **Logs del job** muestra el historial de las últimas 20 ejecuciones del proceso automático, indicando:

- Fecha y hora de ejecución
- Resultado: **ok** o **error**
- Cantidad de cumpleaños encontrados
- Detalle de cada colaborador procesado

---

## Vista de correo

Permite seleccionar un colaborador y tipo de correo para previsualizar cómo quedará el email antes de enviarlo.

### Página de saludo

Desde la vista de correo también se puede abrir la página de cumpleaños personalizada del colaborador, que muestra un diseño visual acorde a su regalo preferido:

- **Cine** → fondo oscuro con tonos cyan
- **Spa** → fondo verde claro
- **Libro** → fondo ámbar

---

## Proceso automático de cumpleaños

El sistema ejecuta automáticamente un job todos los días a las **06:00 AM** (hora del servidor) que:

1. Detecta colaboradores con cumpleaños ese día
2. Genera un código de canje único para cada uno
3. Envía un email de felicitación al colaborador (hasta 3 intentos)
4. Si `Avisar a empresa` está activado, notifica al email de RR.HH. con el área y antigüedad
5. Envía un recordatorio anticipado si hay cumpleaños en los próximos 3 días

---

## Cerrar sesión

Hacer clic en el ícono de salida (→) en la esquina superior derecha del panel. La sesión se almacena en el navegador y se elimina automáticamente al cerrar la ventana.
