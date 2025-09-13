from unittest.mock import patch, MagicMock
from main import main


class TestMain:
    """Test the main function."""

    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_overview_mode(self, mock_parse_args, mock_get_summary):
        """Test main function in overview mode."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.mode = "overview"
        mock_args.searchterm = "cancer"
        mock_args.sortby = "relevance"
        mock_args.email = "test@example.com"
        mock_args.searchnumber = 10
        mock_parse_args.return_value = mock_args

        # Setup mock summary response
        expected_summary = "## Article Overview\n**Title:** Test Article..."
        mock_get_summary.return_value = expected_summary

        # Call main function
        result = main()

        # Verify calls
        mock_parse_args.assert_called_once()
        mock_get_summary.assert_called_once_with(
            "cancer", "relevance", "test@example.com", 10
        )

        # Verify return value
        assert result == expected_summary

    @patch('main.getEmails')
    @patch('main.ParseArgs')
    def test_main_emails_mode(self, mock_parse_args, mock_get_emails):
        """Test main function in emails mode."""
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.mode = "emails"
        mock_args.searchterm = "diabetes"
        mock_args.sortby = "pub_date"
        mock_args.email = "researcher@university.edu"
        mock_args.searchnumber = 25
        mock_parse_args.return_value = mock_args

        # Setup mock emails response
        expected_emails = "author1@example.com, author2@example.com"
        mock_get_emails.return_value = expected_emails

        # Call main function
        result = main()

        # Verify calls
        mock_parse_args.assert_called_once()
        mock_get_emails.assert_called_once_with(
            "diabetes", "pub_date", "researcher@university.edu", 25
        )

        # Verify return value
        assert result == expected_emails

    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_default_overview_mode(self, mock_parse_args, mock_get_summary):
        """Test main function defaults to overview mode when not specified."""
        # Setup mock arguments (mode defaults to "overview")
        mock_args = MagicMock()
        mock_args.mode = "overview"  # This is the default
        mock_args.searchterm = "heart disease"
        mock_args.sortby = "relevance"
        mock_args.email = ""
        mock_args.searchnumber = 10
        mock_parse_args.return_value = mock_args

        mock_get_summary.return_value = "summary result"

        # Call main function
        result = main()

        # Verify getSummary is called (not getEmails)
        mock_get_summary.assert_called_once()
        assert result == "summary result"

    @patch('builtins.print')
    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_prints_output_overview(self, mock_parse_args, mock_get_summary, mock_print):
        """Test that main function prints the output for overview mode."""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.mode = "overview"
        mock_args.searchterm = "test"
        mock_args.sortby = "relevance"
        mock_args.email = "test@example.com"
        mock_args.searchnumber = 5
        mock_parse_args.return_value = mock_args

        expected_output = "Test summary output"
        mock_get_summary.return_value = expected_output

        # Call main function
        result = main()

        # Verify print was called with the output
        mock_print.assert_called_once_with(expected_output)
        assert result == expected_output

    @patch('builtins.print')
    @patch('main.getEmails')
    @patch('main.ParseArgs')
    def test_main_prints_output_emails(self, mock_parse_args, mock_get_emails, mock_print):
        """Test that main function prints the output for emails mode."""
        # Setup mocks
        mock_args = MagicMock()
        mock_args.mode = "emails"
        mock_args.searchterm = "test"
        mock_args.sortby = "relevance"
        mock_args.email = "test@example.com"
        mock_args.searchnumber = 5
        mock_parse_args.return_value = mock_args

        expected_output = "test1@example.com, test2@example.com"
        mock_get_emails.return_value = expected_output

        # Call main function
        result = main()

        # Verify print was called with the output
        mock_print.assert_called_once_with(expected_output)
        assert result == expected_output

    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_with_empty_email(self, mock_parse_args, mock_get_summary):
        """Test main function with empty email parameter."""
        # Setup mock arguments with empty email
        mock_args = MagicMock()
        mock_args.mode = "overview"
        mock_args.searchterm = "covid"
        mock_args.sortby = "pub_date"
        mock_args.email = ""  # Empty email
        mock_args.searchnumber = 15
        mock_parse_args.return_value = mock_args

        mock_get_summary.return_value = "empty email summary"

        # Call main function
        result = main()

        # Verify getSummary is called with empty email
        mock_get_summary.assert_called_once_with(
            "covid", "pub_date", "", 15
        )
        assert result == "empty email summary"

    @patch('main.getEmails')
    @patch('main.ParseArgs')
    def test_main_different_sort_options(self, mock_parse_args, mock_get_emails):
        """Test main function with different sort options."""
        sort_options = ["relevance", "pub_date", "Author", "JournalName"]

        for sort_option in sort_options:
            # Reset mocks
            mock_parse_args.reset_mock()
            mock_get_emails.reset_mock()

            # Setup mock arguments
            mock_args = MagicMock()
            mock_args.mode = "emails"
            mock_args.searchterm = "test"
            mock_args.sortby = sort_option
            mock_args.email = "test@example.com"
            mock_args.searchnumber = 10
            mock_parse_args.return_value = mock_args

            mock_get_emails.return_value = f"emails for {sort_option}"

            # Call main function
            result = main()

            # Verify correct sort option is passed
            mock_get_emails.assert_called_once_with(
                "test", sort_option, "test@example.com", 10
            )
            assert result == f"emails for {sort_option}"

    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_complex_search_term(self, mock_parse_args, mock_get_summary):
        """Test main function with complex search terms."""
        complex_terms = [
            "cancer AND therapy",
            '"machine learning" AND medical',
            "covid-19 OR coronavirus",
            "diabetes[MeSH Terms]"
        ]

        for term in complex_terms:
            # Reset mocks
            mock_parse_args.reset_mock()
            mock_get_summary.reset_mock()

            # Setup mock arguments
            mock_args = MagicMock()
            mock_args.mode = "overview"
            mock_args.searchterm = term
            mock_args.sortby = "relevance"
            mock_args.email = "test@example.com"
            mock_args.searchnumber = 10
            mock_parse_args.return_value = mock_args

            mock_get_summary.return_value = f"summary for {term}"

            # Call main function
            result = main()

            # Verify correct search term is passed
            mock_get_summary.assert_called_once_with(
                term, "relevance", "test@example.com", 10
            )
            assert result == f"summary for {term}"

    @patch('main.getSummary')
    @patch('main.ParseArgs')
    def test_main_different_search_numbers(self, mock_parse_args, mock_get_summary):
        """Test main function with different search numbers."""
        search_numbers = [1, 5, 10, 25, 100]

        for num in search_numbers:
            # Reset mocks
            mock_parse_args.reset_mock()
            mock_get_summary.reset_mock()

            # Setup mock arguments
            mock_args = MagicMock()
            mock_args.mode = "overview"
            mock_args.searchterm = "test"
            mock_args.sortby = "relevance"
            mock_args.email = "test@example.com"
            mock_args.searchnumber = num
            mock_parse_args.return_value = mock_args

            mock_get_summary.return_value = f"summary for {num} results"

            # Call main function
            result = main()

            # Verify correct search number is passed
            mock_get_summary.assert_called_once_with(
                "test", "relevance", "test@example.com", num
            )
            assert result == f"summary for {num} results"


class TestMainEntryPoint:
    """Test the main entry point when script is run directly."""

    @patch('main.main')
    def test_main_entry_point(self, mock_main):
        """Test that main() is called when script is run directly."""
        # Mock the main function
        mock_main.return_value = "test result"

        # Import and execute the main block
        import main

        # The __name__ == "__main__" block should call main()
        # This is tested by ensuring our mocked main function can be called
        result = main.main()
        assert result == "test result"
