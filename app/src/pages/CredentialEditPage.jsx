import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import api from '../api/client';

import PasswordGeneratorButton from './pwd_gen/PasswordGeneratorButton';

export default function CredentialEditPage({ token, onLogout }) {
  const navigate = useNavigate();
  const { id } = useParams();

  const [formData, setFormData] = useState({
    site: '',
    username: '',
    password: '',
    notes: '',
  });
  const [showPassword, setShowPassword] = useState(false);

  const updateField = (field) => (e) => {
    const value = e.target.value;
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  useEffect(() => {
    async function fetchCredential() {
      const response = await api.get(`/spm/credentials/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        validateStatus: () => true,
      });

      if (response.status === 401) {
        onLogout();
        navigate('/', { state: { message: 'Session expired, paste new token' } });
        return;
      }

      if (response.status !== 200) {
        return;
      }

      const data = response.data || {};
      setFormData({
        site: data.site || '',
        username: data.username || '',
        password: data.password || '',
        notes: data.notes || '',
      });
    }

    fetchCredential();
  }, [id, token, navigate, onLogout]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Required fields check (site, username, password)
    if (!formData.site.trim() || !formData.username.trim() || !formData.password.trim()) {
    window.alert('Please enter a Site, Username, and Password to edit a credential.');
    return;
    }

    const response = await api.patch(`/spm/credentials/${id}`, formData, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      validateStatus: () => true,
    });

    if (response.status === 401) {
      onLogout();
      navigate('/', { state: { message: 'Session expired, paste new token' } });
      return;
    }

    // Duplicate site and username combination check
    if (response.status === 409) {
      const msg ='A credential for this site and username combination already exists, use a different site or username.';
      window.alert(msg);
      return;
    }

    if (response.status === 200 || response.status === 204) {
      navigate(`/credentials/${id}`);
    }
  };

  return (
    <div className="vault-page">
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
            <h3 style={{ marginTop: 0 }}>Edit Credential</h3>

            <form onSubmit={handleSubmit}>
              <label className="field">
                <span>Site</span>
                <input value={formData.site} onChange={updateField('site')} placeholder="e.g., Google" />
              </label>

              <label className="field">
                <span>Username</span>
                <input
                  value={formData.username}
                  onChange={updateField('username')}
                  placeholder="e.g., user@example.com"
                />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-row">
                  <input
                    value={formData.password}
                    onChange={updateField('password')}
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Enter a password..."
                  />
                  <button className="btn" type="button" onClick={() => setShowPassword(!showPassword)}>
                    {showPassword ? 'Hide' : 'Show'}
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
                  onChange={updateField('notes')}
                  rows={5}
                  placeholder="Optional notes..."
                />
              </label>

              <button className="btn" type="submit" style={{ marginTop: 12 }}>
                Confirm Edits
              </button>
            </form>
          </div>
        </section>
      </div>
    </div>
  );
}
