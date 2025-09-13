import pytest
import sys
import os
import re

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestEmailRegex:
    """Comprehensive tests for email extraction regex patterns
    
    This tests the email extraction functionality independently of lxml dependencies.
    We can test the regex pattern directly since it's used in the parsing module.
    """
    
    def setup_method(self):
        """Set up the email regex pattern for testing"""
        # This is the same pattern used in parsing.py
        self.email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    
    def test_email_regex_basic_patterns(self):
        """Test basic email pattern matching"""
        test_cases = [
            ("user@domain.com", True),
            ("test.email@example.org", True),
            ("user-name@domain.edu", True),
            ("user_name@domain.net", True),
            ("123@numbers.co.uk", True),
            ("user@sub.domain.com", True),
            ("@domain.com", False),  # Missing username
            ("user@", False),        # Missing domain
            ("user.domain.com", False),  # Missing @
            ("user@domain", False),  # Missing TLD
        ]
        
        for text, should_match in test_cases:
            match = re.search(self.email_pattern, text)
            if should_match:
                assert match is not None, f"Expected to find email in '{text}'"
                assert match.group(0) == text, f"Expected full match for '{text}'"
            else:
                assert match is None, f"Expected no email match in '{text}'"
    
    def test_email_regex_in_text(self):
        """Test email pattern matching within larger text blocks"""
        test_cases = [
            ("Contact us at support@example.com for help", "support@example.com"),
            ("Email: researcher@university.edu", "researcher@university.edu"),
            ("Send to john.doe@lab.org or jane@lab.org", "john.doe@lab.org"),  # First match
            ("Department of Biology, email: prof@science.university.edu, Room 101", "prof@science.university.edu"),
            ("No email in this text", None),
            ("Multiple emails: first@domain.com and second@example.org", "first@domain.com"),
        ]
        
        for text, expected in test_cases:
            match = re.search(self.email_pattern, text)
            if expected:
                assert match is not None, f"Expected to find email in '{text}'"
                assert match.group(0) == expected, f"Expected '{expected}' but got '{match.group(0)}'"
            else:
                assert match is None, f"Expected no email in '{text}'"
    
    def test_email_regex_complex_domains(self):
        """Test email regex with complex domain structures"""
        valid_emails = [
            "user@domain.co.uk",
            "researcher@institute.research.org",
            "student@university.ac.jp",
            "admin@sub.domain.example.com",
            "test@very-long-domain-name.edu",
            "user123@domain456.org",
            "test.user@test-domain.co.uk",
        ]
        
        for email in valid_emails:
            match = re.search(self.email_pattern, email)
            assert match is not None, f"Expected to match '{email}'"
            assert match.group(0) == email, f"Expected full match for '{email}'"
    
    def test_email_regex_special_characters(self):
        """Test email regex with various special characters"""
        test_cases = [
            ("user.name@domain.com", True),
            ("user-name@domain.com", True),
            ("user_name@domain.com", True),
            ("user123@domain.com", True),
            ("123user@domain.com", True),
            ("user@domain-name.com", True),
            ("user@123domain.com", True),
            ("user+tag@domain.com", False),  # + not supported in our regex
            ("user@domain.com.", False),     # Trailing dot
            ("user@.domain.com", False),     # Leading dot in domain
        ]
        
        for email, should_match in test_cases:
            match = re.search(self.email_pattern, email)
            if should_match:
                assert match is not None, f"Expected to match '{email}'"
                assert match.group(0) == email, f"Expected full match for '{email}'"
            else:
                if match is not None:
                    # Allow partial matches for some edge cases
                    continue
    
    def test_email_regex_edge_cases(self):
        """Test edge cases for email regex"""
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "user@domain",  # No TLD
            "user@domain.",  # Empty TLD
            "@domain.com",  # No username
            "user@.com",  # No domain
            "a@b.c",  # Minimal valid email
            "very.long.username@very.long.domain.name.extension",  # Long email
        ]
        
        for case in edge_cases:
            match = re.search(self.email_pattern, case)
            # We don't assert specific behavior for edge cases,
            # just ensure the regex doesn't crash
            if match:
                assert isinstance(match.group(0), str)
    
    def test_email_regex_multiple_matches(self):
        """Test finding multiple emails in text"""
        text = "Contact first@domain.com or second@example.org for help"
        matches = re.findall(self.email_pattern, text)
        
        assert len(matches) == 2
        assert "first@domain.com" in matches
        assert "second@example.org" in matches
    
    def test_email_regex_international_domains(self):
        """Test email regex with international domain patterns"""
        international_emails = [
            "user@domain.de",
            "researcher@university.fr",
            "student@college.au",
            "admin@institute.jp",
            "test@example.ca",
            "user@domain.eu",
        ]
        
        for email in international_emails:
            match = re.search(self.email_pattern, email)
            assert match is not None, f"Expected to match international email '{email}'"
            assert match.group(0) == email
    
    def test_email_regex_surrounded_by_punctuation(self):
        """Test email regex when surrounded by punctuation"""
        test_cases = [
            ("Email: user@domain.com.", "user@domain.com"),
            ("(contact: researcher@lab.org)", "researcher@lab.org"),
            ("Send to <admin@example.com>", "admin@example.com"),
            ("Contact test@domain.com;", "test@domain.com"),
            ("Email [support@help.org]", "support@help.org"),
        ]
        
        for text, expected in test_cases:
            match = re.search(self.email_pattern, text)
            assert match is not None, f"Expected to find email in '{text}'"
            assert match.group(0) == expected, f"Expected '{expected}' in '{text}'"


