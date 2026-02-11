import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
    const navigate = useNavigate()

    return (
    <div>
        <h1>Register</h1>
        <button onClick={() => navigate('/login')}>Back to Login</button>
    </div>
    )
}

export default RegisterPage;