import { useNavigate } from "react-router-dom";
import { FaRegEnvelope, FaRegIdCard, FaLock, FaRegTrashCan } from "react-icons/fa6";
import ProfileCard from "../components/ProfileCard";

function UserProfilePage() {
  const navigate = useNavigate();

  const user = {
    email: "testUser@example.com",
    display_name: "Test User",
  };

  return (
    <div className="profile-wrapper">
      <h1 className="profile-title">Profile Info</h1>

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
