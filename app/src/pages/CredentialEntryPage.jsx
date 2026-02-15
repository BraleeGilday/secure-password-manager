import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

export default function CredentialEntryPage({ token, onLogout }) {
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

  const handleDelete = async () => {
    const response = await axios.delete(`/spm/credentials/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      validateStatus: () => true,
    });

    if (response.status === 401) {
      onLogout();
      navigate('/', { state: { message: 'Session expired, paste token' } });
      return;
    }

    if (response.status === 200 || response.status === 204) {
      navigate('/credentials');
      return;
    }
  };

  return (
    <div>
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
              <h3>Credential Details</h3>
              <div className="card-actions">
                <button
                  className="btn"
                  type="button"
                  onClick={() => navigate(`/credentials/${id}/edit`)}
                >
                  Edit
                </button>
                <button className="btn" type="button" onClick={handleDelete}>
                  Delete
                </button>
              </div>
            </div>

            <div>
              <label className="field">
                <span>Site</span>
                <input value={site} readOnly />
              </label>

              <label className="field">
                <span>Username</span>
                <input value={username} readOnly />
              </label>

              <label className="field">
                <span>Password</span>
                <div className="password-row">
                  <input value={password} type={showPassword ? 'text' : 'password'} readOnly />
                  <button
                    className="btn"
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? 'Hide' : 'Show'}
                  </button>
                </div>
              </label>

              <label className="field">
                <span>Notes</span>
                <div className="notes-block">{notes}</div>
              </label>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
