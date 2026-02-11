import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

import LoginPage from './pages/LoginPage.jsx'
import CredentialsTempPage from './pages/CredentialsTempPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import UserProfilePage from './pages/UserProfilePage.jsx'

function App() {
  return (
    <div>
      <Router>
        <main>
          <Routes>

            {/* Default route */}
            <Route path="/" element={<Navigate to="/login" replace />} />

            {/* User Pages*/}
            <Route path="/login" element={<LoginPage />}></Route>
            <Route path="/register" element={<RegisterPage />}></Route>
            <Route path="/profile" element={<UserProfilePage />}></Route>
            <Route path="/credentials" element={<CredentialsTempPage />}></Route>
          </Routes>
        </main>
      </Router>
    </div>
  )
}

export default App
