function ProfileCard({ icon, heading, value, linkText, onClick }) {
  return (
    <div className="profile-card">
      <div className="profile-card-main">
        <div className="profile-icon">{icon}</div>

        <div className="profile-card-text">
          <div className="profile-card-heading">{heading}</div>
          <div className="profile-card-value">{value}</div>
        </div>
      </div>

      <button
        type="button"
        className="profile-link"
        onClick={onClick}
      >
        {linkText}
      </button>
    </div>
  );
}

export default ProfileCard;
