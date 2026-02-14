import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaRegEnvelope, FaRegIdCard, FaLock, FaRegTrashCan } from "react-icons/fa6";
import ProfileCard from "../components/ProfileCard";
import { fetchMyProfile } from "../api/user";

function UserProfilePage() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null)
  const [error, setError] = useState("")   // show token expired

  useEffect( () => {
    const load = async () => {
      setError("")

      const token = localStorage.getItem("access_token")
      if (!token) {
        navigate("/login")
        return
      }
      
      try {
        const data = await fetchMyProfile()
        setUser(data)
      } catch (err) {
        console.log(err)
        setError("Could not load profile. Please log in again.")
        localStorage.removeItem("access_token")
        navigate("/login")
      }
    }
    load()
  }, [navigate])

  if (!user) return <p className="error-text">{error || "No user found."}</p> // keep?

  return (
    <div className="profile-wrapper">
      <h1 className="profile-title">My Account</h1>

      <div className="profile-cards">
        <ProfileCard
          icon={<FaRegEnvelope size={28} />}
          heading="Account Email"
          value={user.email}
          linkText="Edit email address"
          onClick={() => navigate("/profile/email")}
        />

        <ProfileCard
          icon={<FaRegIdCard size={28} />}
          heading="Display Name"
          value={user.display_name || "(none)"}
          linkText="Add or edit name"
          onClick={() => navigate("/profile/name")}
        />

        <ProfileCard
          icon={<FaLock size={28} />}
          heading="Account Password"
          value="••••••••"
          linkText="Change password"
          onClick={() => navigate("/profile/password")}
        />

        <ProfileCard
          icon={<FaRegTrashCan size={28} />}
          heading="Delete Account"
          value="Permanently delete your account and all saved credentials."
          linkText="Delete account"
          onClick={() => navigate("/profile/delete")}
        />
      </div>
      <p className="form-link" onClick={() => navigate("/credentials")}>
        Back to Credentials
      </p>

    </div>
  );
}

export default UserProfilePage;
