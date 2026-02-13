import {Link} from 'react-router-dom';
import Searchbar from './Searchbar';

export default function Navbar({ isLoggedIn, setIsLoggedIn }) {
    // will need to be updated
    const handleLogin = () => {
        setIsLoggedIn(true);
        // redirect to credentials
    }

    const handleLogout = () => {
        // localStorage.removeItem('token');
        setIsLoggedIn(false);
    }
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
                            {/* <Link>logout</Link> */}
                            <a onClick={handleLogout}>logout</a>
                        </div>
                    </nav>
                    </>
                ) : (
                    <>
                    {/* <Link>register</Link>
                    <Link>login</Link> */}
                    <nav>
                        <div>
                            <a>register</a>
                            <a onClick={handleLogin}>login</a>
                        </div>
                    </nav>
                    
                    </>
                )}
            </div>
        </header>
        </>
    )
}