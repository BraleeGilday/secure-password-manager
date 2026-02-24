import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

import { listCredentials } from "../api/credentials";
import CredentialRow from "../components/CredentialRow";

export default function VaultOverviewPage({ onLogout }) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [credentials, setCredentials] = useState([]);
  const searchTerm = (searchParams.get("search") || "").trim();

  const fetchCredentialsSearch = useCallback(
    async (term) => {
      const response = await listCredentials(term);

      if (response.status === 401) {
        onLogout?.();
        navigate("/login", { replace: true });
        return;
      }

      if (response.status !== 200) {
        setCredentials([]);
        return;
      }

      setCredentials(Array.isArray(response.data) ? response.data : []);
    },
    [onLogout, navigate]
  );

  useEffect(() => {
    fetchCredentialsSearch(searchTerm);
  }, [fetchCredentialsSearch, searchTerm]);

  return (
    <div className="vault-page">
      <div className="page-banner">
        <h2>Credential Vault Overview</h2>
      </div>

      <div className="vault-layout">
        <aside className="card">
          <h3>Vault Options</h3>
          <Link className="btn" to="/credentials/new">
            Add Credential
          </Link>
        </aside>

        <section className="vault-content">
          <div className="card">
            <p style={{ marginTop: 0 }}>
              Use the search bar above to search credentials by site.
            </p>
            {searchTerm ? (
              <p style={{ marginBottom: 0 }}>
                Showing results for: <strong>{searchTerm}</strong>
              </p>
            ) : (
              <p style={{ marginBottom: 0 }}>Showing all credentials.</p>
            )}
          </div>

          <div className="cred-list">
            {credentials.length === 0 ? (
              <p>No credentials found.</p>
            ) : (
              credentials.map((c) => (
                <CredentialRow key={c.id} id={c.id} site={c.site} />
              ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}