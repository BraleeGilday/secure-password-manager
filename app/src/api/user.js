import api from "./client";

// Helper function
function getAuthHeaders() {
  const token = localStorage.getItem("access_token");
  return { Authorization: `Bearer ${token}` };
}

export async function fetchMyProfile() {
  const response = await api.get("/spm/user/me", {
    headers: getAuthHeaders(),
  })

  return response.data; // { id, email, display_name, created_at }
}

export async function updateMyProfile({ email, display_name }) {
const response = await api.put(
    "/spm/user/me", 
    {
      email,
      display_name: display_name?.trim() ? display_name.trim() : null,
    },
    {
      headers: getAuthHeaders(),
    }
)

  return response.data  // updated user object
}

export async function updateMyPassword({ current_password, new_password }) {
const response = await api.put(
    "/spm/user/me/password", 
    {
      current_password,
      new_password,
    },
    {
      headers: getAuthHeaders(),
    }
)

  return response.data  // Backend returns 204 No Content on success
}

export async function deleteMyAccount() {
const response = await api.delete(
    "/spm/user/me", 
    {headers: getAuthHeaders()}
)

  return response.data  // Backend returns 204 No Content on success
}

