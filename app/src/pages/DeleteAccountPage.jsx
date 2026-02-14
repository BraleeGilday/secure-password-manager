import { useState } from "react";
import { useNavigate } from "react-router-dom";

function DeleteAccountPage() {
  const navigate = useNavigate();
  const [confirmText, setConfirmText] = useState("");

  const handleDelete = (e) => {
    e.preventDefault();

    // Later: call backend delete endpoint
    console.log("Would delete account now.");

    navigate("/login");
  };

  const isValid = confirmText.trim().toUpperCase() === "DELETE";

  return (
    <div className="form-container">
      <h2>Delete Account</h2>

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
    </div>
  );
}

export default DeleteAccountPage;
