import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function UserProfilePage() {
    const navigate = useNavigate()

    return (
    <div>
      <h1>My Profile</h1>
      <button onClick={() => navigate('/credentials')}>Back to Credentials</button>
    </div>
    )
}

export default UserProfilePage;