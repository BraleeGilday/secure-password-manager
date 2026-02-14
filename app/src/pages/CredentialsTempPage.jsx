import { useNavigate } from 'react-router-dom';

function CredentialsTempPage() {
    const navigate = useNavigate()

    return (
    <div>
        <h1>My Credentials</h1>
        <p><b>chrome.com</b></p>
        <p>username: example10</p>
        <p>password: ***************</p>
        <br />
        <button onClick={() => navigate('/profile')}>Profile Settings</button>
    </div>
    )
}

export default CredentialsTempPage;