import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import PackageImage from './PackageImage';

const CopyInstallCommand = ({ packageName }) => {
  const copyToClipboard = () => {
    const installCommand = `ato install ${packageName}`;
    navigator.clipboard.writeText(installCommand).then(() => {
      console.log('Install command copied to clipboard!');
    }, (err) => {
      console.error('Could not copy text: ', err);
    });
  };

  return (
    <div className="copy-install-command">
      <span className="install-command">ato install {packageName}</span>
      <button onClick={copyToClipboard} className="search-result-button">
        <FontAwesomeIcon icon={faCopy} />
      </button>
    </div>
  );
};

export default CopyInstallCommand;