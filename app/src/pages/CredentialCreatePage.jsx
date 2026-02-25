import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { createCredential } from "../api/credentials";

import PasswordGeneratorButton from "./pwd_gen/PasswordGeneratorButton";

export default function CredentialCreatePage({ onLogout }) {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    site: "",
    username: "",
    password: "",
    notes: "",
  });
  const [showPassword, setShowPassword] = useState(false);

  const updateField = (field) => (e) => {
    const value = e.target.value;
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  async function handleSubmit(e) {
    e.preventDefault();

    // Required fields check (site, username, password)
    if (
      !formData.site.trim() ||
      !formData.username.trim() ||
      !formData.password.trim()
    ) {
      window.alert(
        "Please enter a Site, Username, and Password to create a credential."
      );
      return;
    }

    const response = await createCredential(formData);

    if (response.status === 401) {
      onLogout?.();
      navigate("/login", { replace: true });
      return;
    }

    // Duplicate site and username combination check
    if (response.status === 409) {
      const msg =
        "A credential for this site and username combination already exists, use a different site or username.";
      window.alert(msg);
      return;
    }

    if (response.status === 200 || response.status === 201) {
      navigate("/credentials");
    }
  }

  return (
    <div className="vault-page">
      <div className="page-banner">
        <h2>Create Credential</h2>
      </div>

      <div className="vault-layout">
        <aside className="card">
          <h3>Navigation Options</h3>
          <Link className="btn" to="/credentials">
            Back to Vault Overview
          </Link>
        </aside>

        <section className="vault-content">
          <div className="card">
            <h3 style={{ marginTop: 0 }}>Add to Required Fields of Site, Username, and Password</h3>

            <form onSubmit={handleSubmit}>
              <label className="field">
                <span>Site</span>
                <input
                  value={formData.site}
                  onChange={updateField("site")}
                  placeholder="e.g., Google"
                />
              </label>

              <label className="field">
                <span>Username</span>
                <input
                  value={formData.username}
                  onChange={updateField("username")}
                  placeholder="e.g., user@example.com"
                />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-row">
                  <input
                    value={formData.password}
                    onChange={updateField("password")}
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter a password..."
                  />
                  <button
                    className="btn"
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>

                {/* Password generator modal/button */}
                <div className="pwd-gen-inline">
                  <PasswordGeneratorButton />
                </div>
              </label>

              <label className="field">
                <span>Notes</span>
                <textarea
                  className="notes-textarea"
                  value={formData.notes}
                  onChange={updateField("notes")}
                  rows={5}
                  placeholder="Optional notes..."
                />
              </label>

              <button className="btn" type="submit" style={{ marginTop: 12 }}>
                Create Credential
              </button>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
}