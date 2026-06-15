import React, { useState } from "react";
import "./LoginPage.css";
import logo from "../assets/cosmo_logo.png";
import { Link, useNavigate, useLocation } from "react-router-dom";
import useDocumentTitle from "../hooks/useDocumentTitle";
import { useAuth } from "../contexts/AuthContext";
import { ApiError } from "../services/api";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useDocumentTitle("Cosmo Drone - Log in");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname ?? "/";
      navigate(from, { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.status === 401 ? "Invalid username or password." : err.message);
      } else {
        setError("Connection error – is the backend running?");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-container">
      <form className="card" onSubmit={handleSubmit}>
        <img src={logo} alt="Cosmo logo" className="logo" />

        <h1 className="title">
          Cosmo Drone Panel
        </h1>

        <p className="subtitle">Log in</p>

        <input
          type="text"
          placeholder="Username"
          className="input"
          value={username}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setUsername(e.target.value)
          }
        />

        <div className="password-wrapper">
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            className="input"
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setPassword(e.target.value)
            }
          />
          <span
            className="eye-2"
            onClick={() => setShowPassword((prev) => !prev)}
          >
            👁
          </span>
        </div>

        {error && <p className="error-message" style={{ color: "var(--error, #ef4444)", fontSize: "0.85rem", textAlign: "center" }}>{error}</p>}

        <div className="password-restore-text">
          <Link to="/password-restore" className="password-restore-text">
            <h3> Forget password, no problem click here for restore </h3>
          </Link>
        </div>

        <div className="buttons">
          <Link to="/signup" className="btn sign-in">
            Sign up
          </Link>
          <button type="submit" className="btn submit" disabled={loading}>
            {loading ? "Logging in…" : "Submit"}
          </button>
        </div>
      </form>

      <p className="footer">Cosmo PK all rights reserved ©</p>
    </div>
  );
};

export default LoginPage;
