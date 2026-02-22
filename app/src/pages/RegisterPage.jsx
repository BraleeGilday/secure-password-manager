import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from "../api/auth";

import FormLink from '../components/FormLink';
import ErrorText from '../components/ErrorText';

function RegisterPage() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [displayName, setDisplayName] = useState('')

    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError("")

        try {
            await registerUser({ email, password, displayName })
            navigate("/login")
        } catch (err) {
            console.log(err)
            const msg =
                err?.response?.data?.detail ||
                "Registration failed. Please try again.";
            setError(msg);
        }
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

            <FormLink to="/login">Back to Login</FormLink>
        </form>
        <ErrorText>{error}</ErrorText>
    </div>
    )
}

export default RegisterPage;