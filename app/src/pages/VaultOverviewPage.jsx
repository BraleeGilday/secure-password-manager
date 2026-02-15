import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

import CredentialRow from '../components/CredentialRow';

export default function VaultOverviewPage({ token, onLogout }) {
  const navigate = useNavigate();

  const [credentials, setCredentials] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchCredentials = useCallback(
    async (term) => {
      const query = term ? `?search=${encodeURIComponent(term)}` : '';

      const response = await axios.get(`/spm/credentials/${query}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        validateStatus: () => true,
      });

      if (response.status === 401) {
        onLogout();
        navigate('/', { state: { message: 'Session expired, paste a token again' } });
        return;
      }

      if (response.status !== 200) {
        setCredentials([]);
        return;
      }

      setCredentials(response.data);
    },
    [token, onLogout, navigate]
  );

  useEffect(() => {
    fetchCredentials('');
  }, [fetchCredentials]);

  const handleLogoutClick = () => {
    onLogout();
    navigate('/');
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchCredentials(searchTerm);
  };

  return (
    <div>
      <div className="page-banner">
        <h2>Credential Vault Overview</h2>
      </div>

      <div className="vault-layout">
        <aside className="card">
          <h3>Vault Options</h3>
          <button className="btn" type="button" onClick={handleLogoutClick}>
            Logout
          </button>
        </aside>

        <section className="vault-content">
          <div className="card">
            <p>Search for a password or choose from your favorite below...</p>

            <form className="search-form" onSubmit={handleSearchSubmit}>
              <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by site..."
              />

              <button className="btn" type="submit">
                Submit
              </button>

              <Link className="btn" to="/credentials/new">
                Add
              </Link>
            </form>
          </div>

          <div className="cred-list">
            {credentials.length === 0 ? (
              <p>No credentials found.</p>
            ) : (
              credentials.map((c) => <CredentialRow key={c.id} id={c.id} site={c.site} />)
            )}
          </div>
        </section>
      </div>
    </div>
  );
}