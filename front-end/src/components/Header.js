import React from 'react';
import logo from '../assets/logo.png'; // Update the path to your logo
import './Header.css'; // Ensure your CSS is properly organized for layout
import { Link } from 'react-router-dom';

const Header = () => {

  return (
    <header className="header">
      <Link to="/">
        <img src={logo} alt="Logo" className="header-logo" />
      </Link>
      {/* <Link to="submit-package" className="submit-btn">Submit Package</Link> */}
    </header>
  );
};

export default Header;