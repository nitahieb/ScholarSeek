import React, { useState } from 'react';
import { type SearchRequest, type SearchResponse, OUTPUT_OPTIONS, SORT_OPTIONS } from '../types';
import { PubMedAPIService } from '../services/api';
import SearchForm from './SearchForm';
import SearchResults from './SearchResults';
import ErrorDisplay from './ErrorDisplay';

const PubMedSearch: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (searchData: SearchRequest) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await PubMedAPIService.search(searchData);
      setResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: '100%', maxWidth: '800px' }}>
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <h2 style={{ marginBottom: 'var(--spacing-md)' }}>Search Articles</h2>
        <SearchForm
          onSearch={handleSearch}
          loading={loading}
          outputOptions={OUTPUT_OPTIONS}
          sortOptions={SORT_OPTIONS}
        />
      </div>

      {error && <ErrorDisplay message={error} />}
      {results && <SearchResults results={results} />}
    </div>
  );
};

export default PubMedSearch;
