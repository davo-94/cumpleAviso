import { useState, useEffect } from 'react';
import { Eye, Mail, Building2, Gift, ArrowRight } from 'lucide-react';
import { api } from '../api.js';

const REGALO_LABEL = {
  cine:  '🎬 Entrada de Cine 2D',
  spa:   '🌿 Voucher Spa (1h)',
  libro: '📚 Libro (a elección)',
};

const FAKE_CODE = 'GIFT-XXX-A1B2C3D4';

export default function EmailPreview({ showToast, onOpenGreeting }) {
  const [colabs, setColabs] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [activeEmail, setActiveEmail] = useState('empleado');

  useEffect(() => {
    api.getColaboradores()
      .then(data => setColabs(data.filter(c => c.activo)))
      .catch(err => showToast(err.message, false));
  }, []);

  const colab = colabs.find(c => c.id === selectedId);

  function handleSelect(e) {
    const id = Number(e.target.value) || null;
    setSelectedId(id);
    setActiveEmail('empleado');
  }

  return (
    <div className="bg-white rounded-xl shadow-md border-t-4 border-purple-500 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center gap-2">
        <Eye className="text-purple-500" size={22} />
        <h2 className="text-lg font-bold text-gray-800">Vista previa de correos</h2>
      </div>

      <div className="p-6">
        <div className="mb-6 max-w-sm">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Selecciona un colaborador para previsualizar
          </label>
          <select
            value={selectedId || ''}
            onChange={handleSelect}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="">— Elige un colaborador —</option>
            {colabs.map(c => (
              <option key={c.id} value={c.id}>{c.nombre} (nac. {c.fec_nac})</option>
            ))}
          </select>
        </div>

        {!colab ? (
          <div className="text-center py-16 text-gray-400">
            <Mail size={48} className="mx-auto mb-3 opacity-30" />
            <p>Selecciona un colaborador para ver cómo se vería su correo de cumpleaños.</p>
          </div>
        ) : (
          <div className="flex gap-6">
            <div className="w-56 flex-shrink-0 bg-gray-50 rounded-xl border border-gray-200 p-3 space-y-2">
              <div className="font-bold text-gray-700 text-sm mb-3 flex items-center gap-2">
                <Mail size={16} /> Bandeja de entrada
              </div>
              <button
                onClick={() => setActiveEmail('empleado')}
                className={`w-full text-left p-3 rounded-lg transition text-sm ${activeEmail === 'empleado' ? 'bg-purple-100 text-purple-800 font-medium border-l-4 border-purple-600' : 'hover:bg-gray-200 text-gray-700'}`}
              >
                <div className="truncate">Para: {colab.nombre}</div>
                <div className="text-xs text-gray-500 truncate">¡Feliz Cumpleaños! 🎉</div>
              </button>
              {colab.avisar_empresa && (
                <button
                  onClick={() => setActiveEmail('empresa')}
                  className={`w-full text-left p-3 rounded-lg transition text-sm ${activeEmail === 'empresa' ? 'bg-purple-100 text-purple-800 font-medium border-l-4 border-purple-600' : 'hover:bg-gray-200 text-gray-700'}`}
                >
                  <div>Para: RR.HH.</div>
                  <div className="text-xs text-gray-500 truncate">Cumpleaños de {colab.nombre}</div>
                </button>
              )}
              {!colab.avisar_empresa && (
                <p className="text-xs text-gray-400 px-2 italic">No hay aviso a la empresa (no autorizado)</p>
              )}
            </div>

            <div className="flex-1 bg-gray-50 rounded-xl p-6 min-w-0">
              {activeEmail === 'empleado' ? (
                <div className="bg-white rounded-xl border p-8 shadow-sm">
                  <div className="border-b pb-4 mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">¡Feliz Cumpleaños, {colab.nombre}! 🎂</h2>
                    <p className="text-gray-500 text-sm mt-1">De: Recursos Humanos &lt;rrhh@empresa.com&gt;</p>
                  </div>
                  <div className="space-y-4 text-gray-700 text-sm">
                    <p>Hola {colab.nombre},</p>
                    <p>¡Todo el equipo te desea un excelente día en tu cumpleaños! Esperamos que lo celebres a lo grande.</p>
                    <div className="my-6 p-5 bg-yellow-50 border border-yellow-200 rounded-xl text-center">
                      <Gift className="text-yellow-500 mx-auto mb-2" size={36} />
                      <h3 className="text-base font-bold text-yellow-800 mb-1">¡Tu regalo de cumpleaños!</h3>
                      <p className="text-yellow-700 text-sm mb-3">
                        Como regalo de parte de la empresa: <strong>{REGALO_LABEL[colab.regalo_pref] || colab.regalo_pref}</strong>
                      </p>
                      <div className="font-mono text-lg bg-yellow-100 px-4 py-2 rounded-lg inline-block border border-yellow-300 tracking-widest">
                        {FAKE_CODE}
                      </div>
                      <p className="text-xs text-yellow-600 mt-2">Presenta este código para canjear tu regalo</p>
                    </div>
                    <p>Gracias por ser parte de nuestro equipo.</p>
                    <p>Atentamente,<br /><strong>El Equipo de CumpleAviso</strong></p>
                  </div>
                  <div className="mt-8 pt-5 border-t flex justify-center">
                    <button
                      onClick={() => onOpenGreeting(colab)}
                      className="bg-indigo-600 text-white px-6 py-3 rounded-full font-bold hover:bg-indigo-700 shadow-md transition flex items-center gap-2"
                    >
                      Ver página de cumpleaños <ArrowRight size={18} />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="bg-white rounded-xl border p-8 shadow-sm">
                  <div className="border-b pb-4 mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">🎈 ¡Hoy es el cumpleaños de {colab.nombre}!</h2>
                    <p className="text-gray-500 text-sm mt-1">De: Sistema CumpleAviso &lt;sistema@cumpleaviso.com&gt;</p>
                    <p className="text-gray-500 text-sm">Para: rrhh@empresa.com</p>
                  </div>
                  <div className="space-y-4 text-gray-700 text-center">
                    <Building2 className="text-indigo-500 mx-auto" size={48} />
                    <p className="text-lg font-medium">¡Es momento de celebrar!</p>
                    <p className="text-sm">Hoy queremos avisar que <strong>{colab.nombre}</strong> cumple años.</p>
                    <div className="bg-indigo-50 p-4 rounded-xl text-sm max-w-sm mx-auto text-left space-y-1">
                      <p><strong>Email:</strong> {colab.email}</p>
                      <p><strong>Regalo enviado:</strong> {REGALO_LABEL[colab.regalo_pref] || colab.regalo_pref}</p>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">
                      Este aviso fue enviado porque el colaborador autorizó la notificación a la empresa.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
