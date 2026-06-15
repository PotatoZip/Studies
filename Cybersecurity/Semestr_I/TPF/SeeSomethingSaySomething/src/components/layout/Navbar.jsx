import { Link, NavLink, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();
  const isPanelActive = location.pathname.startsWith('/dashboard') || location.pathname === '/login';

  return (
    <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-xl shadow-sm border-b border-outline-variant/10 left-0 text-slate-800">
      <div className="flex justify-between items-center h-16 px-6 lg:px-12 w-full max-w-[1440px] mx-auto">
        <Link to="/" className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">account_balance</span>
          <span className="text-xl font-bold text-blue-900 font-headline tracking-tight hidden sm:block">
            See Something? Say Something!
          </span>
        </Link>
        <div className="hidden md:flex items-center gap-8">
          <NavLink 
            to="/" 
            end
            className={({ isActive }) => 
              `font-bold font-headline transition-colors ${isActive ? 'text-blue-900 border-b-2 border-blue-900 pb-1' : 'text-slate-600 hover:text-blue-800'}`
            }
          >
            Home
          </NavLink>
          <NavLink 
            to="/galery" 
            className={({ isActive }) => 
              `font-bold font-headline transition-colors ${isActive ? 'text-blue-900 border-b-2 border-blue-900 pb-1' : 'text-slate-600 hover:text-blue-800'}`
            }
          >
            Galeria zmian
          </NavLink>
          <Link 
            to="/dashboard" 
            className={`font-bold font-headline transition-colors ${isPanelActive ? 'text-blue-900 border-b-2 border-blue-900 pb-1' : 'text-slate-600 hover:text-blue-800'}`}
          >
            Panel
          </Link>
        </div>
        <Link
          to="/send-request"
          className="bg-primary text-on-primary px-6 py-2.5 rounded-full font-bold text-sm hover:opacity-90 hover:-translate-y-0.5 active:translate-y-0 focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-all shadow-sm flex items-center"
        >
          Zgłoś teraz
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;