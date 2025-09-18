#!/bin/bash

# Production Build Script for ScholarSeek
# This script builds the frontend and prepares the backend for production deployment

set -e  # Exit on any error

echo "🚀 Starting ScholarSeek production build..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: This script must be run from the ScholarSeek root directory"
    exit 1
fi

# Build Frontend
echo "📦 Building frontend..."
cd frontend
npm ci --only=production
npm run build
cd ..

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if command -v poetry &> /dev/null; then
    poetry install --only=main --no-interaction
else
    pip install -r requirements.txt
fi

# Install additional production dependencies
echo "📚 Installing production dependencies..."
if command -v poetry &> /dev/null; then
    poetry add psycopg2-binary whitenoise gunicorn
else
    pip install psycopg2-binary whitenoise gunicorn
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/staticfiles
mkdir -p backend/media

# Collect static files
echo "🗂️ Collecting static files..."
cd backend
python manage.py collectstatic --noinput --clear
cd ..

# Check for environment file
if [ ! -f "backend/.env.production" ]; then
    echo "⚠️  Warning: backend/.env.production file not found"
    echo "   Please copy backend/.env.production.template to backend/.env.production"
    echo "   and configure it with your production values"
fi

echo "✅ Production build completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set DJANGO_ENVIRONMENT=production in your environment"
echo "2. Configure backend/.env.production with your settings"
echo "3. Run database migrations: cd backend && python manage.py migrate"
echo "4. Create a superuser: cd backend && python manage.py createsuperuser"
echo "5. Start the server: cd backend && gunicorn web.wsgi:application"