"""
auth.py — Autenticación HTTP Basic para la API.

Todos los endpoints protegidos reciben esta dependencia (require_auth).
FastAPI la resuelve automáticamente y devuelve 401 si faltan o son incorrectas.

Las credenciales se configuran con variables de entorno (ADMIN_USER, ADMIN_PASS).
Si no están definidas, se usan los valores por defecto de demostración.
"""
import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

ADMIN_USER = os.getenv("ADMIN_USER", "test@gap.cl")
ADMIN_PASS = os.getenv("ADMIN_PASS", "mvp1234")


def require_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Verifica usuario y contraseña contra las credenciales configuradas.

    secrets.compare_digest() previene ataques de timing: compara byte a byte
    en tiempo constante, sin cortocircuitar al encontrar la primera diferencia.
    Una comparación normal (==) podría filtrar información sobre cuántos
    caracteres coinciden según el tiempo de respuesta.

    Retorna el nombre de usuario si la autenticación es exitosa.
    """
    user_ok = secrets.compare_digest(credentials.username.encode(), ADMIN_USER.encode())
    pass_ok = secrets.compare_digest(credentials.password.encode(), ADMIN_PASS.encode())
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
