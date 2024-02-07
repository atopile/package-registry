import React, { useState } from 'react';
import SearchBar from './SearchBar'; // Assuming you have this component for search functionality
import logo from '../assets/logo.png'; // Update the path to your logo
import { db } from '../firebaseConfig';
import { collection, addDoc } from 'firebase/firestore';
import './Header.css'; // Ensure your CSS is properly organized for layout

const Header = () => {
  const [packageUrl, setPackageUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    try {
      const submissionsRef = collection(db, 'packageSubmissions');
      await addDoc(submissionsRef, {
        url: packageUrl,
        submittedAt: new Date(),
      });
      alert('Thanks, your package will be reviewed.');
      setPackageUrl('');
    } catch (error) {
      console.error('Error submitting package:', error);
      alert('Submission failed. Please try again.');
    }
  };

  return (
    <header className="header">
      <img src={logo} alt="Logo" className="header-logo" />
      <SearchBar />
      <form onSubmit={handleSubmit} className="package-submit-form">
        <input
          type="text"
          className="package-url-input"
          value={packageUrl}
          onChange={(e) => setPackageUrl(e.target.value)}
          placeholder="Submit package URL"
        />
        <button type="submit" className="submit-btn">Submit</button>
      </form>
    </header>
  );
};

export default Header;