import { useEffect, Suspense, lazy } from 'react';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import { trackPageView } from './analytics';
import { useAuth } from './context/AuthContext';

const HomePage = lazy(() => import('./pages/HomePage'));
const SendRequestPage = lazy(() => import('./pages/SendRequestPage'));
const GaleryPage = lazy(() => import('./pages/GaleryPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'));
const DashboardLayout = lazy(() => import('./pages/dashboard/DashboardLayout'));
const OverviewPage = lazy(() => import('./pages/dashboard/OverviewPage'));
const SettingsPage = lazy(() => import('./pages/dashboard/SettingsPage'));

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

const PageLoader = () => (
  <div className="flex-grow flex items-center justify-center min-h-[50vh]">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
  </div>
);

function App() {
  const location = useLocation();

  useEffect(() => {
    trackPageView(`${location.pathname}${location.search}${location.hash}`);
  }, [location.pathname, location.search, location.hash]);
  
  return (
    <div className="app-shell flex flex-col min-h-screen">
      <Navbar />

      <main className="page-main flex-grow bg-background pt-16 flex flex-col">
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/send-request" element={<SendRequestPage />} />
            <Route path="/galery" element={<GaleryPage />} />
            <Route path="/login" element={<LoginPage />} />

            <Route path="/dashboard" element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }>
              <Route index element={<OverviewPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>

            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </main>

      <Footer />
    </div>
  );
}

export default App;
