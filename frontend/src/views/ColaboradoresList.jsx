import { useState, useEffect } from 'react';
import { Users, RefreshCw, Camera } from 'lucide-react';
import { api } from '../api.js';

const REGALO_STYLE = {
  cine:  'bg-purple-100 text-purple-700',
  spa:   'bg-pink-100 text-pink-700',
  libro: 'bg-yellow-100 text-yellow-700',
};
const REGALO_LABEL = { cine: '🎬 Cine', spa: '🌿 Spa', libro: '📚 Libro' };

function calcAntigüedad(fecIngreso) {
  if (!fecIngreso) return '—';
  const diff = Date.now() - new Date(fecIngreso).getTime();
  const years = Math.floor(diff / (365.25 * 24 * 60 * 60 * 1000));
  if (years >= 1) return `${years} año${years > 1 ? 's' : ''}`;
  const months = Math.floor(diff / (30.44 * 24 * 60 * 60 * 1000));
  return `${months} mes${months !== 1 ? 'es' : ''}`;
}

export default function ColaboradoresList({ token, showToast, onAuthError }) {
  const [colabs, setColabs] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setColabs(await api.getColaboradores(token)); }
    catch (err) { onAuthError(err); }
    finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  async function handleInactivar(id, nombre) {
    if (!confirm(`¿Deshabilitar a ${nombre}? Ya no recibirá saludos de cumpleaños.`)) return;
    try {
      await api.inactivarColaborador(id, token);
      showToast(`${nombre} deshabilitado`);
      load();
    } catch (err) { onAuthError(err); }
  }

  async function handleSubirFoto(id, file) {
    try {
      await api.uploadFoto(id, file, token);
      showToast('Foto actualizada');
      load();
    } catch (err) { onAuthError(err); }
  }

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border-t-4 border-indigo-500">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Users className="text-indigo-500" size={22} />
          <h2 className="text-lg font-bold text-gray-800">Colaboradores registrados</h2>
        </div>
        <button onClick={load} className="text-sm text-indigo-600 hover:underline flex items-center gap-1">
          <RefreshCw size={14} /> Actualizar
        </button>
      </div>

      <div className="overflow-x-auto">
        {loading ? (
          <p className="text-center py-10 text-gray-400">Cargando...</p>
        ) : colabs.length === 0 ? (
          <p className="text-center py-10 text-gray-400">Sin colaboradores registrados</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
              <tr>
                <th className="px-4 py-3 text-left">Foto</th>
                <th className="px-4 py-3 text-left">Nombre</th>
                <th className="px-4 py-3 text-left">Email</th>
                <th className="px-4 py-3 text-left">Cumpleaños</th>
                <th className="px-4 py-3 text-left">Área</th>
                <th className="px-4 py-3 text-left">Antigüedad</th>
                <th className="px-4 py-3 text-left">Regalo</th>
                <th className="px-4 py-3 text-left">Avisa empresa</th>
                <th className="px-4 py-3 text-left">Estado</th>
                <th className="px-4 py-3 text-left">Acción</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {colabs.map(c => (
                <tr key={c.id} className={!c.activo ? 'bg-gray-50 opacity-60' : ''}>
                  <td className="px-4 py-3">
                    <div className="relative group w-10 h-10">
                      {c.foto
                        ? <img src={`/uploads/${c.foto}`} className="w-10 h-10 rounded-full object-cover border border-gray-200" alt={c.nombre} />
                        : <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-sm">{c.nombre[0].toUpperCase()}</div>}
                      <label className="absolute inset-0 rounded-full bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center cursor-pointer transition">
                        <Camera className="text-white" size={14} />
                        <input type="file" accept="image/jpeg,image/png,image/gif,image/webp" className="hidden"
                          onChange={e => e.target.files[0] && handleSubirFoto(c.id, e.target.files[0])} />
                      </label>
                    </div>
                  </td>
                  <td className="px-4 py-3 font-medium text-gray-800">{c.nombre}</td>
                  <td className="px-4 py-3 text-gray-600">{c.email}</td>
                  <td className="px-4 py-3 text-gray-600">{c.fec_nac}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{c.area || '—'}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{calcAntigüedad(c.fec_ingreso)}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${REGALO_STYLE[c.regalo_pref] || 'bg-gray-100 text-gray-600'}`}>
                      {REGALO_LABEL[c.regalo_pref] || c.regalo_pref}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    {c.avisar_empresa ? <span className="text-green-600 font-medium text-xs">Sí</span> : <span className="text-gray-400 text-xs">No</span>}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${c.activo ? 'bg-green-100 text-green-700' : 'bg-gray-200 text-gray-500'}`}>
                      {c.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {c.activo
                      ? <button onClick={() => handleInactivar(c.id, c.nombre)} className="text-xs text-red-500 hover:underline font-medium">Deshabilitar</button>
                      : <span className="text-xs text-gray-300">—</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
