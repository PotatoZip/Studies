import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';

function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Nie udało się zalogować. Sprawdź e-mail i hasło.');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-grow justify-center items-center py-20 px-4">
      <Card className="w-full max-w-md p-8 border-outline-variant/20 shadow-xl">
        <div className="text-center mb-8">
          <span className="material-symbols-outlined text-primary text-5xl">login</span>
          <h1 className="text-3xl font-headline font-bold text-primary mt-2">Logowanie</h1>
          <p className="text-slate-500 mt-2">Zaloguj się, aby uzyskać dostęp do panelu administratora.</p>
        </div>
        {error && <div className="bg-error/10 text-error p-3 rounded-md mb-4 text-center">{error}</div>}
        <form onSubmit={handleLogin} className="space-y-4">
          <Input 
            label="E-mail" 
            type="email" 
            required 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input 
            label="Hasło" 
            type="password" 
            required 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" disabled={loading} className="w-full py-3 mt-2">
            {loading ? 'Logowanie...' : 'Zaloguj'}
          </Button>
        </form>
      </Card>
    </div>
  );
}

export default LoginPage;