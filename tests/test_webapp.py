import pytest
from unittest.mock import patch
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from webapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the main page loads correctly (React app)"""
    response = client.get('/')
    assert response.status_code == 200
    # Check that the React app structure is present
    assert b'<div id="root"></div>' in response.data
    assert b'main.' in response.data  # Check for main.js bundle

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_search_endpoint_missing_searchterm(client):
    """Test search endpoint with missing searchterm"""
    response = client.post('/api/search',
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'searchterm is required' in data['error']

def test_search_endpoint_invalid_mode(client):
    """Test search endpoint with invalid mode"""
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'mode': 'invalid'},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid mode' in data['error']

def test_search_endpoint_invalid_sortby(client):
    """Test search endpoint with invalid sortby"""
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'sortby': 'invalid'},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid sortby' in data['error']

def test_search_endpoint_invalid_searchnumber(client):
    """Test search endpoint with invalid searchnumber"""
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'searchnumber': 0},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'searchnumber must be between 1 and 100' in data['error']

@patch('webapp.subprocess.run')
def test_search_endpoint_network_error(mock_subprocess, client):
    """Test search endpoint with network error (blocked PubMed access)"""
    # Mock subprocess response with network error
    mock_result = type('MockResult', (), {
        'returncode': 1,
        'stdout': '',
        'stderr': 'urllib.error.URLError: <urlopen error [Errno -5] No address associated with hostname>'
    })()
    mock_subprocess.return_value = mock_result
    
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'mode': 'overview'},
                          content_type='application/json')
    assert response.status_code == 500
    data = response.get_json()
    assert 'Network access to PubMed is currently blocked' in data['error']
    assert 'eutils.ncbi.nlm.nih.gov' in data['details']

@patch('webapp.subprocess.run')
def test_search_endpoint_overview_mode(mock_subprocess, client):
    """Test search endpoint in overview mode with mocked subprocess"""
    # Mock successful subprocess response
    mock_result = type('MockResult', (), {
        'returncode': 0,
        'stdout': "## Mock Article\n**Title:** Test Article",
        'stderr': ''
    })()
    mock_subprocess.return_value = mock_result
    
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'mode': 'overview'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success']
    assert data['mode'] == 'overview'
    assert 'Mock Article' in data['result']
    # Check that subprocess was called with correct arguments
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert 'test' in call_args[0][0]  # searchterm in command
    assert '-m' in call_args[0][0]  # mode flag
    assert 'overview' in call_args[0][0]  # mode value

@patch('webapp.subprocess.run')
def test_search_endpoint_emails_mode(mock_subprocess, client):
    """Test search endpoint in emails mode with mocked subprocess"""
    # Mock successful subprocess response
    mock_result = type('MockResult', (), {
        'returncode': 0,
        'stdout': "test@example.com, author@university.edu",
        'stderr': ''
    })()
    mock_subprocess.return_value = mock_result
    
    response = client.post('/api/search',
                          json={'searchterm': 'test', 'mode': 'emails'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success']
    assert data['mode'] == 'emails'
    assert 'test@example.com' in data['result']
    # Check that subprocess was called with correct arguments
    mock_subprocess.assert_called_once()
    call_args = mock_subprocess.call_args
    assert 'test' in call_args[0][0]  # searchterm in command
    assert '-m' in call_args[0][0]  # mode flag
    assert 'emails' in call_args[0][0]  # mode value
