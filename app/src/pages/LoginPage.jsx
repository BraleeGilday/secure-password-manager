import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api/auth';
import FormLink from '../components/FormLink';
import ErrorText from '../components/ErrorText';

function LoginPage({ setIsLoggedIn }) {
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const data = await loginUser(email, password); // { mfa_required, mfa_token }

      sessionStorage.setItem("mfa_token", data.mfa_token);

      // Always go to MFA verify; it will redirect to setup if needed
      navigate("/mfa", { state: { mfaToken: data.mfa_token, email } });
    } catch (err) {
      console.log(err);
      const msg = err?.response?.data?.detail || "Login failed. Check email/password";
      setError(msg);
    }
  };

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

        <FormLink to="/register">Create Account</FormLink>
      </form>

      <ErrorText>{error}</ErrorText>
    </div>
  );
}

export default LoginPage;