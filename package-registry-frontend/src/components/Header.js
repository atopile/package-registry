// src/components/Header.js

import React from 'react';
import './Header.css'; // Make sure to create a corresponding CSS file
import logo from '../assets/Asset 4@3x-8.png'; // Adjust the path to where you've placed your logo
import SearchBar from './SearchBar'; // Import the SearchBar component
import './Header.css'; // Style your header as needed


function Header() {
  return (
    <header className="App-header">
      <img src={logo} alt="Logo" className="App-logo" />
      <SearchBar />
      {/* Other header content */}
    </header>
  );
}

export default Header;