import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Header: React.FC = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access_token");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <header className="header" style={{
      backgroundColor: 'var(--color-surface)',
      borderBottom: '1px solid var(--color-border)',
      padding: 'var(--spacing-md) 0',
      boxShadow: 'var(--shadow-sm)',
      width: '100%'
    }}>
      <div className="header-container" style={{
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 var(--spacing-xl)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Link to="/" className="logo" style={{
          fontFamily: 'var(--font-serif)',
          fontWeight: 700,
          fontSize: '1.5rem',
          color: 'var(--color-primary)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          textDecoration: 'none'
        }}>
          <span style={{ fontSize: '1.8rem' }}>🔬</span> ScholarSeek
        </Link>

        <nav className="nav-links">
          {isLoggedIn ? (
            <button
              onClick={handleLogout}
              className="btn btn-secondary"
              style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
            >
              Logout
            </button>
          ) : (
            <div style={{ display: 'flex', gap: 'var(--spacing-md)' }}>
              <Link to="/login" className="btn btn-secondary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', textDecoration: 'none' }}>Login</Link>
              <Link to="/register" className="btn btn-primary" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', textDecoration: 'none', color: 'white' }}>Register</Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
