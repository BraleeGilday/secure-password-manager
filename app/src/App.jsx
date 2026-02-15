import './App.css';

import { useState } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom';

// Remove this homepage later with real User one
import HomePage from './pages/HomePage';

import VaultOverviewPage from './pages/VaultOverviewPage';
import CredentialEntryPage from './pages/CredentialEntryPage';
import CredentialCreatePage from './pages/CredentialCreatePage';
import CredentialEditPage from './pages/CredentialEditPage';

const TOKEN_KEY = 'spm_token';

function getSavedToken() {
  return localStorage.getItem(TOKEN_KEY) || '';
}

function RequireAuth({ token, children }) {
  const location = useLocation();

  if (!token) {
    return (
      <Navigate
        to="/"
        replace
        state={{
          message: 'Paste access token from backend docs',
          from: location.pathname,
        }}
      />
    );
  }

  return children;
}

export default function App() {
  const [token, setToken] = useState(getSavedToken());

  const saveToken = (newToken) => {
    localStorage.setItem(TOKEN_KEY, newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken('');
  };

  return (
    <Router>
      <main>
        <Routes>
          <Route
            path="/"
            element={<HomePage token={token} onSaveToken={saveToken} onClearToken={logout} />}
          />
          <Route
            path="/credentials"
            element={
              <RequireAuth token={token}>
                <VaultOverviewPage token={token} onLogout={logout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/new"
            element={
              <RequireAuth token={token}>
                <CredentialCreatePage token={token} onLogout={logout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/:id"
            element={
              <RequireAuth token={token}>
                <CredentialEntryPage token={token} onLogout={logout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/:id/edit"
            element={
              <RequireAuth token={token}>
                <CredentialEditPage token={token} onLogout={logout} />
              </RequireAuth>
            }
          />
        </Routes>
      </main>
      <footer>
        <p>&copy; 2026 Secure Password Manager</p>
      </footer>
    </Router>
  );
}
