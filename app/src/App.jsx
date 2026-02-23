import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Navbar from './components/Navbar';
import Footer from './components/Footer';

import Welcome from './pages/Welcome';
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'

import UserProfilePage from './pages/UserProfilePage.jsx'
import EditEmailPage from './pages/EditEmailPage.jsx'
import EditDisplayNamePage from './pages/EditDisplayNamePage.jsx'
import ChangePasswordPage from './pages/ChangePasswordPage.jsx'
import DeleteAccountPage from './pages/DeleteAccountPage.jsx'

import './App.css'

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

// Placeholder for credentials until real pages exist
// Delete Me once Credentials exists!!
function CredentialsPlaceholder() {
  return (
    <div style={{ padding: "1rem" }}>
      <h2>Credentials</h2>
      <p>Coming soon.</p>
    </div>
  );
}


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  return (
    <>
    <Navbar 
      isLoggedIn={isLoggedIn} 
      setIsLoggedIn={setIsLoggedIn}
    />
    <main>
        {/* Routers */}
        <Routes>
          <Route path="/" element={<Welcome />} />

          {/* Auth */}
          <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected User Pages */}
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

          {/* REVISE once Credentials implemented (remove temp page) */}
          <Route
            path="/credentials"
            element={
              <RequireAuth isLoggedIn={isLoggedIn}>
                <CredentialsPlaceholder />
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
