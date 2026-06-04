const BASE = import.meta.env.VITE_API_URL || '';

function authHeaders(token) {
  return {
    'Content-Type': 'application/json',
    Authorization: `Basic ${token}`,
  };
}

export const api = {
  async getColaboradores(token) {
    const res = await fetch(`${BASE}/api/colaboradores`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar colaboradores');
    return res.json();
  },

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

  async inactivarColaborador(id, token) {
    const res = await fetch(`${BASE}/api/colaborador/${id}/inactivar`, {
      method: 'PATCH',
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al inactivar colaborador');
    return res.json();
  },

  async getEnvios(token) {
    const res = await fetch(`${BASE}/api/envios`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar envíos');
    return res.json();
  },

  async getLogs(token) {
    const res = await fetch(`${BASE}/api/logs`, {
      headers: { Authorization: `Basic ${token}` },
    });
    if (res.status === 401) throw Object.assign(new Error('Sesión expirada'), { status: 401 });
    if (!res.ok) throw new Error('Error al cargar logs');
    return res.json();
  },

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
