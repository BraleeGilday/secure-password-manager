import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { deleteCredential, fetchCredentialById } from "../api/credentials";

export default function CredentialEntryPage({ onLogout }) {
  const navigate = useNavigate();
  const { id } = useParams();

  const [site, setSite] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [notes, setNotes] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    async function fetchCredential() {
      const response = await fetchCredentialById(id);

      if (response.status === 401) {
        onLogout?.();
        navigate("/login", { replace: true });
        return;
      }

      if (response.status !== 200) {
        return;
      }

      const data = response.data;
      setSite((data && data.site) || "");
      setUsername((data && data.username) || "");
      setPassword((data && data.password) || "");
      setNotes((data && data.notes) || "");
    }

    fetchCredential();
  }, [id, navigate, onLogout]);

  const handleDelete = async () => {
    const ok = window.confirm(
      `Delete credential "${site}" (${username})? This cannot be undone.`
    );
    if (!ok) return;

    const response = await deleteCredential(id);

    if (response.status === 401) {
      onLogout?.();
      navigate("/login", { replace: true });
      return;
    }

    if (response.status === 200 || response.status === 204) {
      navigate("/credentials");
    }
  };

  return (
    <div className="vault-page">
      <div className="page-banner">
        <h2>View Credential</h2>
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
            <div className="card-header">
              <h3>Review Current Details</h3>
              <div className="card-actions">
                <button
                  className="btn"
                  type="button"
                  onClick={() => navigate(`/credentials/${id}/edit`)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-delete"
                  type="button"
                  onClick={handleDelete}
                >
                  Delete
                </button>
              </div>
            </div>

            <div>
              <label className="field">
                <span>Site</span>
                <input value={site} readOnly disabled tabIndex={-1} />
              </label>

              <label className="field">
                <span>Username</span>
                <input value={username} readOnly disabled tabIndex={-1} />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-row">
                  <input
                    value={password}
                    type={showPassword ? "text" : "password"}
                    readOnly
                    disabled
                    tabIndex={-1}
                  />
                  <button
                    className="btn"
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </label>

              <label className="field">
                <span>Notes</span>
                <div
                  className={`notes-block ${notes?.trim() ? "" : "notes-empty"}`}
                >
                  {notes?.trim() ? notes : "No notes are present."}
                </div>
              </label>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}