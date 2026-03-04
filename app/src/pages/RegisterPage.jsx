import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser, loginUser } from "../api/auth";

import FormLink from '../components/FormLink';
import ErrorText from '../components/ErrorText';

function RegisterPage() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState("");
    const [displayName, setDisplayName] = useState('')

    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError("")

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        try {
            // 1) Register
            await registerUser({ email, password, displayName });

            // 2) Login
            const data = await loginUser(email, password);

            // 3) Since MFA is required, login should return mfa_required
            if (data?.mfa_required) {
            navigate("/mfa/setup", { state: { mfaToken: data.mfa_token, email } });
            return;
            }

            // (Fallback - should not happen if MFA required)
            navigate("/credentials");
        } catch (err) {
            console.log(err);
            const msg = err?.response?.data?.detail || "Registration failed. Please try again.";
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
            <label>Confirm password</label>
            <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
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