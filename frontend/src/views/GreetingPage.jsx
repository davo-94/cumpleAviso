import { useState } from 'react';
import { Send, CheckCircle, ArrowLeft, Gift } from 'lucide-react';

const THEMES = {
  cine: {
    bg:     'bg-slate-900',
    text:   'text-cyan-400',
    card:   'bg-slate-800 border-cyan-500',
    btn:    'bg-cyan-500 hover:bg-cyan-600',
    msgBg:  'bg-cyan-900/30',
    icon:   '🎬',
  },
  spa: {
    bg:     'bg-green-50',
    text:   'text-green-800',
    card:   'bg-white border-green-300',
    btn:    'bg-green-600 hover:bg-green-700',
    msgBg:  'bg-green-100',
    icon:   '🌿',
  },
  libro: {
    bg:     'bg-amber-50',
    text:   'text-amber-900',
    card:   'bg-white border-amber-300',
    btn:    'bg-amber-600 hover:bg-amber-700',
    msgBg:  'bg-amber-100',
    icon:   '📚',
  },
};

const REGALO_LABEL = {
  cine:  '🎬 Entrada de Cine 2D',
  spa:   '🌿 Voucher Spa (1h)',
  libro: '📚 Libro (a elección)',
};

export default function GreetingPage({ colab, onBack }) {
  const theme = THEMES[colab?.regalo_pref] || THEMES.spa;
  const [message, setMessage] = useState('');
  const [sent, setSent] = useState(false);

  return (
    <div className={`min-h-screen ${theme.bg} p-8 flex flex-col items-center justify-center font-sans`}>
      <div className={`max-w-2xl w-full p-8 rounded-2xl shadow-2xl border-t-4 ${theme.card}`}>
        <div className="text-center">
          <div className="text-6xl mb-4">{theme.icon}</div>
          <h1 className={`text-4xl font-black mb-2 ${theme.text}`}>
            ¡Feliz Cumpleaños, {colab?.nombre}!
          </h1>
          <p className={`text-lg opacity-80 mb-6 ${theme.text}`}>
            Hoy es un día especial y todo el equipo lo sabe.
          </p>

          <div className={`mb-6 p-4 rounded-xl ${theme.msgBg} text-center`}>
            <Gift className={`mx-auto mb-2 ${theme.text}`} size={32} />
            <p className={`text-sm font-medium ${theme.text}`}>Tu regalo de parte de la empresa:</p>
            <p className={`font-bold text-base ${theme.text}`}>
              {REGALO_LABEL[colab?.regalo_pref] || colab?.regalo_pref}
            </p>
          </div>

          {!sent ? (
            <div className={`text-left ${theme.msgBg} p-6 rounded-xl`}>
              <label className={`block font-bold mb-2 text-sm ${theme.text}`}>
                Déjale un mensaje a tu compañero:
              </label>
              <textarea
                className="w-full p-3 rounded-lg text-gray-800 bg-white shadow-inner mb-4 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-sm"
                rows="4"
                placeholder="Escribe tus felicitaciones aquí..."
                value={message}
                onChange={e => setMessage(e.target.value)}
              />
              <button
                onClick={() => setSent(true)}
                className={`w-full ${theme.btn} text-white font-bold py-3 rounded-lg transition flex items-center justify-center gap-2`}
              >
                Enviar saludo <Send size={18} />
              </button>
            </div>
          ) : (
            <div className="bg-green-100 text-green-800 p-6 rounded-xl border border-green-200">
              <CheckCircle className="mx-auto mb-2" size={48} />
              <h3 className="text-2xl font-bold">¡Mensaje enviado!</h3>
              <p className="text-sm mt-1">Tu saludo fue añadido al mural virtual de {colab?.nombre}.</p>
            </div>
          )}
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200/20 flex justify-center">
          <button onClick={onBack} className={`text-sm underline opacity-60 hover:opacity-100 ${theme.text} flex items-center gap-1`}>
            <ArrowLeft size={14} /> Volver al panel de administración
          </button>
        </div>
      </div>
    </div>
  );
}
