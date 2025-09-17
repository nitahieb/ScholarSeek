# Architecture Overview

This document provides an overview of the PubMed Author Finder architecture and how the different components interact.

## System Components

### 🔧 CLI Application (`cli/`)
The core Python application that provides PubMed search functionality.

**Key modules:**
- `main.py` - Entry point and command-line interface
- `services.py` - Business logic for search operations
- `pipeline.py` - PubMed API integration using entrezpy
- `analyzer.py` - XML response parsing and article data extraction
- `format.py` - Output formatting (overview and email formats)

**Dependencies:** entrezpy, lxml, uniqpath

### 🌐 Backend API (`backend/`)
Django REST API that wraps the CLI functionality for web access.

**Structure:**
- `web/` - Django project configuration
- `api/` - REST API application with endpoints
- `manage.py` - Django management commands

**Key features:**
- User authentication with JWT tokens
- Search history tracking
- RESTful API endpoints
- Integration with CLI via subprocess calls

**Dependencies:** Django, djangorestframework, djangorestframework-simplejwt

### 🎨 Frontend (`frontend/`)
React/TypeScript web application providing a user-friendly interface.

**Key components:**
- Authentication system (login/register)
- Search interface with configurable options
- Results display (overview/email modes)
- Protected routes for authenticated users

**Dependencies:** React, TypeScript, Vite, axios, react-router-dom

## Data Flow

```
User Input (Web/CLI)
        ↓
    CLI Application
        ↓
    PubMed API (entrezpy)
        ↓
    XML Parsing & Analysis
        ↓
    Formatted Results
        ↓
    Output (Terminal/API Response)
        ↓
    Frontend Display (Web only)
```

## Integration Points

### CLI ↔ Backend
The Django backend calls the CLI application as a subprocess:
```python
cli_args = [
    sys.executable,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cli/main.py')),
    # ... arguments
]
result = subprocess.run(cli_args, capture_output=True, text=True)
```

### Backend ↔ Frontend
RESTful API communication:
- Authentication: JWT token-based
- Search endpoint: `POST /api/search/`
- User management: `POST /api/user/register/`, token endpoints

## Development Workflow

### Local Development
1. **CLI development**: Direct Python execution in `cli/`
2. **Backend development**: Django development server
3. **Frontend development**: Vite development server
4. **Full stack**: Run all components simultaneously

### Testing
- **CLI tests**: 100 test cases covering all functionality
- **Linting**: Ruff for Python, ESLint for TypeScript
- **CI/CD**: GitHub Actions for automated testing

## Configuration

### Environment Variables
- `SECRET_KEY` - Django secret key
- `DEBUG` - Django debug mode
- `ALLOWED_HOSTS` - Django allowed hosts
- `VITE_API_URL` - Frontend API endpoint

### File Configuration
- `pyproject.toml` - Python dependencies and project metadata
- `package.json` - Frontend dependencies
- `pytest.ini` - Test configuration
- Various TypeScript/ESLint configs

## Security Considerations

- JWT tokens for API authentication
- Environment-based configuration
- Input validation and sanitization
- CORS configuration for frontend-backend communication

## Future Enhancements

- Docker containerization
- Database migration strategy
- Caching layer for PubMed results
- Rate limiting for API endpoints
- Enhanced error handling and logging