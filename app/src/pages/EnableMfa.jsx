import { useState } from "react";
import api from "../api/client";
import QRCode from "qrcode.react";

function EnableMfa() {
  const [qrUri, setQrUri] = useState(null);

  const handleSetup = async () => {
    const response = await api.post("/spm/mfa/totp/setup");
    setQrUri(response.data.otpauth_uri);
  };

  return (
    <div>
      <button onClick={handleSetup}>Enable MFA</button>

      {qrUri && (
        <div>
          <p>Scan this with Duo:</p>
          <QRCode value={qrUri} />
        </div>
      )}
    </div>
  );
}

export default EnableMfa