import React, { useState } from 'react';
import { db } from '../firebaseConfig';
import { collection, addDoc } from 'firebase/firestore';
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
    try {
      const submissionsRef = collection(db, 'packageSubmissions');
      await addDoc(submissionsRef, {
        ...formData,
        submittedAt: new Date(),
      });
      alert('Package submitted successfully.');
      setFormData({ url: '', email: '', description: '' }); // Reset form
    } catch (error) {
      console.error('Error submitting package:', error);
      alert('Submission failed. Please try again.');
    }
  };

  return (
    
    <div className="submit-package">
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
          placeholder="Package Description"
          required
        />
        <button type="submit" className="submit-btn">Submit</button>
      </form>
    </div>
  );
};

export default SubmitPackage;