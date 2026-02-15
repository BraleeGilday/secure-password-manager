import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function CredentialCreatePage({ token, onLogout }) {
  const navigate = useNavigate();

  const [site, setSite] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [notes, setNotes] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      site,
      username,
      password,
      notes,
    };

    const response = await axios.post('/spm/credentials/', payload, {
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

    if (response.status === 200 || response.status === 201) {
      navigate('/credentials');
      return;
    }
  }

  return (
    <div>
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
            <h3>Add Credential</h3>

            <form onSubmit={handleSubmit}>
              <label className="field">
                <span>Site</span>
                <input value={site} onChange={(e) => setSite(e.target.value)} placeholder="e.g., Google" />
              </label>

              <label className="field">
                <span>Username</span>
                <input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g., user@example.com"
                />
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
                Create Credential
              </button>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
}
