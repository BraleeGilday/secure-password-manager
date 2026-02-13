import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()

        const payload = {
            username: email,
            password: password,
        }
        
        console.log('Login payload:', payload)

        // Pretend we are authorized
        navigate('/credentials')
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
    </div>
    )
}

export default LoginPage;