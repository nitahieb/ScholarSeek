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

# ---------- Additional ArticleAnalyzer Tests ----------

def test_analyzer_init_result():
    analyzer = ArticleAnalyzer()
    request = MagicMock()
    request.eutil = "efetch"
    request.query_id = "q1"
    request.db = "pubmed"

    response = MagicMock()

    # Test that result is None initially
    assert analyzer.result is None

    # Test init_result creates result
    analyzer.init_result(response, request)
    assert analyzer.result is not None
    assert isinstance(analyzer.result, ArticleResult)

    # Test init_result doesn't overwrite existing result
    original_result = analyzer.result
    analyzer.init_result(response, request)
    assert analyzer.result is original_result

def test_analyzer_analyze_error():
    analyzer = ArticleAnalyzer()
    request = MagicMock()
    request.dump.return_value = {"test": "data"}

    response = MagicMock()
    response.getvalue.return_value = "Error message"

    # Test that analyze_error prints JSON (we can't easily test print output,
    # but we can ensure it doesn't crash)
    try:
        analyzer.analyze_error(response, request)
    except Exception as e:
        pytest.fail(f"analyze_error raised an exception: {e}")

def test_analyzer_analyze_result_empty():
    analyzer = ArticleAnalyzer()
    request = MagicMock()
    request.eutil = "efetch"
    request.query_id = "q1"
    request.db = "pubmed"

    class EmptyResponse:
        def getvalue(self):
            return b"<PubmedArticleSet></PubmedArticleSet>"

    response = EmptyResponse()
    analyzer.analyze_result(response, request)

    assert analyzer.result is not None
    assert analyzer.result.size() == 0
    assert analyzer.result.isEmpty() is True

# ---------- Additional Pipeline Tests ----------

def test_pipeline_search_parameters():
    """Test Pipeline addSearch with various parameters"""
    with patch("pipeline.Conduit") as mock_conduit:
        mock_pipeline = MagicMock()
        mock_conduit.return_value.new_pipeline.return_value = mock_pipeline

        pl = Pipeline(email="test@example.com")
        pl.addSearch("cancer", "pub_date", 25, "pubmed", "uilist")

        expected_query = {
            "db": "pubmed",
            "term": "cancer",
            "retmax": 25,
            "rettype": "uilist",
            "sort": "pub_date"
        }
        mock_pipeline.add_search.assert_called_once_with(expected_query)

def test_pipeline_fetch_parameters():
    """Test Pipeline addFetch with various parameters"""
    with patch("pipeline.Conduit") as mock_conduit:
        mock_pipeline = MagicMock()
        mock_conduit.return_value.new_pipeline.return_value = mock_pipeline

        pl = Pipeline(email="test@example.com")
        pl.searchID = "search123"

        mock_analyzer = MagicMock()
        pl.addFetch(analyzer=mock_analyzer, db="pmc", retmode="json")

        expected_query = {"db": "pmc", "retmode": "json"}
        mock_pipeline.add_fetch.assert_called_once_with(
            expected_query, dependency="search123", analyzer=mock_analyzer
        )

def test_pipeline_get_results_search_only():
    """Test Pipeline getResults when only search is performed"""
    with patch("pipeline.Conduit") as mock_conduit:
        mock_pipeline = MagicMock()
        mock_conduit.return_value.new_pipeline.return_value = mock_pipeline

        pl = Pipeline(email="test@example.com")
        pl.searchID = "search123"
        # No fetchID set

        search_result = "search_result"
        mock_conduit.return_value.get_result.return_value = search_result

        output = pl.getResults()

        mock_conduit.return_value.run.assert_called_once_with(mock_pipeline)
        mock_conduit.return_value.get_result.assert_called_once_with("search123")
        assert output == search_result

# ---------- Additional Parsing Tests ----------

def test_extract_email_edge_cases():
    """Test extract_email with various edge cases"""
    from parsing import extract_email

    test_cases = [
        ("", None),
        (None, None),
        ("No email in this text", None),
        ("Contact: user@domain.com for more info", "user@domain.com"),
        ("Multiple emails: first@domain.com and second@domain.org", "first@domain.com"),
        ("Email with numbers: user123@domain456.com", "user123@domain456.com"),
        ("Email with dots: user.name@sub.domain.com", "user.name@sub.domain.com"),
        ("Email with dashes: user-name@domain-name.com", "user-name@domain-name.com"),
    ]

    for text, expected in test_cases:
        result = extract_email(text)
        assert result == expected

