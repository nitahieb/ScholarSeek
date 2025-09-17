import Header from "../components/Header";
import Footer from "../components/Footer";
import PubMedSearch from "../components/PubMedSearch";

function Home() {
  return (
    <div className="pubmed-search">
      <Header />
      <main className="main-content">
        <PubMedSearch />
      </main>
      <Footer />
    </div>
  );
}

export default Home;