import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/client";
import ErrorText from "../components/ErrorText";

function MfaVerifyPage({ setIsLoggedIn }) {
  const navigate = useNavigate();
  const location = useLocation();

  // Prefer navigation state, fall back to sessionStorage
  const [mfaToken] = useState(
    location.state?.mfaToken || sessionStorage.getItem("mfa_token") || ""
  );
  const email = location.state?.email;

  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  // If we truly have no token, send them back
  useEffect(() => {
    if (!mfaToken) {
      setError("Missing MFA token. Please log in again.");
    }
  }, [mfaToken]);

  const handleVerify = async (e) => {
    e.preventDefault();
    setError("");

    if (!mfaToken) {
      setError("Missing MFA token. Please log in again.");
      return;
    }

    try {
      // For every-login challenge, use /totp/verify
      const response = await api.post("/spm/mfa/totp/verify", {
        mfa_token: mfaToken,
        code,
      });

      const data = response.data;

      localStorage.setItem("access_token", data.access_token);
      sessionStorage.removeItem("mfa_token");
      setIsLoggedIn?.(true);

      navigate("/credentials");
    } catch (err) {
      const detail = err?.response?.data?.detail;

      // If user isn't enrolled yet, send them to setup
      if (detail === "MFA not enrolled") {
        navigate("/mfa/setup", { state: { mfaToken, email } });
        return;
      }

      setError(detail || "MFA verification failed. Try again.");
    }
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Two-Factor Authentication</h1>
      <p>
        {email
          ? `Enter the 6-digit code from your authenticator for ${email}.`
          : "Enter your 6-digit code from your authenticator."}
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