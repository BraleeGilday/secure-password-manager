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
    const res = await api.post("/spm/user/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    // store token so you stay logged in
    localStorage.setItem("access_token", res.data.access_token);

    return res.data; // { access_token, token_type, username }
}
