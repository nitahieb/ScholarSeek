import React from 'react';
import { SearchResponse } from '../types';

interface SearchResultsProps {
  results: SearchResponse;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  const convertMarkdownToHTML = (markdown: string): string => {
    let html = markdown;
    
    // Convert headers
    html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
    
    // Convert bold text
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
    
    // Convert tables
    html = convertMarkdownTables(html);
    
    // Convert line breaks
    html = html.replace(/\n/g, '<br>');
    
    // Convert horizontal rules
    html = html.replace(/^---$/gm, '<hr>');
    
    return html;
  };

  const convertMarkdownTables = (html: string): string => {
    const lines = html.split('\n');
    let inTable = false;
    let result: string[] = [];
    let tableRows: string[][] = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      if (line.startsWith('|') && line.endsWith('|')) {
        if (!inTable) {
          inTable = true;
          tableRows = [];
        }
        
        // Check if this is a separator line
        if (line.match(/^\|[\s\-|]+\|$/)) {
          // Skip separator line
          continue;
        }
        
        const cells = line.split('|').slice(1, -1).map(cell => cell.trim());
        tableRows.push(cells);
      } else {
        if (inTable) {
          // End of table, convert to HTML
          if (tableRows.length > 0) {
            let tableHtml = '<table>';
            tableRows.forEach((row, index) => {
              const tag = index === 0 ? 'th' : 'td';
              tableHtml += '<tr>';
              row.forEach(cell => {
                tableHtml += `<${tag}>${cell}</${tag}>`;
              });
              tableHtml += '</tr>';
            });
            tableHtml += '</table>';
            result.push(tableHtml);
          }
          inTable = false;
          tableRows = [];
        }
        result.push(line);
      }
    }
    
    // Handle table at end of content
    if (inTable && tableRows.length > 0) {
      let tableHtml = '<table>';
      tableRows.forEach((row, index) => {
        const tag = index === 0 ? 'th' : 'td';
        tableHtml += '<tr>';
        row.forEach(cell => {
          tableHtml += `<${tag}>${cell}</${tag}>`;
        });
        tableHtml += '</tr>';
      });
      tableHtml += '</table>';
      result.push(tableHtml);
    }
    
    return result.join('\n');
  };

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
          <div dangerouslySetInnerHTML={{ __html: results.result.replace(/\n/g, '<br>') }} />
        </div>
      );
    } else {
      // Overview results with markdown formatting
      const htmlContent = convertMarkdownToHTML(results.result);
      return (
        <div 
          className="overview-results"
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
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