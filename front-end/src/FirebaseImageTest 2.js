import React, { useEffect, useState } from 'react';
import { getStorage, ref, getDownloadURL } from 'firebase/storage';
import { storage } from './firebaseConfig'; // Adjust the path as necessary

const FirebaseImageTest = () => {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    const imageRef = ref(storage, 'gs://atopile.appspot.com/low-side-current-sensor.png'); // Adjust the path to your image in Firebase Storage

    getDownloadURL(imageRef)
      .then((url) => {
        setImageUrl(url);
      })
      .catch((error) => {
        console.error("Error fetching image:", error);
      });
  }, []);

  return imageUrl ? <img src={imageUrl} alt="Test" /> : <p>Loading image...</p>;
};

export default FirebaseImageTest;