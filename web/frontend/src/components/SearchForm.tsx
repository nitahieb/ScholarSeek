import React, { useState } from 'react';
import type { SearchRequest } from '../types';

interface SearchFormProps {
  onSearch: (searchData: SearchRequest) => void;
  loading: boolean;
  outputOptions: string[];
  sortOptions: string[];
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, loading, outputOptions, sortOptions }) => {
  const [formData, setFormData] = useState<SearchRequest>({
    searchterm: '',
    mode: 'overview',
    searchnumber: 10,
    sortby: 'relevance',
    email: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(formData);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev: SearchRequest) => ({
      ...prev,
      [name]: name === 'searchnumber' ? parseInt(value) : value,
    }));
  };

  return (
    <div className="search-section">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="form-group">
          <label htmlFor="searchterm">Search Term</label>
          <input
            type="text"
            id="searchterm"
            name="searchterm"
            value={formData.searchterm}
            onChange={handleInputChange}
            placeholder="e.g., cancer immunotherapy"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="mode">Output Mode</label>
            <select
              id="mode"
              name="mode"
              value={formData.mode}
              onChange={handleInputChange}
            >
              {outputOptions.map(option => (
                <option key={option} value={option}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="searchnumber">Number of Results</label>
            <input
              type="number"
              id="searchnumber"
              name="searchnumber"
              value={formData.searchnumber}
              onChange={handleInputChange}
              min="1"
              max="100"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="sortby">Sort By</label>
            <select
              id="sortby"
              name="sortby"
              value={formData.sortby}
              onChange={handleInputChange}
            >
              {sortOptions.map(option => (
                <option key={option} value={option}>
                  {option.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button type="submit" className="search-btn" disabled={loading}>
          <span className="btn-text">
            {loading ? 'Searching...' : 'Search PubMed'}
          </span>
          {loading && <span className="loading-spinner">⏳</span>}
        </button>
      </form>
    </div>
  );
};

export default SearchForm;