import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const ThanksForSubmitting = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/');
    }, 10000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Thank You for Submitting Your Package!</h1>
      <p>Your contribution is much appreciated. Redirecting to the main page in 10 seconds...</p>
    </div>
  );
};

export default ThanksForSubmitting;
