import "./SignupPage.css";
import "./PasswordRestorePage.css";
import logo from "../assets/cosmo_logo.png";
import { useNavigate } from "react-router-dom";
import useDocumentTitle from "../hooks/useDocumentTitle";


const TwoFactorAuthSetupPage = () => {
  const navigate = useNavigate();

  useDocumentTitle("Cosmo Drone - 2FA Setup");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/dashboard");

  };


  return (
    <div className="signup-container">
      <form className="card" onSubmit={handleSubmit}>
        <img src={logo} alt="Cosmo logo" className="logo" />

        <h1 className="title">
          Cosmo Drone Panel
        </h1>
        
        <p className="subtitle-password-restore">
          2FA Codes Setup
        </p>

        <p className="text-password-restore">
          Use authentication app to scan the QR code below
        </p>
    
        
        <div className="button-row">
          <button className="btn-2fa submit">
            Submit
          </button>
        </div>
        
      </form>
      <p className="footer">Cosmo PK all rights reserved ©</p>
    </div>
  );
};

export default TwoFactorAuthSetupPage;



