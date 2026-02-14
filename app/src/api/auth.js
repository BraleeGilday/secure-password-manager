import api from "./client";

export async function loginUser(email, password) {
    /* 
    Translating what FastAPI backend expects into a request for Axios to send 
        FastAPI expects form data, not JSON
        Specifically looking for the fields: username (aka email), password
    
    */
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);

    // The Axios POST
    const response = await api.post("/spm/user/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    // store token so you stay logged in
    localStorage.setItem("access_token", response.data.access_token);

    return response.data; // { access_token, token_type, username }
}


export async function registerUser({ email, password, displayName }) {
  const payload = {
    email: email,
    password,
    display_name: displayName.trim() ? displayName.trim() : null,
  };

  const response = await api.post("/spm/user/register", payload);
  return response.data; // UserResponse: {id, email, display_name, created_at}
}