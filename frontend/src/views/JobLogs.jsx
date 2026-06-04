import { useState, useEffect } from 'react';
import { Activity, RefreshCw } from 'lucide-react';
import { api } from '../api.js';

function fmtFecha(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('es-CL', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export default function JobLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setLogs(await api.getLogs()); } catch { /* silencioso */ } finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden border-t-4 border-orange-500">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="text-orange-500" size={22} />
          <h2 className="text-lg font-bold text-gray-800">Logs de ejecución del job</h2>
        </div>
        <button onClick={load} className="text-sm text-indigo-600 hover:underline flex items-center gap-1">
          <RefreshCw size={14} /> Actualizar
        </button>
      </div>

      <div className="overflow-x-auto">
        {loading ? (
          <p className="text-center py-10 text-gray-400">Cargando...</p>
        ) : logs.length === 0 ? (
          <p className="text-center py-10 text-gray-400">Sin logs registrados</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 uppercase text-xs">
              <tr>
                <th className="px-4 py-3 text-left">Fecha</th>
                <th className="px-4 py-3 text-left">Resultado</th>
                <th className="px-4 py-3 text-left">Cumpleaños encontrados</th>
                <th className="px-4 py-3 text-left">Detalle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {logs.map(l => (
                <tr key={l.id}>
                  <td className="px-4 py-3 text-xs text-gray-500">{fmtFecha(l.fecha)}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${l.resultado === 'ok' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {l.resultado}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center text-gray-700">{l.cantidad_encontrados}</td>
                  <td className="px-4 py-3 text-gray-600 text-xs">{l.detalle || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
