import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchMyProfile, updateMyProfile } from "../api/user";

import FormLink from "../components/FormLink";
import ErrorText from "../components/ErrorText";

function EditDisplayNamePage() {
  const navigate = useNavigate();
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
      navigate("/profile")
    } catch(e) {
        console.log(e)
        setError(e?.response?.data?.detail || "Update failed.")
    }
  }

  return (
    <div className="form-container">
      <h1 className="form-title">Update Display Name</h1>

      <form onSubmit={handleSubmit}>
        <label>Display name</label>
        <input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
        />

        <button type="submit">Save</button>

        <FormLink to="/profile">Back to Profile</FormLink>
      </form>
      <ErrorText>{error}</ErrorText>
    </div>
  )
}

export default EditDisplayNamePage;
