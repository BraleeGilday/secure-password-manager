import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/client";
import ErrorText from "../components/ErrorText";

function MfaVerifyPage({ setIsLoggedIn }) {
  const navigate = useNavigate();
  const location = useLocation();

  const mfaToken = location.state?.mfaToken;
  const email = location.state?.email;

  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleVerify = async (e) => {
    e.preventDefault();
    setError("");

    if (!mfaToken) {
      setError("Missing MFA token. Please log in again.");
      return;
    }

    try {
      const response = await api.post("/spm/mfa/totp/complete", {
        mfa_token: mfaToken,
        code,
      });

      const data = response.data;

      localStorage.setItem("access_token", data.access_token);
      setIsLoggedIn(true);
      navigate("/credentials");
    } catch (err) {
      const msg =
        err?.response?.data?.detail || "MFA verification failed. Try again.";
      setError(msg);
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Two-Factor Authentication</h1>
      <p>
        {email ? `Enter the 6-digit code from Duo for ${email}.` : "Enter your 6-digit code from Duo."}
      </p>

      <form onSubmit={handleVerify}>
        <label>6-digit code</label>
        <input
          inputMode="numeric"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="123456"
          required
        />
        <button type="submit">Verify</button>
      </form>

      <ErrorText>{error}</ErrorText>
    </div>
  );
}

export default MfaVerifyPage;