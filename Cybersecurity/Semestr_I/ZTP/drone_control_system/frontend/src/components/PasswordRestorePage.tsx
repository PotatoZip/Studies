import "./SignupPage.css";
import "./PasswordRestorePage.css";
import logo from "../assets/cosmo_logo.png";
import { Link, useNavigate } from "react-router-dom";
import useDocumentTitle from "../hooks/useDocumentTitle";
import { useState } from "react";


const PasswordRestorePage = () => {
  const [email, setEmail] = useState<string>("");
  const navigate = useNavigate();

  useDocumentTitle("Cosmo Drone - Password Restore");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/dashboard");

    console.log({
      email
    });
  };


  return (
    <div className="signup-container">
      <form className="card" onSubmit={handleSubmit}>
        <img src={logo} alt="Cosmo logo" className="logo" />

        <h1 className="title">
          Cosmo Drone Panel
        </h1>
        
        <p className="subtitle-password-restore">
          Password Restore
        </p>

        <p className="text-password-restore">
          Please enter your email used to created an account
        </p>

        <input
            type="email"
            placeholder="Email"
            className="input"
            value={email}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
            }
        />
    
        
        <div className="button-row">
          <Link to="/login" className="btn sign-in">
            Back to log in
          </Link>
          <button className="btn-2fa submit">
            Send
          </button>
        </div>
        
      </form>
      <p className="footer">Cosmo PK all rights reserved ©</p>
    </div>
  );
};

export default PasswordRestorePage;



