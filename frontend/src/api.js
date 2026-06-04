const BASE = import.meta.env.VITE_API_URL || '';

export const api = {
  async getColaboradores() {
    const res = await fetch(`${BASE}/api/colaboradores`);
    if (!res.ok) throw new Error('Error al cargar colaboradores');
    return res.json();
  },

  async createColaborador(data) {
    const res = await fetch(`${BASE}/api/colaborador`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Error al crear colaborador');
    }
    return res.json();
  },

  async uploadFoto(id, file) {
    const fd = new FormData();
    fd.append('foto', file);
    const res = await fetch(`${BASE}/api/colaborador/${id}/foto`, { method: 'POST', body: fd });
    if (!res.ok) throw new Error('Error al subir foto');
    return res.json();
  },

  async inactivarColaborador(id) {
    const res = await fetch(`${BASE}/api/colaborador/${id}/inactivar`, { method: 'PATCH' });
    if (!res.ok) throw new Error('Error al inactivar colaborador');
    return res.json();
  },

  async getEnvios() {
    const res = await fetch(`${BASE}/api/envios`);
    if (!res.ok) throw new Error('Error al cargar envíos');
    return res.json();
  },

  async getLogs() {
    const res = await fetch(`${BASE}/api/logs`);
    if (!res.ok) throw new Error('Error al cargar logs');
    return res.json();
  },

  async ejecutarJob() {
    const res = await fetch(`${BASE}/api/jobs/ejecutar`, { method: 'POST' });
    if (!res.ok) throw new Error('Error al ejecutar job');
    return res.json();
  },
};
