import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SearchResultsContainer from './components/SearchResultsContainer';
import Header from './components/Header';
import PackageDetails from './components/PackageDetails'; // Import your new component
import './App.css';
import SubmitPackage from './components/SubmitPackage';
import ThanksForSubmitting from './components/ThanksForSubmitting';


function App() {
  // Your existing handleSearch and handleFilterChange functions

  return (
    <Router>
      <div className="App">
        <Header />
        <div className="content">
          <Routes>
            <Route path="/" element={<SearchResultsContainer />} />
            <Route path="/package/:id" element={<PackageDetails />} /> {/* New route for PackageDetail */}
            <Route path="/submit-package" element={<SubmitPackage />} />
            <Route path="/thanks-for-submitting" element={<ThanksForSubmitting />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
