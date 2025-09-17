import React from 'react';

interface ErrorDisplayProps {
  message: string;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ message }) => {
  return (
    <div className="error-section">
      <h3>Error</h3>
      <p className="error-message">{message}</p>
    </div>
  );
};

export default ErrorDisplay;