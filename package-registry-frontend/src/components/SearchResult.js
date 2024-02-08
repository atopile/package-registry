import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import './SearchResult.css';
import { Link } from 'react-router-dom';
import CopyInstallCommand from './CopyInstallCommand';
import PackageImage from './PackageImage';
import { faStar } from '@fortawesome/free-solid-svg-icons';


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
  const SearchResult = ({ pkg }) => {

  const copyToClipboard = () => {
    const installCommand = `ato install ${pkg.name}`;
    navigator.clipboard.writeText(installCommand).then(() => {
      console.log('Install command copied to clipboard!');
    }, (err) => {
      console.error('Could not copy text: ', err);
    });
  };

  return (
    <div className="search-result">
      <div className="search-result-image-container">
        <PackageImage images={pkg.images} />
      </div>
      <div className="search-result-info">
      <h2 className="search-result-title">
        <Link to={`/package/${pkg.name}`} state={{ pkg }}>
            {pkg.title}
        </Link>
        </h2>
        <p className="search-result-blurb">{pkg.blurb}</p>
      </div>
      <div className="search-result-right">
        <div className="search-result-extras">
        </div>
        <CopyInstallCommand packageName={pkg.name} />
            <div className="search-result-stars">
            <FontAwesomeIcon icon={faStar} />
            {pkg.stars}
            </div>
            <div className="search-result-contributors">
            👤 {pkg.contributors.length} Contributors
            </div>
            <a href={pkg.repo_url} target="_blank" rel="noopener noreferrer" className="search-result-repo-link">
            View on GitHub
            </a>
        </div>
    </div>
  );
};

export default SearchResult;