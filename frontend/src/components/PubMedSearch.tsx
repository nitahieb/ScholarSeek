import React, { useState } from 'react';
import { SearchRequest, SearchResponse, OUTPUT_OPTIONS, SORT_OPTIONS } from '../types';
import { PubMedAPIService } from '../services/api';
import SearchForm from './SearchForm';
import SearchResults from './SearchResults';
import ErrorDisplay from './ErrorDisplay';
import './PubMedSearch.css';

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
    <div className="pubmed-search">
      <header className="header">
        <h1>🔬 PubMed Author Finder</h1>
        <p className="subtitle">Know a topic? Pull up articles. Meet authors. Make contact.</p>
      </header>

      <main className="main-content">
        <SearchForm 
          onSearch={handleSearch} 
          loading={loading}
          outputOptions={OUTPUT_OPTIONS}
          sortOptions={SORT_OPTIONS}
        />

        {error && <ErrorDisplay message={error} />}
        {results && <SearchResults results={results} />}
      </main>

      <footer className="footer">
        <p>
          Built with ❤️ using the PubMed Author Finder API |{' '}
          <a href="https://github.com/nitahieb/pubmed-author-finder" target="_blank" rel="noopener noreferrer">
            View on GitHub
          </a>
        </p>
      </footer>
    </div>
  );
};

export default PubMedSearch;