import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { QRCodeSVG } from "qrcode.react";

import { fetchTotpStatus, setupTotp, confirmTotp } from "../api/mfa";

import api from "../api/client";
import ErrorText from "../components/ErrorText";
import FormLink from "../components/FormLink";

function MfaSettingsPage() {
  const navigate = useNavigate();

  const [status, setStatus] = useState("loading"); // loading | disabled | enabled | pending
  const [qrUri, setQrUri] = useState(null);
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  // Load MFA status
    useEffect(() => {
    const load = async () => {
        try {
        const data = await fetchTotpStatus();
        setStatus(data);
        } catch (err) {
        // handle 401 the same way as UserProfilePage if you want
        }
    };
    load();
    }, []);

    const handleSetup = async () => {
    const data = await setupTotp();
    setQrUri(data.otpauth_uri);
    };

    const handleConfirm = async () => {
    await confirmTotp(code);
    // refresh status, show success, etc.
    };

  return (
    <div className="form-container">
      <h1 className="form-title">Two-Factor Authentication</h1>

      {status === "loading" && <p>Loading…</p>}

      {status === "disabled" && (
        <>
          <p>MFA is currently <b>disabled</b>.</p>
          <button type="button" onClick={handleSetup}>
            Enable MFA
          </button>
        </>
      )}

      {status === "pending" && (
        <>
          <p>Scan this QR code with Duo Mobile, then enter the 6-digit code.</p>

          {qrUri && (
            <div style={{ margin: "16px 0" }}>
              <QRCodeSVG value={qrUri} />
            </div>
          )}

          <form onSubmit={handleConfirm}>
            <label>6-digit code</label>
            <input
              inputMode="numeric"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="123456"
              required
            />
            <button type="submit">Confirm</button>
          </form>
        </>
      )}

      {status === "enabled" && (
        <>
          <p>MFA is currently <b>enabled</b> ✅</p>
          {/* optional later: disable flow */}
        </>
      )}

      <ErrorText>{error}</ErrorText>

      <FormLink to="/profile">Back to Profile</FormLink>
    </div>
  );
}

export default MfaSettingsPage;