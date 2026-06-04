import { useState } from 'react';
import { PartyPopper, Send, UserPlus, Users, Mail, Activity, Eye } from 'lucide-react';
import RegisterForm from './views/RegisterForm.jsx';
import ColaboradoresList from './views/ColaboradoresList.jsx';
import EnviosHistorial from './views/EnviosHistorial.jsx';
import JobLogs from './views/JobLogs.jsx';
import EmailPreview from './views/EmailPreview.jsx';
import GreetingPage from './views/GreetingPage.jsx';
import { api } from './api.js';

const TABS = [
  { id: 'registrar',     label: 'Registrar',          icon: UserPlus, border: 'border-blue-500'   },
  { id: 'colaboradores', label: 'Colaboradores',       icon: Users,    border: 'border-indigo-500' },
  { id: 'envios',        label: 'Historial de envíos', icon: Mail,     border: 'border-green-500'  },
  { id: 'logs',          label: 'Logs del job',        icon: Activity, border: 'border-orange-500' },
  { id: 'correo',        label: 'Vista correo',        icon: Eye,      border: 'border-purple-500' },
];

export default function App() {
  const [view, setView] = useState('admin');
  const [activeTab, setActiveTab] = useState('registrar');
  const [toast, setToast] = useState(null);
  const [greetingColab, setGreetingColab] = useState(null);

  function showToast(msg, ok = true) {
    setToast({ msg, ok });
    setTimeout(() => setToast(null), 3500);
  }

  async function handleEjecutarJob() {
    try {
      await api.ejecutarJob();
      showToast('Job ejecutado. Revisa la pestaña Logs.');
    } catch (err) {
      showToast(err.message, false);
    }
  }

  function openGreeting(colab) {
    setGreetingColab(colab);
    setView('greeting');
  }

  if (view === 'greeting') {
    return <GreetingPage colab={greetingColab} onBack={() => setView('admin')} />;
  }

  return (
    <div className="min-h-screen bg-gray-100 font-sans">
      {toast && (
        <div className="fixed top-4 right-4 z-50">
          <div className={`px-5 py-3 rounded-lg shadow-lg text-white text-sm font-medium transition-all ${toast.ok ? 'bg-green-600' : 'bg-red-600'}`}>
            {toast.msg}
          </div>
        </div>
      )}

      <nav className="bg-indigo-600 text-white px-6 py-4 shadow-md">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl">
            <PartyPopper size={24} />
            <span>CumpleAviso</span>
          </div>
          <button
            onClick={handleEjecutarJob}
            className="bg-white text-indigo-700 text-sm font-semibold px-4 py-2 rounded-lg hover:bg-indigo-50 transition flex items-center gap-2"
          >
            <Send size={15} /> Ejecutar job ahora
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
          {TABS.map(({ id, label, icon: Icon, border }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`bg-white p-4 rounded-xl shadow-sm hover:shadow-md cursor-pointer transition border-t-4 text-left ${activeTab === id ? border + ' shadow-md' : 'border-transparent'}`}
            >
              <Icon className={`mb-2 ${activeTab === id ? 'text-indigo-600' : 'text-gray-400'}`} size={22} />
              <p className={`text-sm font-semibold ${activeTab === id ? 'text-gray-800' : 'text-gray-500'}`}>{label}</p>
            </button>
          ))}
        </div>

        {activeTab === 'registrar'     && <RegisterForm      showToast={showToast} />}
        {activeTab === 'colaboradores' && <ColaboradoresList  showToast={showToast} />}
        {activeTab === 'envios'        && <EnviosHistorial />}
        {activeTab === 'logs'          && <JobLogs />}
        {activeTab === 'correo'        && <EmailPreview showToast={showToast} onOpenGreeting={openGreeting} />}
      </main>
    </div>
  );
}
