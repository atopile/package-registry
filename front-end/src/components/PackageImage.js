import React, { useState, useEffect } from 'react';
import { ref, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebaseConfig';

const PackageImage = ({ images, size }) => {
    
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    if (images && images.length > 0) {
      const firstImageUrl = images[0];
      const imageRef = ref(storage, firstImageUrl);

      getDownloadURL(imageRef)
        .then((url) => {
          setImageUrl(url);
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
    }
  }, [images]);

  if (!imageUrl) return null;

  return (
    <img src={imageUrl} alt="Package" className="search-result-image" />
  );
};

export default PackageImage;