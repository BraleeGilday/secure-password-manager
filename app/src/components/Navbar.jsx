import { Link, useNavigate } from 'react-router-dom';
import Searchbar from './Searchbar';

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        setIsLoggedIn(false);
        navigate("/login", { replace: true });
    };
    
    return(
        <>
        <header>
            <div className='navbar'>
            <div>
                <h1>SPM</h1>
            </div>
                
                {isLoggedIn ? (
                    <>
                    <Searchbar />
                    <nav>
                        <div>
                            <Link to="/profile">profile</Link>
                            <button type="button" onClick={handleLogout}>
                                logout
                            </button>
                        </div>
                    </nav>
                    </>
                ) : (
                    <>
                    <nav>
                        <div>
                            <Link to="/register">register</Link>
                            <Link to="/login">login</Link>
                        </div>
                    </nav>
                    
                    </>
                )}
            </div>
        </header>
        </>
    )
}