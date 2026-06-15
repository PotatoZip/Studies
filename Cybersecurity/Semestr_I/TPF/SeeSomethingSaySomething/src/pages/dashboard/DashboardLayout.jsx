import { Navigate, Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function DashboardLayout() {
  const { isAuthenticated, logout } = useAuth();

  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex flex-col md:flex-row min-h-[60vh] w-full max-w-[1440px] mx-auto bg-white rounded-2xl shadow-sm border border-slate-200 mt-8 mb-12 overflow-hidden">
      
      <aside className="w-full md:w-64 bg-slate-50 border-r border-slate-200 p-6 flex flex-col">
        <h2 className="text-lg font-headline font-bold text-primary mb-6">Panel Użytkownika</h2>
        <nav className="flex flex-col gap-2 flex-grow">
          <NavLink 
            to="/dashboard" 
            end
            className={({ isActive }) => `px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            Przegląd
          </NavLink>
          <NavLink 
            to="/dashboard/settings" 
            className={({ isActive }) => `px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-primary/10 text-primary' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            Ustawienia
          </NavLink>
        </nav>
        <button 
          onClick={logout}
          className="mt-8 flex items-center justify-center gap-2 px-4 py-2 text-red-600 font-bold hover:bg-red-50 rounded-lg transition-colors border border-transparent hover:border-red-100"
        >
          <span className="material-symbols-outlined text-sm">logout</span>
          Wyloguj
        </button>
      </aside>

      
      <div className="flex-grow p-6 lg:p-10">
        <Outlet />
      </div>
    </div>
  );
}

export default DashboardLayout;