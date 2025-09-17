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
      <Header />
      <main className="main-content">
        <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "10px" }}>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
        <PubMedSearch />
      </main>
      <Footer />
    </div>
  );
}

export default Home;