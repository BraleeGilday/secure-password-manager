import api from "./client";

function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  return { Authorization: `Bearer ${token}` };
}

export async function listCredentials(searchTerm) {
  return api.get("/spm/credentials/", {
    params: searchTerm ? { search: searchTerm } : {},
    headers: getAuthHeaders(),
    validateStatus: () => true,
  });
}

export async function fetchCredentialById(id) {
  return api.get(`/spm/credentials/${id}`, {
    headers: getAuthHeaders(),
    validateStatus: () => true,
  });
}

export async function createCredential(payload) {
  return api.post("/spm/credentials/", payload, {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    validateStatus: () => true,
  });
}

export async function updateCredential(id, payload) {
  return api.patch(`/spm/credentials/${id}`, payload, {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    validateStatus: () => true,
  });
}

export async function deleteCredential(id) {
  return api.delete(`/spm/credentials/${id}`, {
    headers: getAuthHeaders(),
    validateStatus: () => true,
  });
}