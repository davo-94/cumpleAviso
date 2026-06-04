"""
Tests unitarios — HU01: Registro de colaborador con preferencias
Cubre: guardado correcto, email duplicado (409), email inválido (422),
       regalo_pref inválido (422), fecha futura (422).
"""
from tests.conftest import AUTH

COLAB_BASE = {
    "nombre": "Ana García",
    "email": "ana.garcia@test.com",
    "fec_nac": "1990-03-15",
    "regalo_pref": "cine",
    "avisar_empresa": False,
}


# ── HU01: guardado correcto ──────────────────────────────────────────────────

def test_crear_colaborador_exitoso(client):
    res = client.post("/api/colaborador", json=COLAB_BASE, auth=AUTH)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == COLAB_BASE["email"]
    assert data["nombre"] == COLAB_BASE["nombre"]
    assert data["activo"] is True


def test_crear_colaborador_con_area_y_fec_ingreso(client):
    payload = {**COLAB_BASE, "email": "colab2@test.com",
               "area": "Tecnología", "fec_ingreso": "2021-06-01"}
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 201
    data = res.json()
    assert data["area"] == "Tecnología"
    assert data["fec_ingreso"] == "2021-06-01"


# ── HU01: email duplicado → 409 ─────────────────────────────────────────────

def test_email_duplicado_retorna_409(client):
    payload = {**COLAB_BASE, "email": "duplicado@test.com"}
    client.post("/api/colaborador", json=payload, auth=AUTH)
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 409
    assert "ya registrado" in res.json()["detail"].lower()


# ── HU01: validaciones de formato → 422 ─────────────────────────────────────

def test_email_invalido_retorna_422(client):
    payload = {**COLAB_BASE, "email": "no-es-un-email"}
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 422


def test_regalo_pref_invalido_retorna_422(client):
    payload = {**COLAB_BASE, "email": "regalo@test.com", "regalo_pref": "videojuego"}
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 422


def test_fecha_nacimiento_futura_retorna_422(client):
    payload = {**COLAB_BASE, "email": "futuro@test.com", "fec_nac": "2099-01-01"}
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 422


def test_fecha_ingreso_futura_retorna_422(client):
    payload = {**COLAB_BASE, "email": "ingreso@test.com", "fec_ingreso": "2099-12-31"}
    res = client.post("/api/colaborador", json=payload, auth=AUTH)
    assert res.status_code == 422


# ── HU05: listar colaboradores ───────────────────────────────────────────────

def test_listar_colaboradores_retorna_lista(client):
    res = client.get("/api/colaboradores", auth=AUTH)
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# ── Auth: sin credenciales → 401 ────────────────────────────────────────────

def test_sin_auth_retorna_401(client):
    res = client.post("/api/colaborador", json=COLAB_BASE)
    assert res.status_code == 401


def test_credenciales_incorrectas_retorna_401(client):
    res = client.get("/api/colaboradores", auth=("wrong", "wrong"))
    assert res.status_code == 401
