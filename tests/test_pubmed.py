import pytest
from unittest.mock import MagicMock, patch
from pipeline import Pipeline
from article import ArticleRecord, ArticleResult
from analyzer import ArticleAnalyzer
from researcher import Researcher

# ---------- Pipeline Tests ----------
@patch("pipeline.Conduit")
def test_pipeline_add_search(mock_conduit):
    mock_pipeline = MagicMock()
    mock_conduit.return_value.new_pipeline.return_value = mock_pipeline
    pl = Pipeline(email="test@example.com")
    pl.addSearch("cancer")
    mock_pipeline.add_search.assert_called_once()

@patch("pipeline.Conduit")
def test_pipeline_add_fetch(mock_conduit):
    mock_pipeline = MagicMock()
    mock_conduit.return_value.new_pipeline.return_value = mock_pipeline
    pl = Pipeline(email="test@example.com")
    pl.searchID = "search123"
    pl.addFetch()
    mock_pipeline.add_fetch.assert_called_once()

@patch("pipeline.Conduit")
def test_pipeline_get_results_fetch(mock_conduit):
    mock_pipeline = MagicMock()
    mock_conduit.return_value.new_pipeline.return_value = mock_pipeline
    pl = Pipeline(email="test@example.com")
    pl.fetchID = "fetch123"
    result_mock = "result"
    mock_conduit.return_value.get_result.return_value = result_mock
    output = pl.getResults()
    mock_conduit.return_value.run.assert_called_once_with(mock_pipeline)
    assert output == result_mock

# ---------- Article Tests ----------
def test_article_record_repr():
    rec = ArticleRecord("Title", "EN", "2023-01-01", {"a@b.com"}, [], "123")
    rep = repr(rec)
    assert "Title" in rep and "EN" in rep

def test_article_result_methods():
    result = ArticleResult(response=None, request=MagicMock())
    assert result.isEmpty() == True
    result.add_article_record(ArticleRecord("T", "EN", "2023", set(), [], "1"))
    assert result.isEmpty() == False
    assert result.size() == 1

# ---------- Researcher Tests ----------
def test_researcher_repr():
    r = Researcher("Doe", "John", "JD", "Univ", "j@u.com")
    rep = repr(r)
    assert "John" in rep and "Doe" in rep

# ---------- ArticleAnalyzer Tests ----------
def test_analyzer_parsing():
    sample_xml = b"""
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <PMID>123</PMID>
          <Article>
            <ArticleTitle>Sample Title</ArticleTitle>
            <Language>EN</Language>
            <AuthorList>
              <Author>
                <LastName>Doe</LastName>
                <ForeName>John</ForeName>
                <Initials>JD</Initials>
                <Affiliation>Department of Testing, test@example.com</Affiliation>
              </Author>
            </AuthorList>
            <Journal>
              <JournalIssue>
                <PubDate>
                  <Year>2023</Year>
                  <Month>01</Month>
                  <Day>02</Day>
                </PubDate>
              </JournalIssue>
            </Journal>
          </Article>
        </MedlineCitation>
      </PubmedArticle>
    </PubmedArticleSet>
    """
    analyzer = ArticleAnalyzer()
    request_mock = MagicMock()
    request_mock.eutil = "efetch"
    request_mock.query_id = "q1"
    request_mock.db = "pubmed"
    response_mock = MagicMock()
    response_mock.getvalue.return_value = sample_xml
    analyzer.analyze_result(response_mock, request_mock)
    
    result = analyzer.result
    assert result.size() == 1
    article = result.articles[0]
    assert article.title == "Sample Title"
    assert "test@example.com" in article.emails
    assert article.pmid == "123"
