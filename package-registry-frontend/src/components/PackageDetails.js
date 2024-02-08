import React from 'react';
import { useLocation } from 'react-router-dom';
import CopyInstallCommand from './CopyInstallCommand';
import PackageImage from './PackageImage';


function PackageDetails() {
  const location = useLocation();
  const pkg = location.state.pkg; // Access the pkg object passed as state

  // Now you can use pkg to render your package details
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <div style={{ background: '#f0f0f0', width: '20%', textAlign: 'center' }}></div>
        <div style={{ width: '60%' }}>
          <h1>{pkg.title}</h1>
          <CopyInstallCommand packageName={pkg.name} />
          <PackageImage images={pkg.images} />
          <p>{pkg.blurb}</p>
        </div>
        <div style={{ background: '#f0f0f0', width: '20%', textAlign: 'center' }}></div>
      </div>


    </div>
  );
}

export default PackageDetails;