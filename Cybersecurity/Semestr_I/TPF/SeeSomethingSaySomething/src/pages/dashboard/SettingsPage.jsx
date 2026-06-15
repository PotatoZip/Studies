function SettingsPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-3xl font-headline font-bold text-primary mb-6">Ustawienia</h1>
      <div className="max-w-xl space-y-6">
        <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
          <h2 className="text-lg font-bold text-on-surface mb-4">Powiadomienia E-mail</h2>
          <label className="flex items-center gap-3 cursor-pointer p-2 hover:bg-slate-100 rounded-lg transition-colors">
            <input type="checkbox" defaultChecked className="w-5 h-5 rounded text-primary focus:ring-primary" />
            <span className="text-slate-700">Otrzymuj alerty o ważnych zmianach statusów</span>
          </label>
            <label className="flex items-center gap-3 cursor-pointer p-2 hover:bg-slate-100 rounded-lg transition-colors mt-1">
            <input type="checkbox" className="w-5 h-5 rounded text-primary focus:ring-primary" />
            <span className="text-slate-700">Comiesięczny raport aktywności</span>
          </label>
        </div>

        <div className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
          <h2 className="text-lg font-bold text-on-surface mb-4">Zarządzanie Profilem</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-bold text-slate-600 mb-1">Nazwa wyświetlana</label>
              <input type="text" className="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all" defaultValue="Jan Kowalski (Admin)" />
            </div>
            <button className="bg-primary text-on-primary font-bold px-6 py-2.5 rounded-lg hover:opacity-90 transition-opacity">
              Zapisz modyfikacje
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SettingsPage;