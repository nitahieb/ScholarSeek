from unittest.mock import patch, MagicMock
from services import getSummary, getEmails


class TestGetSummary:
    """Test the getSummary service function."""

    @patch('services.overviewFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_summary_basic_flow(
        self, mock_analyzer_class, mock_pipeline_class, mock_overview_format
    ):
        """Test basic getSummary flow with mocked dependencies."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        mock_results = MagicMock()
        mock_results.articles = [MagicMock(), MagicMock()]
        mock_pipeline.getResults.return_value = mock_results

        mock_overview_format.return_value = "formatted overview"

        # Call function
        result = getSummary("cancer", "relevance", "test@email.com", 10)

        # Verify calls
        mock_pipeline_class.assert_called_once_with("test@email.com")
        mock_pipeline.addSearch.assert_called_once_with("cancer", retmax=10, sortBy="relevance")
        mock_analyzer_class.assert_called_once()
        mock_pipeline.addFetch.assert_called_once_with(analyzer=mock_analyzer)
        mock_pipeline.getResults.assert_called_once()
        mock_overview_format.assert_called_once_with(mock_results.articles)

        assert result == "formatted overview"

    @patch('services.overviewFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_summary_different_parameters(
        self, mock_analyzer_class, mock_pipeline_class, mock_overview_format
    ):
        """Test getSummary with different parameter values and no results."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        mock_results = MagicMock()
        mock_results.articles = []
        mock_pipeline.getResults.return_value = mock_results

        # Call function with different parameters
        result = getSummary("diabetes", "pub_date", "researcher@university.edu", 25)

        # Verify calls with new parameters
        mock_pipeline_class.assert_called_once_with("researcher@university.edu")
        mock_pipeline.addSearch.assert_called_once_with("diabetes", retmax=25, sortBy="pub_date")
        mock_analyzer_class.assert_called_once()
        mock_pipeline.addFetch.assert_called_once_with(analyzer=mock_analyzer)
        mock_pipeline.getResults.assert_called_once()
        mock_overview_format.assert_not_called()

        assert result == "No articles found for your search."


class TestGetEmails:
    """Test the getEmails service function."""

    @patch('services.emailFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_emails_basic_flow(
        self, mock_analyzer_class, mock_pipeline_class, mock_email_format
    ):
        """Test basic getEmails flow with mocked dependencies."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        # Create mock articles with emails
        mock_article1 = MagicMock()
        mock_article1.emails = {"author1@example.com", "author2@example.com"}

        mock_article2 = MagicMock()
        mock_article2.emails = {"author3@example.com"}

        mock_results = MagicMock()
        mock_results.articles = [mock_article1, mock_article2]
        mock_pipeline.getResults.return_value = mock_results

        expected_return = (
            "author1@example.com, author2@example.com, author3@example.com"
        )
        mock_email_format.return_value = expected_return

        # Call function
        result = getEmails("cancer", "relevance", "test@email.com", 10)

        # Verify calls
        mock_pipeline_class.assert_called_once_with("test@email.com")
        mock_pipeline.addSearch.assert_called_once_with("cancer", retmax=10, sortBy="relevance")
        mock_analyzer_class.assert_called_once()
        mock_pipeline.addFetch.assert_called_once_with(analyzer=mock_analyzer)
        mock_pipeline.getResults.assert_called_once()

        # Verify email collection and formatting
        expected_emails = {"author1@example.com", "author2@example.com", "author3@example.com"}
        mock_email_format.assert_called_once_with(expected_emails)

        assert result == expected_return

    @patch('services.emailFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_emails_no_emails(
        self, mock_analyzer_class, mock_pipeline_class, mock_email_format
    ):
        """Test getEmails when articles have no emails."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        # Create mock articles with no emails
        mock_article1 = MagicMock()
        mock_article1.emails = set()

        mock_article2 = MagicMock()
        mock_article2.emails = set()

        mock_results = MagicMock()
        mock_results.articles = [mock_article1, mock_article2]
        mock_pipeline.getResults.return_value = mock_results

        mock_email_format.return_value = ""

        # Call function
        result = getEmails("test", "relevance", "test@email.com", 5)

        # Verify empty email set is passed to formatter
        mock_email_format.assert_called_once_with(set())

        assert result == ""

    @patch('services.emailFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_emails_duplicate_emails(
        self, mock_analyzer_class, mock_pipeline_class, mock_email_format
    ):
        """Test getEmails with duplicate emails across articles."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        # Create mock articles with overlapping emails
        mock_article1 = MagicMock()
        mock_article1.emails = {"same@example.com", "unique1@example.com"}

        mock_article2 = MagicMock()
        mock_article2.emails = {"same@example.com", "unique2@example.com"}

        mock_results = MagicMock()
        mock_results.articles = [mock_article1, mock_article2]
        mock_pipeline.getResults.return_value = mock_results

        mock_email_format.return_value = "unique emails"

        # Call function
        result = getEmails("test", "relevance", "test@email.com", 5)

        # Verify unique emails are collected
        expected_emails = {"same@example.com", "unique1@example.com", "unique2@example.com"}
        mock_email_format.assert_called_once_with(expected_emails)

        assert result == "unique emails"

    @patch('services.emailFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_emails_empty_articles(
        self, mock_analyzer_class, mock_pipeline_class, mock_email_format
    ):
        """Test getEmails when no articles are returned."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        mock_results = MagicMock()
        mock_results.articles = []
        mock_pipeline.getResults.return_value = mock_results

        mock_email_format.return_value = ""

        # Call function
        result = getEmails("obscure term", "relevance", "test@email.com", 10)


        assert result == "No articles found — no emails to display."

    @patch('services.emailFormat')
    @patch('services.Pipeline')
    @patch('services.ArticleAnalyzer')
    def test_get_emails_different_parameters(
        self, mock_analyzer_class, mock_pipeline_class, mock_email_format
    ):
        """Test getEmails with different parameter values."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline_class.return_value = mock_pipeline

        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer

        # Create mock articles with emails for this parameter set
        mock_article1 = MagicMock()
        mock_article1.emails = {"authorA@university.edu", "authorB@institute.org"}

        mock_article2 = MagicMock()
        mock_article2.emails = {"authorC@hospital.net"}

        mock_results = MagicMock()
        mock_results.articles = [mock_article1, mock_article2]
        mock_pipeline.getResults.return_value = mock_results

        expected_emails = {"authorA@university.edu", "authorB@institute.org", "authorC@hospital.net"}
        mock_email_format.return_value = "authorA@university.edu, authorB@institute.org, authorC@hospital.net"

        # Call function with different parameters
        result = getEmails("heart disease", "Author", "doctor@hospital.org", 50)

        # Verify calls with new parameters
        mock_pipeline_class.assert_called_once_with("doctor@hospital.org")
        mock_pipeline.addSearch.assert_called_once_with("heart disease", retmax=50, sortBy="Author")
        mock_email_format.assert_called_once_with(expected_emails)

        assert result == "authorA@university.edu, authorB@institute.org, authorC@hospital.net"
