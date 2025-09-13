from unittest.mock import MagicMock
from format import overviewFormat, emailFormat


class TestOverviewFormat:
    """Test the overviewFormat function."""

    def test_overview_format_empty_list(self):
        """Test overviewFormat with empty article list."""
        result = overviewFormat([])
        assert result == ""

    def test_overview_format_single_article(self):
        """Test overviewFormat with a single article."""
        # Create a mock article
        mock_article = MagicMock()
        mock_article.title = "Test Article"
        mock_article.pmid = "12345"
        mock_article.language = "EN"
        mock_article.date = "2023-01-01"
        mock_article.emails = {"test@example.com"}

        # Create mock person
        mock_person = MagicMock()
        mock_person.firstName = "John"
        mock_person.lastName = "Doe"
        mock_person.affiliation = "Test University"
        mock_article.people = [mock_person]

        result = overviewFormat([mock_article])

        assert "Test Article" in result
        assert "12345" in result
        assert "EN" in result
        assert "2023-01-01" in result
        assert "test@example.com" in result
        assert "John Doe" in result
        assert "Test University" in result
        assert "##  Article Overview" in result
        assert "| Author | Affiliation |" in result

    def test_overview_format_multiple_articles(self):
        """Test overviewFormat with multiple articles."""
        # Create mock articles
        mock_article1 = MagicMock()
        mock_article1.title = "First Article"
        mock_article1.pmid = "11111"
        mock_article1.language = "EN"
        mock_article1.date = "2023-01-01"
        mock_article1.emails = {"first@example.com"}
        mock_article1.people = []

        mock_article2 = MagicMock()
        mock_article2.title = "Second Article"
        mock_article2.pmid = "22222"
        mock_article2.language = "ES"
        mock_article2.date = "2023-02-01"
        mock_article2.emails = {"second@example.com"}
        mock_article2.people = []

        result = overviewFormat([mock_article1, mock_article2])

        assert "First Article" in result
        assert "Second Article" in result
        assert "11111" in result
        assert "22222" in result
        assert "first@example.com" in result
        assert "second@example.com" in result

    def test_overview_format_no_emails(self):
        """Test overviewFormat with article that has no emails."""
        mock_article = MagicMock()
        mock_article.title = "No Email Article"
        mock_article.pmid = "99999"
        mock_article.language = "EN"
        mock_article.date = "2023-01-01"
        mock_article.emails = set()  # Empty set
        mock_article.people = []

        result = overviewFormat([mock_article])

        assert "No Email Article" in result
        assert "**Emails:**" not in result  # Should not show emails section

    def test_overview_format_multiple_people(self):
        """Test overviewFormat with multiple authors."""
        mock_article = MagicMock()
        mock_article.title = "Multi Author Article"
        mock_article.pmid = "55555"
        mock_article.language = "EN"
        mock_article.date = "2023-01-01"
        mock_article.emails = set()

        # Create multiple mock people
        person1 = MagicMock()
        person1.firstName = "John"
        person1.lastName = "Doe"
        person1.affiliation = "University A"

        person2 = MagicMock()
        person2.firstName = "Jane"
        person2.lastName = "Smith"
        person2.affiliation = "University B"

        mock_article.people = [person1, person2]

        result = overviewFormat([mock_article])

        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "University A" in result
        assert "University B" in result


class TestEmailFormat:
    """Test the emailFormat function."""

    def test_email_format_empty_set(self):
        """Test emailFormat with empty email set."""
        result = emailFormat(set())
        assert result == ""

    def test_email_format_single_email(self):
        """Test emailFormat with single email."""
        emails = {"test@example.com"}
        result = emailFormat(emails)
        assert result == "test@example.com"

    def test_email_format_multiple_emails(self):
        """Test emailFormat with multiple emails."""
        emails = {"first@example.com", "second@example.com", "third@example.com"}
        result = emailFormat(emails)

        # Since sets are unordered, we check that all emails are present
        assert "first@example.com" in result
        assert "second@example.com" in result
        assert "third@example.com" in result
        assert result.count(",") == 2  # Two commas for three emails

    def test_email_format_empty_list(self):
        """Test emailFormat with empty list."""
        result = emailFormat([])
        assert result == ""

    def test_email_format_list_input(self):
        """Test emailFormat with list input."""
        emails = ["test1@example.com", "test2@example.com"]
        result = emailFormat(emails)
        assert "test1@example.com" in result
        assert "test2@example.com" in result
        assert "," in result