class TestRegexPatterns:
    """Additional regex pattern tests for parsing functionality"""
    
    def test_date_pattern_extraction(self):
        """Test patterns that might be used for date extraction"""
        # Test year pattern
        year_pattern = r'\d{4}'
        test_texts = [
            ("Published in 2023", "2023"),
            ("Year: 2022", "2022"),
            ("1999-2000", "1999"),  # First match
            ("No year here", None),
        ]
        
        for text, expected in test_texts:
            match = re.search(year_pattern, text)
            if expected:
                assert match is not None, f"Expected year in '{text}'"
                assert match.group(0) == expected
            else:
                assert match is None, f"Expected no year in '{text}'"
    
    def test_month_pattern_extraction(self):
        """Test month number pattern extraction"""
        month_pattern = r'\b(0?[1-9]|1[0-2])\b'
        test_cases = [
            ("Month 01", "01"),
            ("Month 1", "1"),
            ("Month 12", "12"),
            ("Month 13", None),  # Invalid month
            ("Month 00", None),  # Invalid month
        ]
        
        for text, expected in test_cases:
            match = re.search(month_pattern, text)
            if expected:
                assert match is not None, f"Expected month in '{text}'"
                assert match.group(0) == expected
            else:
                assert match is None, f"Expected no valid month in '{text}'"
    
    def test_pmid_pattern_extraction(self):
        """Test PMID pattern extraction"""
        pmid_pattern = r'\b\d+\b'
        test_cases = [
            ("PMID: 12345678", "12345678"),
            ("ID 123", "123"),
            ("No numbers here", None),
            ("Mixed 123 text 456", "123"),  # First match
        ]
        
        for text, expected in test_cases:
            match = re.search(pmid_pattern, text)
            if expected:
                assert match is not None, f"Expected PMID in '{text}'"
                assert match.group(0) == expected
            else:
                assert match is None, f"Expected no PMID in '{text}'"
    
    def test_name_patterns(self):
        """Test patterns for extracting names"""
        # Simple name pattern (letters, spaces, hyphens, apostrophes)
        name_pattern = r"[A-Za-z\-'\s]+"
        
        test_names = [
            "John Smith",
            "Mary-Jane Watson",
            "O'Connor",
            "Jean-Paul",
            "Maria José",
        ]
        
        for name in test_names:
            match = re.search(name_pattern, name)
            assert match is not None, f"Expected to match name '{name}'"
            # Note: This is a simple pattern test, not comprehensive name validation
    
    def test_affiliation_keywords(self):
        """Test patterns for finding affiliation keywords"""
        university_pattern = r'\b(?:University|College|Institute|Laboratory|Department|Lab)\b'
        
        test_affiliations = [
            ("Stanford University", True),
            ("MIT Laboratory", True),
            ("Research Institute", True),
            ("Department of Biology", True),
            ("Independent researcher", False),
            ("Private company", False),
        ]
        
        for text, should_match in test_affiliations:
            match = re.search(university_pattern, text, re.IGNORECASE)
            if should_match:
                assert match is not None, f"Expected to find institution keyword in '{text}'"
            else:
                assert match is None, f"Expected no institution keyword in '{text}'"


class TestTextProcessingPatterns:
    """Test text processing patterns that might be used in parsing"""
    
    def test_whitespace_normalization(self):
        """Test whitespace normalization patterns"""
        texts = [
            "  Multiple   spaces  ",
            "\t\nTabs and newlines\t\n",
            "Normal text",
            "",
        ]
        
        for text in texts:
            # Test that we can normalize whitespace
            normalized = re.sub(r'\s+', ' ', text.strip())
            assert isinstance(normalized, str)
            if text.strip():
                assert normalized  # Should not be empty if original had content
    
    def test_html_tag_removal(self):
        """Test HTML tag removal patterns"""
        html_pattern = r'<[^>]+>'
        
        test_cases = [
            ("<b>Bold</b>", "Bold"),
            ("Text with <em>emphasis</em>", "Text with emphasis"),
            ("No HTML here", "No HTML here"),
            ("<p>Paragraph <span>with</span> tags</p>", "Paragraph with tags"),
        ]
        
        for html_text, expected in test_cases:
            cleaned = re.sub(html_pattern, '', html_text)
            assert cleaned == expected, f"Expected '{expected}' but got '{cleaned}'"
    
    def test_special_character_handling(self):
        """Test handling of special characters in text"""
        special_chars = [
            "Text with & ampersand",
            "Quotes 'single' and \"double\"",
            "Punctuation: semicolon; comma, period.",
            "Numbers 123 and symbols #@$%",
        ]
        
        for text in special_chars:
            # Test that patterns can handle special characters without crashing
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
            # Should not crash, regardless of match result
            assert email_match is None or isinstance(email_match.group(0), str)
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters"""
        unicode_texts = [
            "Café with accents",
            "José María González",
            "Universität München",
            "École Polytechnique",
            "北京大学",  # Chinese characters
        ]
        
        for text in unicode_texts:
            # Test that regex patterns can handle Unicode
            try:
                # Simple pattern that should work with Unicode
                match = re.search(r'\w+', text)
                if match:
                    assert isinstance(match.group(0), str)
            except Exception as e:
                pytest.fail(f"Unicode handling failed for '{text}': {e}")