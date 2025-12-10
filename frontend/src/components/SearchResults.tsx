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
        <div style={{
          textAlign: 'center',
          color: 'var(--color-text-muted)',
          padding: 'var(--spacing-xl)',
          fontStyle: 'italic'
        }}>
          No {results.mode === 'emails' ? 'author emails' : 'articles'} found for this search.
        </div>
      );
    }

    if (results.mode === 'emails') {
      return (
        <div style={{
          fontFamily: 'monospace',
          backgroundColor: 'var(--color-primary)',
          color: 'var(--color-text-inverted)',
          padding: 'var(--spacing-lg)',
          borderRadius: 'var(--radius-md)',
          lineHeight: '1.8',
          overflowX: 'auto',
          margin: 'var(--spacing-md) 0'
        }}>
          <strong>Author Emails Found:</strong><br />
          <div style={{ whiteSpace: 'pre-wrap' }}>{results.result}</div>
        </div>
      );
    } else {
      // Use react-markdown for overview results
      return (
        <div className="markdown-content" style={{ lineHeight: '1.7' }}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{results.result}</ReactMarkdown>
        </div>
      );
    }
  };

  return (
    <div className="card" style={{ padding: 'var(--spacing-xl)' }}>
      <h2 style={{
        borderBottom: '2px solid var(--color-border)',
        paddingBottom: 'var(--spacing-sm)',
        marginBottom: 'var(--spacing-lg)'
      }}>
        Results
      </h2>
      <div>
        {renderContent()}
      </div>
    </div>
  );
};

export default SearchResults;
