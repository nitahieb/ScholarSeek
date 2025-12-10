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
    <form onSubmit={handleSubmit}>
      <div className="input-group">
        <label className="input-label" htmlFor="searchterm">Search Term</label>
        <input
          className="input-field"
          type="text"
          id="searchterm"
          name="searchterm"
          value={formData.searchterm}
          onChange={handleInputChange}
          placeholder="e.g., cancer immunotherapy"
          required
        />
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: 'var(--spacing-md)',
        marginBottom: 'var(--spacing-lg)'
      }}>
        <div className="input-group" style={{ marginBottom: 0 }}>
          <label className="input-label" htmlFor="mode">Output Mode</label>
          <select
            className="input-field"
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

        <div className="input-group" style={{ marginBottom: 0 }}>
          <label className="input-label" htmlFor="searchnumber">Number of Results</label>
          <input
            className="input-field"
            type="number"
            id="searchnumber"
            name="searchnumber"
            value={formData.searchnumber}
            onChange={handleInputChange}
            min="1"
            max="100"
          />
        </div>

        <div className="input-group" style={{ marginBottom: 0 }}>
          <label className="input-label" htmlFor="sortby">Sort By</label>
          <select
            className="input-field"
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

      <button
        type="submit"
        className="btn btn-primary"
        disabled={loading}
        style={{ width: '100%' }}
      >
        {loading ? (
          <>
            <span className="loading-spinner"></span>
            Searching...
          </>
        ) : 'Search PubMed'}
      </button>
    </form>
  );
};

export default SearchForm;
