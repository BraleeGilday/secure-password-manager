import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { fetchMyProfile, updateMyProfile } from "../api/user"

// TO-DO
// Add a confirmation to this page and instructions that
// Upon changing their email, they'll be signed out and 
// must sign back in with changed email.

function EditEmailPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [displayName, setDisplayName] = useState("") // keep unchanged
  const [error, setError] = useState("")

  useEffect(() => {
    const load = async () => {
      try {
        const u = await fetchMyProfile();
        setEmail(u.email)
        setDisplayName(u.display_name || "")
      } catch (e) {
        console.log(e)
        setError("Could not load profile.")
      }
    }
    load()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("")

    try {
      await updateMyProfile({
        email,
        display_name: displayName || null,
      })
      navigate("/login")  // ???
    } catch(e) {
        console.log(e)
        setError(e?.response?.data?.detail || "Update failed.")
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-title">Update Email</h1>

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
        </p>  {/* Could add: Are you sure? Unsaved changes */}
      </form>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default EditEmailPage;
