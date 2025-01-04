import React, { useState } from 'react';
import '../style/nav.css'


const Nav = () => {
    const [menuVisible, setMenuVisible] = useState(false);
  
    const toggleMenu = () => {
      setMenuVisible(!menuVisible);
    };
  
    return (
      <nav className="navbar">
        <a href="#" className="logo">Borko.AI</a>
  
        <ul className={`menu ${menuVisible ? 'show' : ''}`}>
          <li><a href="#research">About Us</a></li>
          <li><a href="#products">Who is Borko?</a></li>
        </ul>
  
        <div className="hamburger" onClick={toggleMenu}>
          ☰
        </div>
      </nav>
    );
  };
  


export default Nav;