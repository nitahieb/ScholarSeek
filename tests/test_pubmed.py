import pytest
from unittest.mock import MagicMock, patch
from pipeline import Pipeline
from article import ArticleRecord, ArticleResult
from analyzer import ArticleAnalyzer
from researcher import Researcher
from parsing import (
    parse_xml,
    extract_basics,
    extract_publish_date,
    extract_authors_and_emails,
)

# ---------- Fixtures ----------

@pytest.fixture
def pipeline_with_mock():
    with patch("pipeline.Conduit") as mock_conduit:
        mock_pipeline = MagicMock()
        mock_conduit.return_value.new_pipeline.return_value = mock_pipeline
        yield Pipeline(email="test@example.com"), mock_pipeline, mock_conduit.return_value

# ---------- Pipeline Tests ----------

def test_pipeline_add_search(pipeline_with_mock):
    pl, mock_pipeline, _ = pipeline_with_mock
    pl.addSearch("cancer","relevance",10)
    mock_pipeline.add_search.assert_called_once()

def test_pipeline_add_fetch(pipeline_with_mock):
    pl, mock_pipeline, _ = pipeline_with_mock
    pl.searchID = "search123"
    pl.addFetch()
    mock_pipeline.add_fetch.assert_called_once()

def test_pipeline_get_results_fetch(pipeline_with_mock):
    pl, mock_pipeline, mock_conduit = pipeline_with_mock
    pl.fetchID = "fetch123"
    result_mock = "result"
    mock_conduit.get_result.return_value = result_mock

    output = pl.getResults()

    mock_conduit.run.assert_called_once_with(mock_pipeline)
    assert output == result_mock

# ---------- Article and Researcher Tests ----------

def test_article_record_repr():
    rec = ArticleRecord("Title", "EN", "2023-01-01", {"a@b.com"}, [], "123")
    rep = repr(rec)
    assert "Title" in rep and "EN" in rep

def test_article_result_methods():
    result = ArticleResult(response=None, request=MagicMock())
    assert result.isEmpty() is True

    result.add_article_record(ArticleRecord("T", "EN", "2023", set(), [], "1"))
    assert result.isEmpty() is False
    assert result.size() == 1

def test_researcher_repr():
    r = Researcher("Doe", "John", "JD", "Univ", "j@u.com")
    rep = repr(r)
    assert "John" in rep and "Doe" in rep

# ---------- Parsing Helpers Tests ----------

@pytest.fixture
def sample_article_xml():
    return b"""
    <PubmedArticle>
      <MedlineCitation>
        <PMID>123</PMID>
        <Article>
          <ArticleTitle>Sample Title</ArticleTitle>
          <Language>EN</Language>
          <Journal>
            <JournalIssue>
              <PubDate>
                <Year>2023</Year>
                <Month>01</Month>
                <Day>02</Day>
              </PubDate>
            </JournalIssue>
          </Journal>
          <AuthorList>
            <Author>
              <LastName>Doe</LastName>
              <ForeName>John</ForeName>
              <Initials>JD</Initials>
              <Affiliation>Dept of Testing, test@example.com</Affiliation>
            </Author>
          </AuthorList>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """

def test_parse_xml(sample_article_xml):
    class DummyResponse:
        def getvalue(self):
            return b"<PubmedArticleSet>" + sample_article_xml + b"</PubmedArticleSet>"

    root = parse_xml(DummyResponse())
    assert root.find(".//PMID").text == "123"

def test_extract_basics_and_publish_date(sample_article_xml):
    import lxml.etree as etree
    from io import BytesIO

    article = etree.fromstring(sample_article_xml)
    pmid, title, language = extract_basics(article)
    assert pmid == "123"
    assert title == "Sample Title"
    assert language == "EN"

    date = extract_publish_date(article)
    assert date == "2023-01-02"

@pytest.mark.parametrize("affiliation, expected_email", [
    ("No email here", None),
    ("Contact: someone@domain.com", "someone@domain.com"),
])
def test_extract_authors_and_emails_affiliations(sample_article_xml, affiliation, expected_email):
    import lxml.etree as etree
    article_xml = sample_article_xml.replace(
        b"Dept of Testing, test@example.com",
        affiliation.encode()
    )
    article = etree.fromstring(article_xml)
    emails, authors = extract_authors_and_emails(article)
    if expected_email:
        assert expected_email in emails
        assert authors[0].email == expected_email
    else:
        assert not emails
        assert authors[0].email is None

# ---------- Integration Test for ArticleAnalyzer ----------

def test_analyzer_parsing_integration(sample_article_xml):
    analyzer = ArticleAnalyzer()
    request = MagicMock()
    request.eutil = "efetch"
    request.query_id = "q1"
    request.db = "pubmed"

    class DummyResponse:
        def getvalue(self):
            return b"<PubmedArticleSet>" + sample_article_xml + b"</PubmedArticleSet>"

    response = DummyResponse()
    analyzer.analyze_result(response, request)
    result = analyzer.result
    assert result.size() == 1
    article = result.articles[0]
    assert article.title == "Sample Title"
    assert "test@example.com" in article.emails
    assert article.pmid == "123"
