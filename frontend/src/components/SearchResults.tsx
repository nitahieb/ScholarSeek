import React from 'react';
import type { SearchResponse } from '../types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'

interface SearchResultsProps {
  results: SearchResponse;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  const renderContent = () => {
    if (!results.result || !results.result.trim()) {
      return (
        <div className="no-results">
          <em>No {results.mode === 'emails' ? 'author emails' : 'articles'} found for this search.</em>
        </div>
      );
    }

    if (results.mode === 'emails') {
      return (
        <div className="email-results">
          <strong>Author Emails Found:</strong><br />
          <div>{results.result}</div>
        </div>
      );
    } else {
      // Use react-markdown for overview results
      return (
        <div className="overview-results">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{results.result}</ReactMarkdown>
        </div>
      );
    }
  };

  return (
    <div className="results-section">
      <h2>Results</h2>
      <div className="results-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default SearchResults;