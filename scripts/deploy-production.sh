#!/bin/bash

# Production Deployment Script for ScholarSeek
# This script handles the deployment process including migrations and server startup

set -e  # Exit on any error

echo "🚀 Starting ScholarSeek production deployment..."

# Ensure we're in production mode
export DJANGO_ENVIRONMENT=production

# Source environment variables if .env.production exists
if [ -f "backend/.env.production" ]; then
    echo "📄 Loading production environment variables..."
    export $(cat backend/.env.production | grep -v '^#' | xargs)
else
    echo "❌ Error: backend/.env.production file not found"
    echo "   Please create this file with your production configuration"
    exit 1
fi

# Check required environment variables
required_vars=("DJANGO_SECRET_KEY" "DJANGO_ALLOWED_HOSTS")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Required environment variable $var is not set"
        exit 1
    fi
done

# Navigate to backend directory
cd backend

# Run database migrations
echo "🗃️ Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "🗂️ Collecting static files..."
python manage.py collectstatic --noinput --clear

# Check if superuser exists, if not prompt to create one
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('No superuser found. Please create one:')
    exit(1)
else:
    print('Superuser exists.')
" || {
    echo "Creating superuser..."
    python manage.py createsuperuser
}

# Start the production server
echo "🌐 Starting production server..."
exec gunicorn web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log