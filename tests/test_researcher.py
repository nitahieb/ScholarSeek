import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from researcher import Researcher


class TestResearcher:
    """Comprehensive tests for the Researcher class"""
    
    def test_researcher_default_initialization(self):
        """Test Researcher initialization with default empty values"""
        r = Researcher()
        assert r.firstName == ""
        assert r.lastName == ""
        assert r.initials == ""
        assert r.affiliation == ""
        assert r.email == ""
    
    def test_researcher_full_initialization(self):
        """Test Researcher initialization with all parameters"""
        r = Researcher(
            lastName="Smith",
            firstName="John",
            initials="JS",
            affiliation="MIT",
            email="john@mit.edu"
        )
        assert r.lastName == "Smith"
        assert r.firstName == "John"
        assert r.initials == "JS"
        assert r.affiliation == "MIT"
        assert r.email == "john@mit.edu"
    
    def test_researcher_partial_initialization(self):
        """Test Researcher initialization with only some parameters"""
        r = Researcher(lastName="Doe", firstName="Jane")
        assert r.lastName == "Doe"
        assert r.firstName == "Jane"
        assert r.initials == ""
        assert r.affiliation == ""
        assert r.email == ""
    
    def test_researcher_named_parameters(self):
        """Test Researcher initialization using named parameters in different order"""
        r = Researcher(email="test@example.com", firstName="Alice", lastName="Johnson")
        assert r.lastName == "Johnson"
        assert r.firstName == "Alice"
        assert r.initials == ""
        assert r.affiliation == ""
        assert r.email == "test@example.com"
    
    def test_researcher_repr_empty(self):
        """Test string representation of empty Researcher"""
        r = Researcher()
        repr_str = repr(r)
        assert "Researcher(" in repr_str
        assert "firstName=" in repr_str
        assert "lastName=" in repr_str
        assert "initials=" in repr_str
        assert "affiliation=" in repr_str
        assert "email=" in repr_str
    
    def test_researcher_repr_full(self):
        """Test string representation of fully populated Researcher"""
        r = Researcher(
            lastName="Brown",
            firstName="Charlie",
            initials="CB",
            affiliation="Stanford University",
            email="charlie@stanford.edu"
        )
        repr_str = repr(r)
        assert "Researcher(" in repr_str
        assert "firstName=Charlie" in repr_str
        assert "lastName=Brown" in repr_str
        assert "initials=CB" in repr_str
        assert "affiliation=Stanford University" in repr_str
        assert "charlie@stanford.edu" in repr_str
    
    def test_researcher_attribute_modification(self):
        """Test that Researcher attributes can be modified after creation"""
        r = Researcher()
        r.firstName = "Bob"
        r.lastName = "Wilson"
        r.email = "bob@example.com"
        
        assert r.firstName == "Bob"
        assert r.lastName == "Wilson"
        assert r.email == "bob@example.com"
        assert r.initials == ""
        assert r.affiliation == ""
    
    def test_researcher_none_values(self):
        """Test Researcher initialization with None values"""
        r = Researcher(
            lastName=None,
            firstName=None,
            initials=None,
            affiliation=None,
            email=None
        )
        assert r.lastName is None
        assert r.firstName is None
        assert r.initials is None
        assert r.affiliation is None
        assert r.email is None
    
    def test_researcher_special_characters(self):
        """Test Researcher with special characters in names and affiliations"""
        r = Researcher(
            lastName="O'Connor",
            firstName="María José",
            initials="M.J.",
            affiliation="École Polytechnique Fédérale de Lausanne",
            email="maria.jose@epfl.ch"
        )
        assert r.lastName == "O'Connor"
        assert r.firstName == "María José"
        assert r.initials == "M.J."
        assert r.affiliation == "École Polytechnique Fédérale de Lausanne"
        assert r.email == "maria.jose@epfl.ch"
    
    def test_researcher_long_values(self):
        """Test Researcher with very long strings"""
        long_affiliation = "Department of Very Long Scientific Research in Advanced " \
                          "Technologies and Biological Sciences at the International " \
                          "Institute of Technology and Innovation"
        long_email = "very.long.email.address.for.testing@university.example.org"
        
        r = Researcher(
            affiliation=long_affiliation,
            email=long_email
        )
        assert r.affiliation == long_affiliation
        assert r.email == long_email
    
    def test_researcher_empty_strings_vs_none(self):
        """Test difference between empty strings and None values"""
        r1 = Researcher()  # Default empty strings
        r2 = Researcher(lastName=None, firstName=None)  # Explicit None
        
        assert r1.lastName == ""
        assert r1.firstName == ""
        assert r2.lastName is None
        assert r2.firstName is None
    
    def test_researcher_vars_dict(self):
        """Test that vars() returns the correct dictionary representation"""
        r = Researcher(
            lastName="Test",
            firstName="User",
            email="test@example.com"
        )
        vars_dict = vars(r)
        expected_keys = {"firstName", "lastName", "initials", "affiliation", "email"}
        assert set(vars_dict.keys()) == expected_keys
        assert vars_dict["firstName"] == "User"
        assert vars_dict["lastName"] == "Test"
        assert vars_dict["email"] == "test@example.com"
        assert vars_dict["initials"] == ""
        assert vars_dict["affiliation"] == ""