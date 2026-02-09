import React, {useState} from 'react'
import {Link, Router, Routes} from 'react-router-dom';
import './App.css'
import Main from './components/Main';

function App() {
  const copyrightYear = new Date().getFullYear();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogout = () => {
    // remove token;
    setIsLoggedIn(false);
  }
  // this will need to go to separate route
  const handleLogin = () => {
    setIsLoggedIn(true);
  }

  return (
    <>
      <header>
        <div className='navbar'>
        <div>
          <h1>SPM</h1>
        </div>
        <div>
          <nav>
            {/* Use Link */}
            {isLoggedIn ? (
              <div>
                <a>Settings</a>
                <a onClick={handleLogout}>Logout</a>
              </div>
            ):(
              <div>
              <a>Register</a>
              <a onClick={handleLogin}>Login</a>
              </div>
            )}
          </nav>
        </div>
        </div>
      </header>
      <main>
        {/* Routes go here */}
        {isLoggedIn ? (
          <div className='tempbox'>
            <p>Credentials and Things</p>
          </div>
        ): (
          <div className='tempbox'>
            <p>Register or Login to get started!</p>
          </div>
        )}

      </main>
      <footer>
        <p>&copy;{copyrightYear}</p>
      </footer>
    </>
  )
}

export default App
