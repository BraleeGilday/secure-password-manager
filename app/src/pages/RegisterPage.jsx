import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [displayName, setDisplayName] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()

        const payload = {
            email: email,
            password: password,
            display_name: displayName.trim() ? displayName.trim() : null,
        }
        
        console.log('Register payload:', payload)

        // Pretend we are authorized
        navigate('/login')
    }

    return (
    <div className="form-container">
        <h1 className="form-title">Create Account</h1>
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
            <label>Display Name (optional)</label>
            <input 
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
            />
            <button type="submit">Create Account</button>
            <p className="form-link" onClick={() => navigate('/login')}>Back to Login</p>
        </form>
    </div>
    )
}

export default RegisterPage;