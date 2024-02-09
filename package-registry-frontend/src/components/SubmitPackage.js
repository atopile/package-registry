import React, { useState } from 'react';
import { functions } from '../firebaseConfig'; // Import Firebase functions
import { httpsCallable } from 'firebase/functions';
import './SubmitPackage.css';

const SubmitPackage = () => {
  const [formData, setFormData] = useState({
    url: '',
    email: '',
    description: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting package with data:', formData); // Added for debugging
    try {

      data = formData.get('data')
      const submitPackage = httpsCallable(functions, 'submit_package');
      // Wrap formData in a 'data' object to match expected request format and include headers for CORS
      const result = await submitPackage({ data: formData, headers: { 'Access-Control-Allow-Origin': '*' } });
      // console.log('Result after submission:', result); // Added for debugging
      if (result.data.message === "Package submitted successfully") {
        // Redirect using window.location for navigation
        window.location.href = '/thanks-for-submitting';
      } else {
        // Check for errors in the result.data.error if the message is not present
        const errorMessage = result.data.error ? result.data.error : 'Submission failed. Please try again.';
        throw new Error(errorMessage);
      }
      setFormData({ url: '', email: '', description: '' });
    } catch (error) {
      console.error('Error submitting package:', error);
      alert(error.message);
    }
  };

  return (
    <div className="submit-package">
      <div className="heading">
        <h1>Submit Your Package</h1>
      </div>
        <p>We will review your package within 24 hours and it will be available upon approval.</p>
      <form onSubmit={handleSubmit} className="submit-package-form">
        <input
          type="text"
          name="url"
          value={formData.url}
          onChange={handleChange}
          placeholder="Package URL"
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Your Email"
          required
        />
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="What does your package do? Why is it awesome?"
          required
        />
        <button type="submit" className="submit-btn">Submit</button>
      </form>
    </div>
  );
};

export default SubmitPackage;
