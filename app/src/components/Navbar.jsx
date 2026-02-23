import { useLocation, useNavigate } from 'react-router-dom';
import Searchbar from './Searchbar';

export default function Navbar({ isLoggedIn, onLogout }) {
  const navigate = useNavigate();
  const location = useLocation();

  const showSearch = isLoggedIn && location.pathname === '/credentials';

  const handleLogin = () => {
    // Token paste login on welcome page (TEMP)
    navigate('/');
  };

  const handleLogout = () => {
    onLogout?.();
    navigate('/');
  };

  return (
    <>
      <header>
        <div className="navbar">
          <div>
            <h1 style={{ cursor: 'pointer' }} onClick={() => navigate(isLoggedIn ? '/credentials' : '/')}
            >
              SPM
            </h1>
          </div>

          {isLoggedIn ? (
            <>
              {showSearch ? <Searchbar /> : null}
              <nav>
                <div>
                  <a>Profile</a>
                  <a onClick={handleLogout}>Logout</a>
                </div>
              </nav>
            </>
          ) : (
            <>
              <nav>
                <div>
                  <a>register</a>
                  <a onClick={handleLogin}>Login</a>
                </div>
              </nav>
            </>
          )}
        </div>
      </header>
    </>
  );
}
