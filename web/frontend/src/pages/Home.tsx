import Header from "../components/Header";
import Footer from "../components/Footer";
import PubMedSearch from "../components/PubMedSearch";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/logout");
  };

  return (
    <div className="pubmed-search">
      <div className="logout-bar">
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>
      <Header />
      <main className="main-content">
        <PubMedSearch />
      </main>
      <Footer />
    </div>
  );
}

export default Home;