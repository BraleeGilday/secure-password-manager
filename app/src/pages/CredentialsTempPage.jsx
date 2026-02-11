import { useNavigate } from 'react-router-dom';

function CredentialsTempPage() {
    const navigate = useNavigate()

    return (
    <div>
        <h1>My Credentials</h1>
        <button onClick={() => navigate('/profile')}>Profile Settings</button>
    </div>
    )
}

export default CredentialsTempPage;