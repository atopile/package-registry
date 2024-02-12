// src/components/FilterContainer.js

import React, { useState } from 'react';
import './FilterContainer.css';

function FilterContainer({ onFilterChange }) {
  const [inputVoltage, setInputVoltage] = useState({ min: 0, max: 100 });

  const handleRangeChange = (event) => {
    const { name, value } = event.target;
    setInputVoltage((prev) => ({ ...prev, [name]: value }));
    onFilterChange({ ...inputVoltage, [name]: value });
  };

  return (
    <div className="filter-container">
      <h2>Filters</h2>
      <div className="filter-option">
        <label htmlFor="input-voltage-min">Input Voltage (0-100V):</label>
        <input
          type="range"
          id="input-voltage-min"
          name="min"
          min="0"
          max="100"
          value={inputVoltage.min}
          onChange={handleRangeChange}
        />
        <input
          type="range"
          id="input-voltage-max"
          name="max"
          min="0"
          max="100"
          value={inputVoltage.max}
          onChange={handleRangeChange}
        />
        <div className="range-inputs">
          <input
            type="number"
            id="input-voltage-min-text"
            name="min"
            min="0"
            max="100"
            value={inputVoltage.min}
            onChange={handleRangeChange}
          />
          <input
            type="number"
            id="input-voltage-max-text"
            name="max"
            min="0"
            max="100"
            value={inputVoltage.max}
            onChange={handleRangeChange}
          />
        </div>
      </div>
      {/* Add more filters as needed */}
    </div>
  );
}

export default FilterContainer;