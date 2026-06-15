import React, { useState } from "react";
import "./SignupPage.css";
import logo from "../assets/cosmo_logo.png";
import { Link, useNavigate } from "react-router-dom";
import useDocumentTitle from "../hooks/useDocumentTitle";
import { useAuth } from "../contexts/AuthContext";
import { ApiError } from "../services/api";

const SignupPage: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [retypePassword, setRetypePassword] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  useDocumentTitle("Cosmo Drone - Sign up");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== retypePassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);
    try {
      await register(username, email, password);
      navigate("/");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message ?? "Registration failed.");
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

        <p className="subtitle">Sign up</p>

        <input
          type="email"
          placeholder="Email"
          className="input"
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
          }
        />

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
            className="eye"
            onClick={() => setShowPassword((prev) => !prev)}
          >
            👁
          </span>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Retype Password"
            className="input"
            value={retypePassword}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setRetypePassword(e.target.value)
            }
          />
        </div>

        {error && <p style={{ color: "var(--error, #ef4444)", fontSize: "0.85rem", textAlign: "center" }}>{error}</p>}

        <div className="buttons">
          <Link to="/login" className="btn sign-in">
            Sign in
          </Link>
          <button type="submit" className="btn submit" disabled={loading}>
            {loading ? "Creating account…" : "Submit"}
          </button>
        </div>
      </form>

      <p className="footer">Cosmo PK all rights reserved ©</p>
    </div>
  );
};

export default SignupPage;


