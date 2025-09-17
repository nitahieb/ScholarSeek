import React from "react";
import "./PubMedSearch.css";

const Footer: React.FC = () => (
  <footer className="footer">
    <p>
      &copy; {new Date().getFullYear()} PubMed Author Finder &mdash; <a href="https://github.com/nitahieb/pubmed-author-finder">GitHub</a>
    </p>
  </footer>
);

export default Footer;