import { useState } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

import Welcome from './pages/Welcome';
import VaultOverviewPage from './pages/VaultOverviewPage';
import CredentialEntryPage from './pages/CredentialEntryPage';
import CredentialCreatePage from './pages/CredentialCreatePage';
import CredentialEditPage from './pages/CredentialEditPage';

import './App.css';

const TOKEN_KEY = 'token';

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

function App() {
  const [token, setToken] = useState(getSavedToken());

  const saveToken = (newToken) => {
    localStorage.setItem(TOKEN_KEY, newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setToken('');
  };

  const isLoggedIn = Boolean(token);

  return (
    <>
    <Navbar isLoggedIn={isLoggedIn} onLogout={logout} />
    <main>
        {/* Routers */}
        <Routes>
          <Route path="/" element={<Welcome token={token} onSaveToken={saveToken} />} />

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
    <Footer />
    </>
  )
}

export default App
