import { useState } from "react";
import { useNavigate } from "react-router-dom";

function EditEmailPage() {
  const navigate = useNavigate();

  // Mock current value
  const [email, setEmail] = useState("testUser@example.com");

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = { email: email, display_name: "Test User" }; // unchanged name for now
    console.log("PUT profile update:", payload);

    navigate("/profile");
  };

  return (
    <div className="form-container">
      <h2>Update Email</h2>

      <form onSubmit={handleSubmit}>
        <label>New email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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

export default EditEmailPage;
