// src/App.js

import React from 'react';
import SearchResultsContainer from './components/SearchResultsContainer';
import FilterContainer from './components/FilterContainer'; // Import the FilterContainer component
import dummyResults from './data/dummyData';
import Header from './components/Header'; // Import the Header component
import './App.css'; // This line should be at the top of your App.js file
// import FirebaseImageTest from './FirebaseImageTest';

function App() {
  const handleSearch = (searchTerm) => {
    console.log(searchTerm);
    // Implement your search logic here
  };

  const handleFilterChange = (event) => {
    // Implement your filter logic here
    console.log(event.target.name, event.target.checked);
  };

  return (
    <div className="App">

      <Header /> {/* Include the Header component */}
      <div className="content">
        {/* <aside> */}
          {/* <FilterContainer onFilterChange={handleFilterChange} /> */}
        {/* </aside> */}
        <main>
          <SearchResultsContainer results={dummyResults} />
        </main>
      </div>
    </div>
  );
}

export default App;