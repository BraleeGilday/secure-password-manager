import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { loginUser } from '../api/auth';

function LoginPage() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError("")

        try {
            await loginUser(email, password)
            navigate("/credentials")
        } catch (err) {
            console.log(err)
            const msg =
                err?.response?.data?.detail ||
                "Login failed. Check email/password"
            setError(msg)
        }
    }

    return (
    <div className="form-container">
        <h1 className="form-title">Welcome Back!</h1>
        <form onSubmit={handleSubmit}>
            <label>Enter your email address</label>
            <input 
                type="email"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <label>Enter your password</label>
            <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit">Login</button>
            <p className="form-link" onClick={() => navigate('/register')}>Create Account</p>
        </form>
        {error && <p className="error-text">{error}</p>}
    </div>
    )
}

export default LoginPage;