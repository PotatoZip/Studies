import { Link } from 'react-router-dom';

function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 py-20 animate-fade-in">
      <div className="relative">
        <span className="material-symbols-outlined text-[150px] text-slate-200 drop-shadow-sm select-none">sentiment_dissatisfied</span>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-9xl font-black text-slate-800/10 tracking-tighter mix-blend-overlay">
          404
        </div>
      </div>
      
      <h1 className="mt-8 text-4xl md:text-5xl font-headline font-extrabold text-slate-800 tracking-tight">Ups! Zgubiliśmy się...</h1>
      <p className="mt-4 text-slate-600 max-w-md text-lg leading-relaxed">
        Strona, której szukasz mogła zostać usunięta, zmieniła swój adres lub po prostu nigdy nie istniała.
      </p>
      
      <div className="mt-10 flex gap-4">
        <Link
          to="/"
          className="bg-primary text-on-primary px-8 py-3 rounded-full font-bold shadow-md hover:shadow-lg hover:bg-primary/90 hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
        >
          <span className="material-symbols-outlined">home</span>
          Wróć na stronę główną
        </Link>
      </div>
    </div>
  );
}

export default NotFoundPage;