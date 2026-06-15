function OverviewPage() {
  return (
    <div className="animate-fade-in">
      <h1 className="text-3xl font-headline font-bold text-primary mb-6">Przegląd</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div className="p-6 bg-blue-50 rounded-2xl border border-blue-100 shadow-sm">
          <p className="text-blue-600 text-sm font-bold uppercase tracking-wider mb-2">Aktywne Zgłoszenia</p>
          <p className="text-4xl font-headline font-black text-blue-900">3</p>
        </div>
        <div className="p-6 bg-green-50 rounded-2xl border border-green-100 shadow-sm">
          <p className="text-green-600 text-sm font-bold uppercase tracking-wider mb-2">Rozwiązane Problemy</p>
          <p className="text-4xl font-headline font-black text-green-900">12</p>
        </div>
      </div>
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4 text-on-surface">Ostatnia Aktywność</h2>
        <div className="bg-slate-50 p-4 rounded-xl text-slate-600 mb-2 border border-slate-200">
          Zgłoszenie #1023 (Dziura w jezdni) zostało przyjęte do ostatecznej weryfikacji.
        </div>
        <div className="bg-slate-50 p-4 rounded-xl text-slate-600 border border-slate-200">
          Zgłoszenie #984 (Niedziałająca latarnia) zmieniło status na: Rozwiązane.
        </div>
      </div>
    </div>
  );
}

export default OverviewPage;