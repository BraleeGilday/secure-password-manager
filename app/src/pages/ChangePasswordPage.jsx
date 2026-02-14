import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { updateMyPassword } from "../api/user"

function ChangePasswordPage() {
  const navigate = useNavigate()

  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    try {
      await updateMyPassword({
        current_password: currentPassword,
        new_password: newPassword,
      })
      navigate("/login")  // ???
    } catch (e) {
      console.log(e)
      setError(e?.response?.data?.detail || "Password update failed.")
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-title">Change Password</h1>

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
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default ChangePasswordPage;
