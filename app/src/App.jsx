import {useState} from 'react';
import {Route, Routes, Router} from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <>
    <Navbar 
      isLoggedIn={isLoggedIn} 
      setIsLoggedIn={setIsLoggedIn}
    />
    <main>
        {/* Routers */}
    </main>
    <Footer />
    </>
  )
}

export default App
