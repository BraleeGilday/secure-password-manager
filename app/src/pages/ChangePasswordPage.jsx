import { useState } from "react";
import { useNavigate } from "react-router-dom";

function ChangePasswordPage() {
  const navigate = useNavigate();

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = { current_password: currentPassword, new_password: newPassword };
    console.log("PUT password update:", payload);

    navigate("/profile");
  };

  return (
    <div className="form-container">
      <h2>Change Password</h2>

      <form onSubmit={handleSubmit}>
        <label>Current password</label>
        <input
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          required
        />

        <label>New password</label>
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
        />

        <button type="submit">Save</button>

        <p className="form-link" onClick={() => navigate("/profile")}>
          Back to Profile
        </p>
      </form>
    </div>
  );
}

export default ChangePasswordPage;
