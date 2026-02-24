import { Link, useLocation, useNavigate } from "react-router-dom";
import Searchbar from "./Searchbar";

export default function Navbar({ isLoggedIn, onLogout }) {
  const navigate = useNavigate();
  const location = useLocation();

  const showSearch = isLoggedIn && location.pathname === "/credentials";

  const handleLogout = () => {
    onLogout?.();
    navigate("/login", { replace: true });
  };

  return (
    <header>
      <div className="navbar">
        <div>
          <h1 style={{ margin: 0 }}>
            <Link
              to={isLoggedIn ? "/credentials" : "/"}
              style={{ textDecoration: "none", color: "inherit" }}
            >
              SPM
            </Link>
          </h1>
        </div>

        {isLoggedIn ? (
          <>
            {showSearch ? <Searchbar /> : null}
            <nav>
              <div>
                <Link to="/profile">Profile</Link>
                <button type="button" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            </nav>
          </>
        ) : (
          <nav>
            <div>
              <Link to="/register">register</Link>
              <Link to="/login">login</Link>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}