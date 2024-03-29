import React, { useEffect, useState } from 'react';
import SearchResult from './SearchResult';
import { functions } from '../firebaseConfig'; // Import Firebase functions
import { httpsCallable } from 'firebase/functions';
import './SearchResultsContainer.css';

function SearchResultsContainer() {
  const [packages, setPackages] = useState([]);

  useEffect(() => {
    const listPackages = httpsCallable(functions, 'list_packages');
    listPackages().then((result) => {
      console.log("API call result:", result.data);
      setPackages(result.data);
    }).catch((error) => {
      console.error("API call failed:", error);
    });
  }, []);

  return (
    <div className="search-results-container">
      {packages.filter(pkg => pkg.display).map((pkg) => (
        <SearchResult pkg = {pkg}/>
      ))}
    </div>
  );
}

export default SearchResultsContainer;