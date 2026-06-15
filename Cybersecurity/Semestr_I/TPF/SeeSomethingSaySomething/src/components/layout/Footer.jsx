function Footer() {
  return (
    <footer className="w-full bg-slate-50 border-t border-slate-200 mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center py-12 px-6 lg:px-12 w-full max-w-[1440px] mx-auto gap-8">
        <div className="flex flex-col gap-4 items-center md:items-start">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-2xl">account_balance</span>
            <span className="text-lg font-bold text-blue-900 font-headline tracking-tight">
              See Something? Say Something!
            </span>
          </div>
          <p className="text-slate-500 text-sm font-body m-0">
            © 2024 Civic Integrity Portal. Wszystkie prawa zastrzeżone.
          </p>
        </div>
        <div className="flex flex-wrap justify-center gap-8">
          <a className="text-slate-500 hover:text-primary transition-colors text-sm font-body" href="#!">
            Prywatność
          </a>
          <a className="text-slate-500 hover:text-primary transition-colors text-sm font-body" href="#!">
            Regulamin
          </a>
          <a className="text-slate-500 hover:text-primary transition-colors text-sm font-body" href="#!">
            Pomoc
          </a>
        </div>
        <div className="flex gap-4">
          <a className="w-10 h-10 rounded-full bg-white border border-outline-variant flex items-center justify-center text-primary hover:bg-primary hover:text-on-primary transition-all" href="#!">
            <span className="material-symbols-outlined text-xl">language</span>
          </a>
          <a className="w-10 h-10 rounded-full bg-white border border-outline-variant flex items-center justify-center text-primary hover:bg-primary hover:text-on-primary transition-all" href="#!">
            <span className="material-symbols-outlined text-xl">share</span>
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;