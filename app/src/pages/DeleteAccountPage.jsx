import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { deleteMyAccount } from "../api/user"

function DeleteAccountPage() {
  const navigate = useNavigate()
  const [confirmText, setConfirmText] = useState("")
  const [error, setError] = useState("")

  const handleDelete = async (e) => {
    e.preventDefault()
    setError("")

    try {
      await deleteMyAccount()
      localStorage.removeItem("access_token")
      navigate("/login")
    } catch (e) {
      console.log(e)
      setError(e?.response?.data?.detail || "Delete failed.")
    }
  }

  const isValid = confirmText.trim().toUpperCase() === "DELETE";

  return (
    <div className="form-container">
      <h1 className="form-title">Delete Account</h1>

      <form onSubmit={handleDelete}>
        <p className="muted">
          This action is permanent. To confirm, type <strong>DELETE</strong> below.
        </p>

        <label>Type DELETE to confirm</label>
        <input
          type="text"
          value={confirmText}
          onChange={(e) => setConfirmText(e.target.value)}
          required
        />

        <button type="submit" disabled={!isValid}>
          Delete account
        </button>

        <p className="form-link" onClick={() => navigate("/profile")}>
          Back to Profile
        </p>
      </form>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default DeleteAccountPage;
