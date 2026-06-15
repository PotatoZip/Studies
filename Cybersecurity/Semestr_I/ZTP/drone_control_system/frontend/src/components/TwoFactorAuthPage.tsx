import "./SignupPage.css";
import "./TwoFactorAuthPage.css";
import logo from "../assets/cosmo_logo.png";
import { useNavigate } from "react-router-dom";
import useDocumentTitle from "../hooks/useDocumentTitle";
import { useRef, useState } from "react";


const CODE_LENGTH = 6;

const TwoFactorAuthPage = () => {
  const [code, setCode] = useState<string[]>(Array(CODE_LENGTH).fill(""));
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  const navigate = useNavigate();

  useDocumentTitle("Cosmo Drone - 2FA Login");

  const handleChange = (value: string, index: number) => {
    if (!/^[0-9]?$/.test(value)) return;

    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    // move forward
    if (value && index < CODE_LENGTH - 1) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

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

        <p className="subtitle-2fa">
          Enter the 2FA Code
        </p>

        <div className="code-inputs">
          {code.map((digit, index) => (
            <div key={index} className="input-wrapper">
              <input
                ref={(el) => (inputsRef.current[index] = el)}
                type="text"
                maxLength={1}
                value={digit}
                onChange={(e) => handleChange(e.target.value, index)}
                onKeyDown={(e) => handleKeyDown(e, index)}
                className="digit-input"
              />

              {/* dash in middle */}
              {index === 2 && <span className="dash">-</span>}
            </div>
          ))}
        </div>
        
        <div className="button-row">
          <button className="btn-2fa submit">Submit</button>
        </div>
        

      </form>
      <p className="footer">Cosmo PK all rights reserved ©</p>
    </div>
  );
};

export default TwoFactorAuthPage;



