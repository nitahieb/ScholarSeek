# Development Setup Guide

This guide will help you set up the PubMed Author Finder for development.

## Prerequisites

- Python 3.10+ (tested with 3.11, 3.12, 3.13)
- Node.js 16+ and npm
- Poetry (recommended for Python dependency management)
- Git

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/nitahieb/pubmed-author-finder.git
cd pubmed-author-finder
```

### 2. CLI Development Setup
```bash
# Install dependencies
poetry install --no-interaction --no-root

# Test the CLI
poetry run python cli/main.py --help
poetry run python cli/main.py "cancer research" -n 2 -m overview

# Run tests
poetry run pytest tests/ -v

# Run linting
poetry run ruff check .
```

### 3. Backend Development Setup
```bash
# Install dependencies (if not already done)
poetry install --no-interaction --no-root

# Set up environment variables (optional)
cp .env.example .env  # Create this file if needed
# Edit .env with your settings

# Run Django development server
cd backend
poetry run python manage.py migrate  # Set up database
poetry run python manage.py runserver  # Start server on http://localhost:8000

# Create superuser (optional)
poetry run python manage.py createsuperuser
```

### 4. Frontend Development Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev  # Start on http://localhost:5173

# Run linting
npm run lint

# Build for production
npm run build
```

## Development Workflow

### Working on CLI Features
1. Make changes in `cli/` directory
2. Run tests: `poetry run pytest tests/`
3. Test manually: `poetry run python cli/main.py "your query"`
4. Run linting: `poetry run ruff check .`

### Working on Backend Features
1. Make changes in `backend/` directory
2. Test Django functionality: `cd backend && poetry run python manage.py runserver`
3. Test API endpoints using curl, Postman, or the frontend
4. Run linting: `poetry run ruff check .`

### Working on Frontend Features
1. Make changes in `frontend/` directory
2. Test with development server: `npm run dev`
3. Run linting: `npm run lint`
4. Test integration with backend API

## Testing

### Running All Tests
```bash
# Python tests (CLI functionality)
poetry run pytest tests/ -v

# Frontend linting
cd frontend && npm run lint

# Python linting
poetry run ruff check .
```

### Test Coverage
- **CLI**: 100 comprehensive test cases covering all modules
- **Linting**: Enforced code style with Ruff (Python) and ESLint (TypeScript)
- **Integration**: Manual testing of CLI-backend integration

## Common Development Tasks

### Adding New CLI Features
1. Implement the feature in appropriate `cli/` modules
2. Add tests in `tests/` directory
3. Update help text and documentation
4. Ensure all tests pass

### Adding New API Endpoints
1. Add views in `backend/api/views.py`
2. Add URL patterns in `backend/api/urls.py`
3. Add serializers if needed in `backend/api/serializers.py`
4. Test the endpoints manually or with automated tests

### Adding New Frontend Components
1. Create component in `frontend/src/components/`
2. Add proper TypeScript types
3. Integrate with routing if needed
4. Ensure ESLint passes

## Environment Configuration

### Python Environment
Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend Environment
Create `frontend/.env.local`:
```bash
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Common Issues

**"Module not found" errors in CLI**
- Ensure you're using Poetry: `poetry run python cli/main.py`
- Check that pytest.ini has correct pythonpath

**Network errors when testing CLI**
- Expected in sandboxed environments
- CLI argument parsing should work even without internet

**Frontend can't connect to backend**
- Ensure backend is running on http://localhost:8000
- Check CORS settings in Django
- Verify VITE_API_URL environment variable

**Poetry installation issues**
- Install Poetry: `pip install poetry`
- Alternative: Use pip directly: `pip install -r requirements.txt` (if available)

### Debug Tips

1. **CLI debugging**: Add print statements or use Python debugger
2. **Backend debugging**: Use Django's built-in logging and debug toolbar
3. **Frontend debugging**: Use browser developer tools and console

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the patterns above
4. Ensure all tests pass
5. Submit a pull request

## Performance Notes

- **CLI**: Very fast (< 1 second for tests, < 3 seconds total build)
- **Backend**: Django development server is suitable for testing
- **Frontend**: Vite provides fast hot-reload development

## IDE Setup

### VS Code Recommended Extensions
- Python (ms-python.python)
- Ruff (charliermarsh.ruff)
- ES7+ React/Redux/React-Native snippets
- TypeScript Importer

### PyCharm Setup
- Configure Poetry interpreter
- Enable Ruff for linting
- Set up run configurations for CLI and Django