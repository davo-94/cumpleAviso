import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMPRESA_EMAIL = os.getenv("EMPRESA_EMAIL", "rrhh@empresa.com")

REGALO_LABEL = {
    "cine": "Entrada 2D al cine",
    "spa": "Voucher de spa (1 hora)",
    "libro": "Voucher para libro (a elección)",
}


def _send(to: str, subject: str, html: str) -> bool:
    if not SMTP_USER or not SMTP_PASS:
        print(f"[EMAIL] Sin credenciales — simulando envío a {to}: {subject}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to, msg.as_string())
        print(f"[EMAIL] Enviado a {to}: {subject}")
        return True
    except Exception as e:
        print(f"[EMAIL] Error al enviar a {to}: {e}")
        return False


def send_birthday_email(nombre: str, email: str, regalo_pref: str, codigo: str) -> bool:
    regalo = REGALO_LABEL.get(regalo_pref, regalo_pref)
    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
      <h2 style="color:#2563eb">Feliz cumpleanos, {nombre}!</h2>
      <p>En este dia especial, queremos celebrarte con un regalo:</p>
      <p style="font-size:18px"><strong>Regalo: {regalo}</strong></p>
      <p>Tu codigo unico de canje:</p>
      <p style="background:#f3f4f6;padding:16px;font-family:monospace;font-size:20px;
                 letter-spacing:2px;text-align:center">{codigo}</p>
      <p style="color:#6b7280;font-size:12px">Valido por 90 dias desde hoy.</p>
      <p>Que tengas un excelente dia!</p>
      <p><em>El equipo de RR.HH.</em></p>
    </body></html>
    """
    return _send(email, f"Feliz cumpleanos {nombre} — Tu regalo de hoy", html)


def _calcular_antiguedad(fec_ingreso) -> str:
    if not fec_ingreso:
        return "No especificada"
    from datetime import date
    today = date.today()
    years = today.year - fec_ingreso.year - (
        (today.month, today.day) < (fec_ingreso.month, fec_ingreso.day)
    )
    if years >= 1:
        return f"{years} año{'s' if years > 1 else ''}"
    months = (today.year - fec_ingreso.year) * 12 + today.month - fec_ingreso.month
    return f"{months} mes{'es' if months != 1 else ''}"


def send_company_notice(
    nombre: str,
    regalo_pref: str,
    area: str = None,
    fec_ingreso=None,
) -> bool:
    regalo = REGALO_LABEL.get(regalo_pref, regalo_pref)
    antiguedad = _calcular_antiguedad(fec_ingreso)
    area_str = area or "No especificada"
    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
      <h2 style="color:#16a34a">Aviso de cumpleanos</h2>
      <p>Hoy es el cumpleanos de <strong>{nombre}</strong>.</p>
      <table style="border-collapse:collapse;width:100%;margin:16px 0">
        <tr><td style="padding:6px 12px;color:#6b7280">Área</td>
            <td style="padding:6px 12px;font-weight:bold">{area_str}</td></tr>
        <tr style="background:#f9fafb">
            <td style="padding:6px 12px;color:#6b7280">Antigüedad</td>
            <td style="padding:6px 12px;font-weight:bold">{antiguedad}</td></tr>
        <tr><td style="padding:6px 12px;color:#6b7280">Regalo entregado</td>
            <td style="padding:6px 12px;font-weight:bold">{regalo}</td></tr>
      </table>
      <p><em>Sistema CumpleAviso</em></p>
    </body></html>
    """
    return _send(EMPRESA_EMAIL, f"Hoy es el cumpleanos de {nombre}", html)


def send_reminder_email(proximos: list) -> bool:
    if not proximos:
        return False
    rows = "".join(
        f"<tr><td style='padding:8px'>{c['nombre']}</td>"
        f"<td style='padding:8px'>{c['fecha']}</td>"
        f"<td style='padding:8px'>{REGALO_LABEL.get(c['regalo_pref'], c['regalo_pref'])}</td></tr>"
        for c in proximos
    )
    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
      <h2 style="color:#d97706">Recordatorio: Proximos cumpleanos (en 3 dias)</h2>
      <table border="1" cellspacing="0" style="border-collapse:collapse;width:100%">
        <tr style="background:#f3f4f6">
          <th style="padding:8px">Nombre</th>
          <th style="padding:8px">Fecha</th>
          <th style="padding:8px">Regalo preferido</th>
        </tr>
        {rows}
      </table>
      <p><em>Sistema CumpleAviso</em></p>
    </body></html>
    """
    return _send(
        EMPRESA_EMAIL,
        f"Proximos cumpleanos en 3 dias ({len(proximos)} colaborador/es)",
        html,
    )
