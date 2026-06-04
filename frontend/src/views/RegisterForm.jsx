import { useState, useRef } from 'react';
import { UserPlus, Camera, CheckCircle, User } from 'lucide-react';
import { api } from '../api.js';

export default function RegisterForm({ token, showToast, onAuthError }) {
  const [fotoPreview, setFotoPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const fotoInputRef = useRef(null);

  function handleFotoChange(e) {
    const file = e.target.files[0];
    if (file) setFotoPreview(URL.createObjectURL(file));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    const form = e.target;
    try {
      const data = {
        nombre: form.nombre.value.trim(),
        email: form.email.value.trim(),
        fec_nac: form.fec_nac.value,
        regalo_pref: form.regalo_pref.value,
        avisar_empresa: form.avisar_empresa.checked,
        area: form.area.value.trim() || null,
        fec_ingreso: form.fec_ingreso.value || null,
      };
      const colab = await api.createColaborador(data, token);
      if (fotoInputRef.current?.files[0]) {
        await api.uploadFoto(colab.id, fotoInputRef.current.files[0], token);
      }
      showToast('Colaborador registrado correctamente');
      form.reset();
      setFotoPreview(null);
    } catch (err) {
      onAuthError(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-lg mx-auto bg-white rounded-xl shadow-md p-6 border-t-4 border-blue-500">
      <div className="flex items-center gap-3 mb-6">
        <UserPlus className="text-blue-500" size={28} />
        <div>
          <h2 className="text-xl font-bold text-gray-800">Nuevo colaborador</h2>
          <p className="text-gray-500 text-sm">Registra sus datos para activar saludos automáticos.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col items-center gap-2">
          <label className="cursor-pointer group relative">
            <div className="w-24 h-24 rounded-full bg-gray-100 border-2 border-dashed border-gray-300 flex items-center justify-center overflow-hidden group-hover:border-indigo-400 transition">
              {fotoPreview
                ? <img src={fotoPreview} className="w-full h-full object-cover" alt="preview" />
                : <User className="text-gray-300" size={36} />}
            </div>
            <span className="absolute bottom-0 right-0 bg-indigo-600 rounded-full p-1.5 shadow group-hover:bg-indigo-700 transition">
              <Camera className="text-white" size={12} />
            </span>
            <input ref={fotoInputRef} name="foto" type="file" accept="image/jpeg,image/png,image/gif,image/webp" className="hidden" onChange={handleFotoChange} />
          </label>
          <span className="text-xs text-gray-400">Foto (opcional)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Nombre completo</label>
            <input name="nombre" required className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input name="email" type="email" required className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha de nacimiento</label>
            <input name="fec_nac" type="date" required className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fecha de ingreso <span className="text-gray-400 font-normal">(opcional)</span></label>
            <input name="fec_ingreso" type="date" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Área <span className="text-gray-400 font-normal">(opcional)</span></label>
            <input name="area" placeholder="Ej. Tecnología, Marketing…" className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Regalo preferido</label>
            <select name="regalo_pref" required className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="">Seleccionar...</option>
              <option value="cine">🎬 Cine (entrada 2D)</option>
              <option value="spa">🌿 Spa (voucher 1h)</option>
              <option value="libro">📚 Libro (a elección)</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <input name="avisar_empresa" type="checkbox" id="avisar" className="w-4 h-4 text-indigo-600 rounded" />
          <label htmlFor="avisar" className="text-sm text-gray-700">Autoriza aviso a la empresa el día de su cumpleaños</label>
        </div>

        <button type="submit" disabled={loading}
          className="w-full bg-indigo-600 text-white py-2.5 rounded-lg font-semibold hover:bg-indigo-700 transition flex items-center justify-center gap-2 disabled:opacity-60">
          <CheckCircle size={18} />
          {loading ? 'Registrando...' : 'Registrar colaborador'}
        </button>
      </form>
    </div>
  );
}
