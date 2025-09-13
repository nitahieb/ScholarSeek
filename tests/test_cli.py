import pytest
from unittest.mock import patch, MagicMock
from cli import ParseArgs


class TestParseArgs:
    """Test the ParseArgs function."""

    def test_parse_args_default_values(self):
        """Test ParseArgs with minimal arguments (defaults)."""
        with patch('sys.argv', ['script', 'cancer']):
            args = ParseArgs()
            assert args.searchterm == 'cancer'
            assert args.mode == 'overview'
            assert args.email == ''
            assert args.searchnumber == 10
            assert args.sortby == 'relevance'

    def test_parse_args_all_arguments(self):
        """Test ParseArgs with all arguments specified."""
        test_args = [
            'script', 'diabetes',
            '--mode', 'emails',
            '--email', 'test@example.com',
            '--searchnumber', '25',
            '--sortby', 'pub_date'
        ]
        with patch('sys.argv', test_args):
            args = ParseArgs()
            assert args.searchterm == 'diabetes'
            assert args.mode == 'emails'
            assert args.email == 'test@example.com'
            assert args.searchnumber == 25
            assert args.sortby == 'pub_date'

    def test_parse_args_short_flags(self):
        """Test ParseArgs with short flag versions."""
        test_args = [
            'script', 'heart disease',
            '-m', 'overview',
            '-e', 'researcher@university.edu',
            '-n', '5',
            '-s', 'Author'
        ]
        with patch('sys.argv', test_args):
            args = ParseArgs()
            assert args.searchterm == 'heart disease'
            assert args.mode == 'overview'
            assert args.email == 'researcher@university.edu'
            assert args.searchnumber == 5
            assert args.sortby == 'Author'

    def test_parse_args_mode_choices(self):
        """Test ParseArgs mode argument choices."""
        # Test valid overview mode
        with patch('sys.argv', ['script', 'test', '-m', 'overview']):
            args = ParseArgs()
            assert args.mode == 'overview'

        # Test valid emails mode
        with patch('sys.argv', ['script', 'test', '-m', 'emails']):
            args = ParseArgs()
            assert args.mode == 'emails'

    def test_parse_args_invalid_mode(self):
        """Test ParseArgs with invalid mode choice."""
        with patch('sys.argv', ['script', 'test', '-m', 'invalid']):
            with pytest.raises(SystemExit):
                ParseArgs()

    def test_parse_args_sortby_choices(self):
        """Test ParseArgs sortby argument choices."""
        valid_sorts = ['relevance', 'pub_date', 'Author', 'JournalName']

        for sort_option in valid_sorts:
            with patch('sys.argv', ['script', 'test', '-s', sort_option]):
                args = ParseArgs()
                assert args.sortby == sort_option

    def test_parse_args_invalid_sortby(self):
        """Test ParseArgs with invalid sortby choice."""
        with patch('sys.argv', ['script', 'test', '-s', 'invalid_sort']):
            with pytest.raises(SystemExit):
                ParseArgs()

    def test_parse_args_searchnumber_integer(self):
        """Test ParseArgs searchnumber argument type conversion."""
        with patch('sys.argv', ['script', 'test', '-n', '100']):
            args = ParseArgs()
            assert args.searchnumber == 100
            assert isinstance(args.searchnumber, int)

    def test_parse_args_invalid_searchnumber(self):
        """Test ParseArgs with invalid searchnumber (non-integer)."""
        with patch('sys.argv', ['script', 'test', '-n', 'not_a_number']):
            with pytest.raises(SystemExit):
                ParseArgs()

    def test_parse_args_complex_search_term(self):
        """Test ParseArgs with complex search terms."""
        complex_terms = [
            'cancer AND therapy',
            '"machine learning"',
            'covid-19 OR coronavirus',
            'diabetes type 2'
        ]

        for term in complex_terms:
            with patch('sys.argv', ['script', term]):
                args = ParseArgs()
                assert args.searchterm == term

    def test_parse_args_missing_required_argument(self):
        """Test ParseArgs with missing required searchterm."""
        with patch('sys.argv', ['script']):
            with pytest.raises(SystemExit):
                ParseArgs()

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_parser_configuration(self, mock_parse_args):
        """Test that the argument parser is configured correctly."""
        mock_parse_args.return_value = MagicMock(
            searchterm='test',
            mode='overview',
            email='',
            searchnumber=10,
            sortby='relevance'
        )

        # Call ParseArgs to verify parser creation
        ParseArgs()

        # Verify parse_args was called
        mock_parse_args.assert_called_once()

    def test_parse_args_email_empty_string_default(self):
        """Test that email defaults to empty string."""
        with patch('sys.argv', ['script', 'test']):
            args = ParseArgs()
            assert args.email == ''
            assert isinstance(args.email, str)

    def test_parse_args_help_message(self):
        """Test ParseArgs help functionality."""
        with patch('sys.argv', ['script', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                ParseArgs()
            # Help should exit with code 0
            assert exc_info.value.code == 0
