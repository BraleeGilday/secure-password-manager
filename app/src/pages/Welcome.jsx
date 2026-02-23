import { useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Card from '../components/Card';

export default function Welcome({ token, onSaveToken }) {
  const navigate = useNavigate();
  const location = useLocation();

  const initialMsg = useMemo(() => {
    return (location.state && location.state.message) || '';
  }, [location.state]);

  const [tokenInput, setTokenInput] = useState(token || '');
  const [message, setMessage] = useState(initialMsg);

  const handleSubmit = (e) => {
    e.preventDefault();

    const trimmed = tokenInput.trim();
    if (!trimmed) {
      setMessage('Paste new token');
      return;
    }

    onSaveToken(trimmed);
    navigate('/credentials');
  };

  return (
    <>
      <Card
        content={
          <div>
            <h2 style={{ marginTop: 0 }}>Secure Password Manager</h2>
            <p style={{ marginTop: 6 }}>
              Paste a backend access token to open your vault.
            </p>
            {message ? (
              <p style={{ marginTop: 10 }}>
                <strong>{message}</strong>
              </p>
            ) : null}

            <form onSubmit={handleSubmit} style={{ marginTop: 12 }}>
              <label style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <span>Access Token</span>
                <input
                  type="password"
                  value={tokenInput}
                  onChange={(e) => setTokenInput(e.target.value)}
                  placeholder="Paste token here"
                  style={{ padding: 10 }}
                />
              </label>

              <div style={{ marginTop: 12 }}>
                <button type="submit">Open Vault</button>
              </div>
            </form>
          </div>
        }
      />
    </>
  );
}
