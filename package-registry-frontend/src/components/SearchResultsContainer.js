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
        <SearchResult
          key={pkg.id}
          title={pkg.title}
          images={pkg.images}
          name={pkg.name}
          price={pkg.price}
          blurb={pkg.blurb}
          contributors={pkg.contributors}
          url={pkg.repo_url}
          tags={pkg.tags}
          stars={pkg.stars}
        />
      ))}
    </div>
  );
}

export default SearchResultsContainer;