import React, { useState, useEffect } from 'react';
import { ref, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebaseConfig'; // Adjust the path as necessary
import './SearchResult.css';

const SearchResult = ({ title, description, images }) => {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    if (images && images.length > 0) {
      const firstImageUrl = images[0];
      const imageRef = ref(storage, firstImageUrl); // Use the imported `storage` instance

      getDownloadURL(imageRef)
        .then((url) => {
          setImageUrl(url);
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
    }
  }, [images]);

  return (
    <div className="search-result">
      {imageUrl && (
        <img src={imageUrl} alt="Package" style={{ width: '200px', height: '200px', objectFit: 'cover', padding: '20px'}} />
      )}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
};

export default SearchResult;