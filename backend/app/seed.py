from datetime import date
from .database import SessionLocal
from .models import Colaborador


COLABORADORES_PRUEBA = [
    dict(nombre="María González",   email="maria.gonzalez@empresa.com",  fec_nac=date(1990,  6,  4), regalo_pref="spa",   avisar_empresa=True,  area="Recursos Humanos",  fec_ingreso=date(2019, 3, 10)),
    dict(nombre="Carlos Pérez",     email="carlos.perez@empresa.com",    fec_nac=date(1988,  6,  4), regalo_pref="cine",  avisar_empresa=True,  area="Tecnología",        fec_ingreso=date(2021, 7,  1)),
    dict(nombre="Sofía Ramírez",    email="sofia.ramirez@empresa.com",   fec_nac=date(1995,  8, 15), regalo_pref="libro", avisar_empresa=False, area="Marketing",         fec_ingreso=date(2022, 1, 20)),
    dict(nombre="Diego Morales",    email="diego.morales@empresa.com",   fec_nac=date(1992, 11, 22), regalo_pref="cine",  avisar_empresa=True,  area="Ventas",            fec_ingreso=date(2020, 5, 15)),
    dict(nombre="Valentina Torres", email="valentina.torres@empresa.com",fec_nac=date(1993,  3,  8), regalo_pref="spa",   avisar_empresa=False, area="Finanzas",          fec_ingreso=date(2023, 9,  5)),
]


def seed_db():
    db = SessionLocal()
    try:
        if db.query(Colaborador).count() > 0:
            return
        for data in COLABORADORES_PRUEBA:
            db.add(Colaborador(**data))
        db.commit()
        print(f"[SEED] {len(COLABORADORES_PRUEBA)} colaboradores de prueba insertados")
    except Exception as e:
        print(f"[SEED] Error: {e}")
        db.rollback()
    finally:
        db.close()