def test_extract_publish_date_edge_cases():
    """Test extract_publish_date with various date formats"""
    import lxml.etree as etree

    # Test with no PubDate element
    article_no_date = etree.fromstring(
        b"<PubmedArticle><MedlineCitation><Article></Article></MedlineCitation></PubmedArticle>"
    )
    date = extract_publish_date(article_no_date)
    assert date == ""

    # Test with only year
    article_year_only = etree.fromstring(b"""
    <PubmedArticle>
      <MedlineCitation>
        <Article>
          <Journal>
            <JournalIssue>
              <PubDate>
                <Year>2023</Year>
              </PubDate>
            </JournalIssue>
          </Journal>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """)
    date = extract_publish_date(article_year_only)
    assert date == "2023"

    # Test with year and month
    article_year_month = etree.fromstring(b"""
    <PubmedArticle>
      <MedlineCitation>
        <Article>
          <Journal>
            <JournalIssue>
              <PubDate>
                <Year>2023</Year>
                <Month>03</Month>
              </PubDate>
            </JournalIssue>
          </Journal>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """)
    date = extract_publish_date(article_year_month)
    assert date == "2023-03"

def test_extract_authors_no_authors():
    """Test extract_authors_and_emails with no authors"""
    import lxml.etree as etree

    article_no_authors = etree.fromstring(b"""
    <PubmedArticle>
      <MedlineCitation>
        <Article>
          <ArticleTitle>Title</ArticleTitle>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """)

    emails, authors = extract_authors_and_emails(article_no_authors)
    assert emails == set()
    assert authors == []

def test_extract_authors_incomplete_data():
    """Test extract_authors_and_emails with incomplete author data"""
    import lxml.etree as etree

    article_incomplete = etree.fromstring(b"""
    <PubmedArticle>
      <MedlineCitation>
        <Article>
          <AuthorList>
            <Author>
              <LastName>Doe</LastName>
              <!-- Missing ForeName and Initials -->
            </Author>
            <Author>
              <ForeName>Jane</ForeName>
              <!-- Missing LastName -->
            </Author>
          </AuthorList>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """)

    emails, authors = extract_authors_and_emails(article_incomplete)
    assert len(authors) == 2
    assert authors[0].lastName == "Doe"
    assert authors[0].firstName == ""
    assert authors[1].firstName == "Jane"
    assert authors[1].lastName == ""

# ---------- Additional Article Tests ----------

def test_article_result_dump():
    """Test ArticleResult dump method"""
    request = MagicMock()
    request.eutil = "efetch"
    request.query_id = "test_query"
    request.db = "pubmed"

    result = ArticleResult(None, request)
    article = ArticleRecord("Test", "EN", "2023", set(), [], "123")
    result.add_article_record(article)

    dump_data = result.dump()
    assert isinstance(dump_data, dict)
    assert result in dump_data
    assert "dump" in dump_data[result]
    assert dump_data[result]["dump"]["query_id"] == "test_query"
    assert dump_data[result]["dump"]["db"] == "pubmed"
    assert dump_data[result]["dump"]["eutil"] == "efetch"

def test_article_result_get_link_parameter():
    """Test ArticleResult get_link_parameter method"""
    request = MagicMock()
    request.eutil = "efetch"
    request.query_id = "test_query"
    request.db = "pubmed"

    result = ArticleResult(None, request)
    link_params = result.get_link_parameter()
    assert link_params == {}

# ---------- Additional Researcher Tests ----------

def test_researcher_empty_initialization():
    """Test Researcher with no parameters"""
    r = Researcher()
    assert r.firstName == ""
    assert r.lastName == ""
    assert r.initials == ""
    assert r.affiliation == ""
    assert r.email == ""

def test_researcher_partial_initialization():
    """Test Researcher with partial parameters"""
    r = Researcher(lastName="Smith", firstName="John")
    assert r.lastName == "Smith"
    assert r.firstName == "John"
    assert r.initials == ""
    assert r.affiliation == ""
    assert r.email == ""

def test_researcher_full_initialization():
    """Test Researcher with all parameters"""
    r = Researcher(
        lastName="Johnson",
        firstName="Alice",
        initials="AJ",
        affiliation="MIT",
        email="alice@mit.edu"
    )
    assert r.lastName == "Johnson"
    assert r.firstName == "Alice"
    assert r.initials == "AJ"
    assert r.affiliation == "MIT"
    assert r.email == "alice@mit.edu"
