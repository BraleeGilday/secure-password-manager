import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import QRCode from "react-qr-code";
import api from "../api/client";
import ErrorText from "../components/ErrorText";
import FormLink from "../components/FormLink";

function MfaSetupPage({ setIsLoggedIn }) {
  const navigate = useNavigate();
  const location = useLocation();

  const [mfaToken] = useState(
    location.state?.mfaToken || sessionStorage.getItem("mfa_token") || ""
  );

  const [qrUri, setQrUri] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loadingSetup, setLoadingSetup] = useState(false);
  const [loadingConfirm, setLoadingConfirm] = useState(false);

  // Persist token if we got it via navigation
  useEffect(() => {
    if (location.state?.mfaToken) {
      sessionStorage.setItem("mfa_token", location.state.mfaToken);
    }
  }, [location.state]);

  // Auto-generate QR when page loads
  useEffect(() => {
    const run = async () => {
      setError("");

      if (!mfaToken) {
        setError("Missing MFA token. Please log in again.");
        return;
      }

      setLoadingSetup(true);
      try {
        const res = await api.post("/spm/mfa/totp/setup", { mfa_token: mfaToken });
        setQrUri(res.data.otpauth_uri);
      } catch (err) {
        setError(err?.response?.data?.detail || "Could not start MFA setup.");
      } finally {
        setLoadingSetup(false);
      }
    };

    run();
  }, [mfaToken]);

  const handleConfirm = async (e) => {
    e.preventDefault();
    setError("");

    if (!mfaToken) {
      setError("Missing MFA token. Please log in again.");
      return;
    }

    setLoadingConfirm(true);

    try {
      const complete = await api.post("/spm/mfa/totp/complete", {
        mfa_token: mfaToken,
        code,
      });

      localStorage.setItem("access_token", complete.data.access_token);
      sessionStorage.removeItem("mfa_token");
      setIsLoggedIn?.(true);

      navigate("/credentials");
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid code. Try again.");
    } finally {
      setLoadingConfirm(false);
    }
  };

  return (
    <div className="form-container mfa-card">
      <h1 className="form-title mfa-title">Set up Two-Factor Authentication</h1>

      <p className="mfa-description">
        Scan QR code using an authenticator app, then enter the 6-digit code.
      </p>

      {loadingSetup && <p>Generating QR code…</p>}

      {qrUri && (
        <div className="qr-container">
          <div className="qr-box">
            <QRCode value={qrUri} />
          </div>
        </div>
      )}

      <form onSubmit={handleConfirm} className="mfa-form">
        <label className="mfa-label">6-digit code</label>

        <input
          className="mfa-code-input"
          inputMode="numeric"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="123456"
          required
        />

        <button type="submit" className="mfa-btn" disabled={loadingConfirm}>
          {loadingConfirm ? "Verifying..." : "Confirm"}
        </button>
      </form>

      <ErrorText>{error}</ErrorText>

      <FormLink to="/login">Back to Login</FormLink>
    </div>
  );
}

export default MfaSetupPage;