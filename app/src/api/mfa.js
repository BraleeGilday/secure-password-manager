import api from "./client";

// Helper function (same style as user.js)
function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  return { Authorization: `Bearer ${token}` };
}

// GET /spm/mfa/totp/status
export async function fetchTotpStatus() {
  const response = await api.get("/spm/mfa/totp/status", {
    headers: getAuthHeaders(),
  });
  return response.data; // e.g. { totp_enabled: boolean, ... }
}

// POST /spm/mfa/totp/setup
export async function setupTotp() {
  const response = await api.post(
    "/spm/mfa/totp/setup",
    null,
    { headers: getAuthHeaders() }
  );
  return response.data; // { issuer, account_name, otpauth_uri }
}

// POST /spm/mfa/totp/confirm
export async function confirmTotp(code) {
  const response = await api.post(
    "/spm/mfa/totp/confirm",
    { code },
    { headers: getAuthHeaders() }
  );
  return response.data;
}

export async function fetchEnrollmentStatus(mfaToken) {
  const res = await api.post("/spm/mfa/totp/enrollment-status", { mfa_token: mfaToken });
  return res.data; // { totp_enabled, has_secret }
}