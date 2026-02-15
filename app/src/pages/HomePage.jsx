// THIS IS NOT THE REAL HOMEPAGE - CHANGE LATER, THIS IS ONLY FOR GETTING TOKEN IN
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function HomePage({ token, onSaveToken }) {
  const navigate = useNavigate();
  const location = useLocation();

  const initialMsg = (location.state && location.state.message) || '';

  const [tokenInput, setTokenInput] = useState(token || '');
  const [setMessage] = useState(initialMsg);

  const handleSubmit = (e) => {
    e.preventDefault();

    const trimmed = tokenInput.trim();
    if (!trimmed) {
      setMessage('Paste access token from backend docs');
      return;
    }

    onSaveToken(trimmed);
    navigate('/credentials');
  };

  return (
    <div>
      <div className="card">
        <h2>Secure Password Manager</h2>

        <form onSubmit={handleSubmit}>
          <label className="field">
            <span>Access Token Field</span>
            <input
              type="password"
              value={tokenInput}
              onChange={(e) => setTokenInput(e.target.value)}
            />
          </label>

          <div className="card-actions">
            <button type="submit" className="btn">
              Open Vault
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
