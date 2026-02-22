import {useState} from 'react';
import {Route, Routes} from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

import Welcome from './pages/Welcome';

import './App.css'
import { BrowserRouter as Routes, Route } from 'react-router-dom'

import LoginPage from './pages/LoginPage.jsx'
import CredentialsTempPage from './pages/CredentialsTempPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import UserProfilePage from './pages/UserProfilePage.jsx'
import EditEmailPage from './pages/EditEmailPage.jsx'
import EditDisplayNamePage from './pages/EditDisplayNamePage.jsx'
import ChangePasswordPage from './pages/ChangePasswordPage.jsx'
import DeleteAccountPage from './pages/DeleteAccountPage.jsx'
import Welcome from './pages/Welcome.jsx'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

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
          <Route path="/login" element={<LoginPage />}></Route>
          <Route path="/register" element={<RegisterPage />}></Route>

          {/* User Pages */}
          <Route path="/profile" element={<UserProfilePage />}></Route>
          <Route path="/profile/email" element={<EditEmailPage />} />
          <Route path="/profile/name" element={<EditDisplayNamePage />} />
          <Route path="/profile/password" element={<ChangePasswordPage />} />
          <Route path="/profile/delete" element={<DeleteAccountPage />} />

          {/* Temp - Delete */}
          <Route path="/credentials" element={<CredentialsTempPage />}></Route>

        </Routes>
    </main>
    <Footer />
    </>
  )
}

export default App
