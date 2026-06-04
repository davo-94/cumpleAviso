import { useState, useEffect } from 'react';
import { Mail, RefreshCw } from 'lucide-react';
import { api } from '../api.js';

function fmtFecha(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('es-CL', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export default function EnviosHistorial({ token, onAuthError }) {
  const [envios, setEnvios] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setEnvios(await api.getEnvios(token)); }
    catch (err) { onAuthError(err); }
    finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border-t-4 border-green-500">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Mail className="text-green-500" size={22} />
          <h2 className="text-lg font-bold text-gray-800">Historial de envíos (últimos 50)</h2>
        </div>
        <button onClick={load} className="text-sm text-indigo-600 hover:underline flex items-center gap-1">
          <RefreshCw size={14} /> Actualizar
        </button>
      </div>

      <div className="overflow-x-auto">
        {loading ? (
          <p className="text-center py-10 text-gray-400">Cargando...</p>
        ) : envios.length === 0 ? (
          <p className="text-center py-10 text-gray-400">Sin envíos registrados</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
              <tr>
                <th className="px-4 py-3 text-left">Colaborador</th>
                <th className="px-4 py-3 text-left">Email</th>
                <th className="px-4 py-3 text-left">Fecha</th>
                <th className="px-4 py-3 text-left">Código</th>
                <th className="px-4 py-3 text-left">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {envios.map(e => (
                <tr key={e.id}>
                  <td className="px-4 py-3 font-medium text-gray-800">{e.nombre_colab}</td>
                  <td className="px-4 py-3 text-gray-600">{e.email_colab}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{fmtFecha(e.fecha)}</td>
                  <td className="px-4 py-3 font-mono text-xs text-gray-600 bg-gray-50">{e.codigo}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${e.estado_envio === 'enviado' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {e.estado_envio}
                    </span>
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
