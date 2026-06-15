import Button from '../components/ui/Button';

function SendRequestPage() {
  return (
    <div className="flex-grow pt-8 pb-20 px-6 mx-auto w-full max-w-5xl bg-background font-body text-on-surface">
      <header className="mb-12 text-center">
        <h1 className="text-3xl md:text-4xl font-extrabold font-headline text-on-surface tracking-tight mb-4">
          Nowe zgłoszenie
        </h1>
        <p className="text-on-surface-variant text-base mx-auto max-w-2xl">
          Pomóż nam dbać o okolicę. Wypełnij krótki formularz, aby poinformować odpowiednie służby o problemie.
        </p>
      </header>

      <form className="space-y-10" onSubmit={(e) => e.preventDefault()}>
        <section className="grid grid-cols-1 md:grid-cols-2 lg:gap-12 gap-8">
          <div className="space-y-2">
            <label className="block text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-2">
              Kategoria i Służba
            </label>
            <select className="custom-select w-full h-12 px-4 bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary transition-all text-sm" defaultValue="">
              <option disabled value="">
                Wybierz kategorię...
              </option>
              <option value="roads">Drogi (Zarząd Dróg Miejskich)</option>
              <option value="greenery">Zieleń (Zarząd Zieleni)</option>
              <option value="lighting">Oświetlenie (Zakład Energetyczny)</option>
              <option value="waste">Odpady (Zakład Oczyszczania Miasta)</option>
              <option value="other">Inne</option>
            </select>
            <p className="text-[11px] text-on-surface-variant/70 px-1">
              Automatycznie zasugerujemy odpowiedni departament.
            </p>
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-2">
              Priorytet zgłoszenia
            </label>
            <div className="grid grid-cols-3 gap-2">
              <label className="relative">
                <input className="peer sr-only" name="priority" type="radio" value="low" />
                <div className="text-center p-2 rounded-xl border border-outline-variant peer-checked:border-primary peer-checked:bg-primary/5 cursor-pointer transition-all">
                  <span className="block text-xs font-bold">Niski</span>
                  <span className="block text-[10px] text-on-surface-variant leading-tight mt-1">Drobna usterka</span>
                </div>
              </label>
              <label className="relative">
                <input className="peer sr-only" name="priority" type="radio" value="medium" defaultChecked />
                <div className="text-center p-2 rounded-xl border border-outline-variant peer-checked:border-primary peer-checked:bg-primary/5 cursor-pointer transition-all">
                  <span className="block text-xs font-bold">Średni</span>
                  <span className="block text-[10px] text-on-surface-variant leading-tight mt-1">Utrudnienie</span>
                </div>
              </label>
              <label className="relative">
                <input className="peer sr-only" name="priority" type="radio" value="high" />
                <div className="text-center p-2 rounded-xl border border-outline-variant peer-checked:border-error peer-checked:bg-error/5 cursor-pointer transition-all">
                  <span className="block text-xs font-bold peer-checked:text-error">Wysoki</span>
                  <span className="block text-[10px] text-on-surface-variant leading-tight mt-1">Zagrożenie</span>
                </div>
              </label>
            </div>
          </div>
        </section>

        <section className="space-y-2">
          <label className="block text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-2">
            Opis problemu
          </label>
          <textarea
            className="w-full min-h-[120px] bg-white border border-outline-variant rounded-xl focus:ring-2 focus:ring-primary focus:border-primary p-4 text-sm placeholder:text-on-surface-variant/40"
            placeholder="Opisz dokładnie, co i gdzie wymaga interwencji..."
          ></textarea>
        </section>

        <section className="space-y-2">
          <label className="block text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-4">
            Zdjęcia (maks. 3)
          </label>
          <div className="flex flex-wrap gap-4">
            <div className="relative w-28 h-28 rounded-xl overflow-hidden group border border-outline-variant">
              <img
                alt="Pothole preview"
                className="w-full h-full object-cover"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuD1iVMCNZg9R1C2EjQZj3UBbm0ZeCgEYzibt0Qqngk5l70aXxuOPaaHTKEeDSUb7y0NVJQIXT3PQpUBpd1HwgqYGqu0s1wgD1mGm_Lm15zekP0PeQjWIDbazCODRodMTVZxy_L6X1gEIqfkIRLP1lp-vtoTOW5WiMQ3CHW_0qEffCMXQqWUOgjRtkesmbF_dh7hkCFuR4eKyeuUmLhXCATG6dOC8trffbroZkKGkx2H9BYj62jsB2KtJQVJxhJl3Uj2zGCefhFKA5U"
              />
              <button
                className="absolute top-1 right-1 bg-error/90 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                type="button"
              >
                <span className="material-symbols-outlined text-xs leading-none">close</span>
              </button>
            </div>
            <button
              className="w-28 h-28 rounded-xl border-2 border-dashed border-outline-variant flex flex-col items-center justify-center hover:bg-surface-container-low hover:border-primary/40 transition-all text-on-surface-variant group"
              type="button"
            >
              <span className="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform">
                add_a_photo
              </span>
              <span className="text-[10px] font-bold mt-1">Dodaj zdjęcie</span>
            </button>
          </div>
        </section>

        <section className="space-y-2">
          <label className="block text-xs font-bold text-on-surface-variant uppercase tracking-widest mb-4">
            Lokalizacja
          </label>
          <div className="rounded-2xl overflow-hidden border border-outline-variant bg-white p-2">
            <div className="aspect-video md:aspect-[21/9] w-full rounded-xl overflow-hidden bg-slate-100 relative">
              <img
                className="w-full h-full object-cover grayscale opacity-60"
                data-alt="minimalist city map"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCV6fsVD4sZWGeZkp7iDFlOm4UrbCuSILIExNvZqSKb4J-09eXR4twQTP6m_4RxIaIoiCk07n_NV1RcSkJWUOw3SBMRHaEMOhQugqTnnECeojvLMKy8XzTX6V8wAMETtXb0qZUxUxtNneukRI6Fd0nibupJeREtLv58w9GR5pQWyovKQGu9QLcYnGeQBZmhieLtoYuCkQIsinG8-TjYfAEmyz3qzcsnAw413HGT97j8FO_yTFQ72SBJmv_4kuxiBrL49RoZC4Xskt0"
              />
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <span
                  className="material-symbols-outlined text-primary text-4xl drop-shadow-sm"
                  style={{ fontVariationSettings: '"FILL" 1' }}
                >
                  location_on
                </span>
              </div>
              <div className="absolute bottom-3 left-3 right-3 flex gap-2">
                <div className="flex-grow bg-white/95 backdrop-blur-sm px-3 py-2 rounded-lg text-xs font-semibold shadow-sm border border-outline-variant/20 truncate">
                  Marszałkowska 104, Warszawa
                </div>
                <button
                  className="bg-primary text-white p-2 rounded-lg shadow-sm hover:bg-primary-container transition-colors"
                  type="button"
                >
                  <span className="material-symbols-outlined text-sm">my_location</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        <div className="pt-6 border-t border-outline-variant/30 flex flex-col items-center">
          <Button
            type="submit"
            className="w-full md:w-auto md:min-w-[280px] h-14 px-8 text-base"
          >
            Wyślij zgłoszenie
            <span className="material-symbols-outlined text-lg">send</span>
          </Button>
          <p className="mt-4 text-[11px] text-on-surface-variant text-center">
            Przesyłając zgłoszenie akceptujesz regulamin partycypacji społecznej.
          </p>
        </div>
      </form>
    </div>
  );
}

export default SendRequestPage;
