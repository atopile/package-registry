import React from 'react';

const PackageDetails = ({ match }) => {
  // You can access the package name from the URL via match.params.packageName
  const packageName = match.params.packageName;

  // Fetch package details using packageName or pass it as a prop

  return (
    <div>
      <h1>{packageName}</h1>
      {/* Render package details here */}
    </div>
  );
};

export default PackageDetails;