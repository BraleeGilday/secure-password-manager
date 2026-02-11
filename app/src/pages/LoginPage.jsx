import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const navigate = useNavigate()

    return (
    <div>
        <h1>Login</h1>

        <button onClick={() => navigate('/register')}>Create an account</button>
        <button onClick={() => navigate('/credentials')}>Login - temporary</button>
    </div>
    )
}

export default LoginPage;