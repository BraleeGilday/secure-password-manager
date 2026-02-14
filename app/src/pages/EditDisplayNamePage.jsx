import { useState } from "react";
import { useNavigate } from "react-router-dom";

function EditDisplayNamePage() {
  const navigate = useNavigate();

  const [displayName, setDisplayName] = useState("Test User");

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = { email: "testUser@example.com", display_name: displayName.trim() || null };
    console.log("PUT profile update:", payload);

    navigate("/profile");
  };

  return (
    <div className="form-container">
      <h2>Update Display Name</h2>

      <form onSubmit={handleSubmit}>
        <label>Display name</label>
        <input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
        />

        <button type="submit">Save</button>

        <p className="form-link" onClick={() => navigate("/profile")}>
          Back to Profile
        </p>
      </form>
    </div>
  );
}

export default EditDisplayNamePage;
