import time
import secrets
from datetime import date, timedelta

from ..database import SessionLocal
from ..models import Colaborador, LogEjecucion, EnvioRegalia, EnvioEmpresa
from .email_service import (
    send_birthday_email,
    send_company_notice,
    send_reminder_email,
)


def _generate_code(colab_id: int, regalo_pref: str) -> str:
    prefix = regalo_pref.upper()[:4]
    token = secrets.token_hex(4).upper()
    return f"{prefix}-{colab_id}-{token}"


def run_birthday_job():
    """HU02: Job diario. Detecta cumpleanos y dispara envios (HU03, HU04, HU06)."""
    db = SessionLocal()
    today = date.today()
    en_3_dias = today + timedelta(days=3)
    resultados = []

    try:
        activos = db.query(Colaborador).filter(Colaborador.activo == True).all()

        # HU02: cumpleanos de hoy
        hoy_cumple = [
            c for c in activos
            if c.fec_nac.month == today.month and c.fec_nac.day == today.day
        ]

        for colab in hoy_cumple:
            # HU03: envio de regalia con hasta 3 intentos
            codigo = _generate_code(colab.id, colab.regalo_pref)
            exito_email = False
            for intento in range(3):
                exito_email = send_birthday_email(
                    colab.nombre, colab.email, colab.regalo_pref, codigo
                )
                if exito_email:
                    break
                if intento < 2:
                    time.sleep(2)

            envio = EnvioRegalia(
                id_colab=colab.id,
                nombre_colab=colab.nombre,
                email_colab=colab.email,
                codigo=codigo,
                estado_envio="enviado" if exito_email else "fallido",
            )
            db.add(envio)

            # HU04: aviso a empresa (solo si autorizado)
            if colab.avisar_empresa:
                exito_empresa = send_company_notice(colab.nombre, colab.regalo_pref)
                from .email_service import EMPRESA_EMAIL
                db.add(EnvioEmpresa(
                    id_colab=colab.id,
                    nombre_colab=colab.nombre,
                    destinatario=EMPRESA_EMAIL,
                    exito=exito_empresa,
                    tipo="cumpleanos",
                ))

            resultados.append(
                f"{colab.nombre}: {'enviado' if exito_email else 'fallido'}"
            )

        # HU06: recordatorio 3 dias antes
        proximos = [
            c for c in activos
            if c.fec_nac.month == en_3_dias.month and c.fec_nac.day == en_3_dias.day
        ]
        if proximos:
            datos = [
                {
                    "nombre": c.nombre,
                    "fecha": en_3_dias.strftime("%d/%m/%Y"),
                    "regalo_pref": c.regalo_pref,
                }
                for c in proximos
            ]
            send_reminder_email(datos)
            from .email_service import EMPRESA_EMAIL
            for c in proximos:
                db.add(EnvioEmpresa(
                    id_colab=c.id,
                    nombre_colab=c.nombre,
                    destinatario=EMPRESA_EMAIL,
                    exito=True,
                    tipo="recordatorio",
                ))
            resultados.append(
                f"Recordatorio: {', '.join(c.nombre for c in proximos)}"
            )

        db.add(LogEjecucion(
            resultado="ok",
            cantidad_encontrados=len(hoy_cumple),
            detalle="; ".join(resultados) if resultados else "Sin cumpleanos hoy",
        ))
        db.commit()
        print(f"[JOB] Ejecutado — {len(hoy_cumple)} cumpleanos hoy")

    except Exception as e:
        db.add(LogEjecucion(resultado="error", cantidad_encontrados=0, detalle=str(e)))
        db.commit()
        print(f"[JOB] Error: {e}")
    finally:
        db.close()
