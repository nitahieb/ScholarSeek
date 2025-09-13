from constants import PUBMED_SORT_OPTIONS, APPLICATION_OUTPUT_OPTIONS


def test_pubmed_sort_options():
    """Test that PUBMED_SORT_OPTIONS contains expected values."""
    expected_options = ["relevance", "pub_date", "Author", "JournalName"]
    assert PUBMED_SORT_OPTIONS == expected_options
    assert len(PUBMED_SORT_OPTIONS) == 4
    assert "relevance" in PUBMED_SORT_OPTIONS
    assert "pub_date" in PUBMED_SORT_OPTIONS


def test_application_output_options():
    """Test that APPLICATION_OUTPUT_OPTIONS contains expected values."""
    expected_options = ["overview", "emails"]
    assert APPLICATION_OUTPUT_OPTIONS == expected_options
    assert len(APPLICATION_OUTPUT_OPTIONS) == 2
    assert "overview" in APPLICATION_OUTPUT_OPTIONS
    assert "emails" in APPLICATION_OUTPUT_OPTIONS


def test_constants_are_lists():
    """Test that constants are proper list types."""
    assert isinstance(PUBMED_SORT_OPTIONS, list)
    assert isinstance(APPLICATION_OUTPUT_OPTIONS, list)


def test_constants_are_not_empty():
    """Test that constants are not empty."""
    assert len(PUBMED_SORT_OPTIONS) > 0
    assert len(APPLICATION_OUTPUT_OPTIONS) > 0
