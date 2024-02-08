import React, { useState } from 'react';
import SearchBar from './SearchBar'; // Assuming you have this component for search functionality
import logo from '../assets/logo.png'; // Update the path to your logo
import { db } from '../firebaseConfig';
import { collection, addDoc } from 'firebase/firestore';
import './Header.css'; // Ensure your CSS is properly organized for layout
import { Link } from 'react-router-dom';

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
      <img src={logo} alt="Logo" className="header-logo" padding="20px" />
      <Link to="submit-package" className="submit-btn">Submit Package</Link>
    </header>
  );
};

export default Header;