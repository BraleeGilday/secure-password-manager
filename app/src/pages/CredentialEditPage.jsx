import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

export default function CredentialEditPage({ token, onLogout }) {
  const navigate = useNavigate();
  const { id } = useParams();

  const [site, setSite] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [notes, setNotes] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    async function fetchCredential() {
      const response = await axios.get(`/spm/credentials/${id}`, {
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
        return;
      }

      const data = response.data;

      setSite((data && data.site) || '');
      setUsername((data && data.username) || '');
      setPassword((data && data.password) || '');
      setNotes((data && data.notes) || '');
    }

    fetchCredential();
  }, [id, token, navigate, onLogout]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      site,
      username,
      password,
      notes,
    };

    const response = await axios.patch(`/spm/credentials/${id}`, payload, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      validateStatus: () => true,
    });

    if (response.status === 401) {
      onLogout();
      navigate('/', { state: { message: 'Session expired, paste a token again' } });
      return;
    }

    if (response.status === 200 || response.status === 204) {
      navigate(`/credentials/${id}`);
      return;
    }
  };

  return (
    <div>
      <div className="page-banner">
        <h2>Edit Credential</h2>
      </div>

      <div className="vault-layout">
        <aside className="card">
          <h3>Navigation Options</h3>
          <Link className="btn" to={`/credentials/${id}`}>
            Back
          </Link>
        </aside>

        <section className="vault-content">
          <div className="card">
            <h3>Edit Credential</h3>

            <form onSubmit={handleSubmit}>
              <label className="field">
                <span>Site</span>
                <input value={site} onChange={(e) => setSite(e.target.value)} placeholder="e.g., Google" />
              </label>

              <label className="field">
                <span>Username</span>
                <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="e.g., user@example.com" />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-row">
                  <input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Enter a password..."
                  />
                  <button className="btn" type="button" onClick={() => setShowPassword(!showPassword)}>
                    {showPassword ? 'Hide' : 'Show'}
                  </button>
                </div>
              </label>

              <label className="field">
                <span>Notes</span>
                <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={5} placeholder="Optional notes..." />
              </label>

              <button className="btn" type="submit">
                Confirm Edits
              </button>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
}
