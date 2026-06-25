/**
 * api.js — Capa de acceso a la API REST del backend.
 *
 * Centraliza todas las llamadas HTTP para que los componentes no tengan
 * URLs hardcodeadas ni lógica de red dispersa.
 *
 * VITE_API_URL se resuelve en tiempo de build (no en runtime).
 * En producción apunta a Railway; en desarrollo local queda vacío
 * y las rutas son relativas al mismo servidor.
 *
 * Convención de errores: si el servidor devuelve 401, se lanza un objeto
 * con { status: 401 } para que App.jsx pueda detectarlo y hacer logout.
 */
const BASE = import.meta.env.VITE_API_URL || '';

/** Construye los headers con autenticación Basic y Content-Type JSON. */
function authHeaders(token) {
  return {
    'Content-Type': 'application/json',
    Authorization: `Basic ${token}`,
  };
}

export const api = {
  /** Obtiene la lista de todos los colaboradores. */
  async getColaboradores(token) {
    const res = await fetch(`${BASE}/api/colaboradores`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar colaboradores');
    return res.json();
  },

  /** Crea un nuevo colaborador. Lanza el mensaje de error del servidor si falla. */
  async createColaborador(data, token) {
    const res = await fetch(`${BASE}/api/colaborador`, {
      method: 'POST',
      headers: authHeaders(token),
      body: JSON.stringify(data),
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Error al crear colaborador');
    }
    return res.json();
  },

  /**
   * Sube la foto de un colaborador como multipart/form-data.
   * No usa authHeaders() porque FormData no lleva Content-Type manual
   * (el navegador lo agrega automáticamente con el boundary correcto).
   */
  async uploadFoto(id, file, token) {
    const fd = new FormData();
    fd.append('foto', file);
    const res = await fetch(`${BASE}/api/colaborador/${id}/foto`, {
      method: 'POST',
      headers: { Authorization: `Basic ${token}` },
      body: fd,
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al subir foto');
    return res.json();
  },

  /** Marca un colaborador como inactivo (ya no recibe notificaciones). */
  async inactivarColaborador(id, token) {
    const res = await fetch(`${BASE}/api/colaborador/${id}/inactivar`, {
      method: 'PATCH',
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al inactivar colaborador');
    return res.json();
  },

  /** Obtiene el historial de los últimos 50 envíos de regalías. */
  async getEnvios(token) {
    const res = await fetch(`${BASE}/api/envios`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar envíos');
    return res.json();
  },

  /** Obtiene el historial de las últimas 20 ejecuciones del job. */
  async getLogs(token) {
    const res = await fetch(`${BASE}/api/logs`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar logs');
    return res.json();
  },

  /** Dispara manualmente el job de cumpleaños (útil para pruebas). */
  async ejecutarJob(token) {
    const res = await fetch(`${BASE}/api/jobs/ejecutar`, {
      method: 'POST',
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al ejecutar job');
    return res.json();
  },
};
