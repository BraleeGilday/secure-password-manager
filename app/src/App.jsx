import { useEffect, useState } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Welcome from "./pages/Welcome";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";

import UserProfilePage from "./pages/UserProfilePage.jsx";
import EditEmailPage from "./pages/EditEmailPage.jsx";
import EditDisplayNamePage from "./pages/EditDisplayNamePage.jsx";
import ChangePasswordPage from "./pages/ChangePasswordPage.jsx";
import DeleteAccountPage from "./pages/DeleteAccountPage.jsx";

import VaultOverviewPage from "./pages/VaultOverviewPage.jsx";
import CredentialEntryPage from "./pages/CredentialEntryPage.jsx";
import CredentialCreatePage from "./pages/CredentialCreatePage.jsx";
import CredentialEditPage from "./pages/CredentialEditPage.jsx";
import MfaVerifyPage from "./pages/MfaVerifyPage.jsx";
import MfaSetupPage from "./pages/MfaSetupPage.jsx";

import "./App.css";


/**
 * RequireAuth acts as a route guard for protected pages.
 *
 * If the user is logged in, it renders the requested page (children).
 * If not, it redirects the user to the login page instead.
 *
 * This prevents unauthenticated users from accessing protected routes
 * like /profile or /credentials directly via the URL.
 */
function RequireAuth({ isLoggedIn, children }) {
  return isLoggedIn ? children : <Navigate to="/login" replace />;
}


function App() {
  const location = useLocation();

  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  // Keep React state in sync with localStorage on navigation
  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem("access_token"));
  }, [location.pathname]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsLoggedIn(false);
  };

  return (
    <>
      <Navbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      <main>
        <Routes>
          <Route path="/" element={<Welcome />} />

          {/* Auth */}
          <Route
            path="/login"
            element={<LoginPage setIsLoggedIn={setIsLoggedIn} />}
          />
          <Route path="/mfa" element={<MfaVerifyPage setIsLoggedIn={setIsLoggedIn} />} />

          <Route path="/register" element={<RegisterPage />} />
          <Route path="/mfa/setup" element={<MfaSetupPage setIsLoggedIn={setIsLoggedIn} />} />
          
          {/* User Pages */}
          <Route
            path="/profile"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <UserProfilePage />
              </RequireAuth>
            }
          />
          <Route
            path="/profile/email"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <EditEmailPage />
              </RequireAuth>
            }
          />
          <Route
            path="/profile/name"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <EditDisplayNamePage />
              </RequireAuth>
            }
          />
          <Route
            path="/profile/password"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <ChangePasswordPage />
              </RequireAuth>
            }
          />
          <Route
            path="/profile/delete"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <DeleteAccountPage />
              </RequireAuth>
            }
          />

          {/* Credential Pages */}
          <Route
            path="/credentials"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <VaultOverviewPage onLogout={handleLogout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/new"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <CredentialCreatePage onLogout={handleLogout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/:id"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <CredentialEntryPage onLogout={handleLogout} />
              </RequireAuth>
            }
          />
          <Route
            path="/credentials/:id/edit"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <CredentialEditPage onLogout={handleLogout} />
              </RequireAuth>
            }
          />
        </Routes>
      </main>
      <Footer />
    </>
  );
}

export default App;