import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import { ref, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebaseConfig';
import './SearchResult.css';

function checkForOverflow() {
    const blurbs = document.querySelectorAll('.search-result-blurb');

    blurbs.forEach(blurb => {
      if (blurb.scrollHeight > blurb.clientHeight) {
        // Content is overflowing
        blurb.classList.add('is-overflowing');
      } else {
        blurb.classList.remove('is-overflowing');
      }
    });
  }

const SearchResult = ({ title, blurb, images, name, stars, contributors, url }) => {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    checkForOverflow();
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


  const copyToClipboard = () => {
    const installCommand = `ato install ${name}`;
    navigator.clipboard.writeText(installCommand).then(() => {
      console.log('Install command copied to clipboard!');
    }, (err) => {
      console.error('Could not copy text: ', err);
    });
  };

  return (
    <div className="search-result">
      <div className="search-result-image-container">
        {imageUrl && (
          <img src={imageUrl} alt="Package" className="search-result-image" />
        )}
      </div>
      <div className="search-result-info">
        <h2 className="search-result-title">{title}</h2>
        <p className="search-result-blurb">{blurb}</p>
      </div>
      <div className="search-result-right">
        <div className="search-result-extras">
            <div className="search-result-stars">
            ⭐ {stars} Stars
            </div>
            <div className="search-result-contributors">
            👤 {contributors.length} Contributors
            </div>
            <a href={url} target="_blank" rel="noopener noreferrer" className="search-result-repo-link">
            View on GitHub
            </a>
        </div>
        <div className="copy-install-command">
            <span className="install-command">ato install {name}</span>
            <button onClick={copyToClipboard} className="search-result-button">
            <FontAwesomeIcon icon={faCopy} />
            </button>
        </div>
        </div>
    </div>
  );
};

export default SearchResult;