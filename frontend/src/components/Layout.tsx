import React from 'react';
import Header from './Header';
import Footer from './Footer';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="app-layout" style={{
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100vh',
            backgroundColor: 'var(--color-background)'
        }}>
            <Header />
            <main className="main-content" style={{
                flex: 1,
                width: '100%',
                maxWidth: '1200px',
                margin: '0 auto',
                padding: 'var(--spacing-xl)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
            }}>
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
