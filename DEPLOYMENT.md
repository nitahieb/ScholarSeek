# ScholarSeek Production Deployment Guide

This guide provides comprehensive instructions for deploying ScholarSeek to production environments.

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 13+
- Redis (optional, for caching)
- Nginx (for reverse proxy)
- SSL certificate (recommended)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nitahieb/ScholarSeek.git
   cd ScholarSeek
   ```

2. **Run the production build script**:
   ```bash
   ./scripts/build-production.sh
   ```

3. **Configure environment variables**:
   ```bash
   cp backend/.env.production.template backend/.env.production
   # Edit backend/.env.production with your settings
   ```

4. **Deploy to production**:
   ```bash
   export DJANGO_ENVIRONMENT=production
   ./scripts/deploy-production.sh
   ```

## Detailed Deployment Instructions

### 1. System Dependencies

Install required system packages:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and build dependencies
sudo apt install -y python3 python3-pip python3-venv build-essential

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install -y nginx

# Install Redis (optional)
sudo apt install -y redis-server
```

### 2. Database Setup

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE scholarseek;
CREATE USER scholarseek_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE scholarseek TO scholarseek_user;
\q
```

### 3. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/scholarseek
sudo chown $USER:$USER /var/www/scholarseek
cd /var/www/scholarseek

# Clone repository
git clone https://github.com/nitahieb/ScholarSeek.git .

# Install Python dependencies
pip install poetry
poetry install --only=main

# Build frontend
cd frontend
npm ci --only=production
npm run build
cd ..
```

### 4. Environment Configuration

Create production environment file:

```bash
cp backend/.env.production.template backend/.env.production
```

Edit `backend/.env.production` with your configuration:

```env
# Required Settings
DJANGO_SECRET_KEY=your-unique-secret-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DEBUG=False

# Database
DB_NAME=scholarseek
DB_USER=scholarseek_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# CORS (your frontend domains)
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# HTTPS
USE_HTTPS=True

# Email (for error reporting)
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
ADMIN_EMAIL=admin@yourdomain.com
```

### 5. Application Deployment

```bash
# Set environment
export DJANGO_ENVIRONMENT=production

# Run migrations
cd backend
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test the application
python manage.py check --deploy
```

### 6. Process Management with systemd

Create systemd service file:

```bash
sudo nano /etc/systemd/system/scholarseek.service
```

Content:

```ini
[Unit]
Description=ScholarSeek Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=scholarseek
WorkingDirectory=/var/www/scholarseek/backend
Environment=DJANGO_ENVIRONMENT=production
EnvironmentFile=/var/www/scholarseek/backend/.env.production
ExecStart=/var/www/scholarseek/.venv/bin/gunicorn web.wsgi:application \
    --bind unix:/run/scholarseek/scholarseek.sock \
    --workers 3 \
    --worker-class gthread \
    --worker-connections 1000 \
    --timeout 30 \
    --log-level info \
    --access-logfile /var/www/scholarseek/backend/logs/access.log \
    --error-logfile /var/www/scholarseek/backend/logs/error.log
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable scholarseek
sudo systemctl start scholarseek
sudo systemctl status scholarseek
```

### 7. Nginx Configuration

Create Nginx virtual host:

```bash
sudo nano /etc/nginx/sites-available/scholarseek
```

Content:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Frontend
    location / {
        root /var/www/scholarseek/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://unix:/run/scholarseek/scholarseek.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/scholarseek/backend/staticfiles/;
        expires 1y;
    }

    # Media files
    location /media/ {
        alias /var/www/scholarseek/backend/media/;
        expires 1y;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/scholarseek /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate Setup

Using Let's Encrypt:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Monitoring and Logging

Set up log rotation:

```bash
sudo nano /etc/logrotate.d/scholarseek
```

Content:

```
/var/www/scholarseek/backend/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload scholarseek
    endscript
}
```

### 10. Automated Backups

Set up automated backups with cron:

```bash
sudo crontab -e
```

Add:

```bash
# Daily backup at 2 AM
0 2 * * * /var/www/scholarseek/scripts/backup.sh >> /var/log/scholarseek-backup.log 2>&1
```

## Docker Deployment (Alternative)

For containerized deployment:

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Health Checks and Monitoring

The application includes a health check endpoint at `/api/health/` that returns:

```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "0.2.0",
    "database": "connected",
    "environment": "production"
}
```

Use this endpoint for:
- Load balancer health checks
- Monitoring system integration
- Uptime monitoring services

## Security Considerations

1. **Firewall**: Configure UFW or iptables to only allow necessary ports
2. **Updates**: Regular system and dependency updates
3. **Monitoring**: Set up intrusion detection and log monitoring
4. **Backups**: Test backup restoration procedures regularly
5. **SSL**: Use strong SSL configuration and HSTS headers

## Troubleshooting

### Common Issues

1. **Static files not loading**: Check `STATIC_ROOT` and Nginx configuration
2. **Database connection errors**: Verify PostgreSQL is running and credentials are correct
3. **Permission errors**: Ensure proper file ownership and permissions
4. **CORS errors**: Check `CORS_ALLOWED_ORIGINS` setting

### Log Files

- Application logs: `/var/www/scholarseek/backend/logs/`
- Nginx logs: `/var/log/nginx/`
- System logs: `/var/log/syslog`

## Performance Optimization

1. **Database**: Configure PostgreSQL for your workload
2. **Caching**: Enable Redis for session and cache storage
3. **CDN**: Use a CDN for static assets
4. **Monitoring**: Set up application performance monitoring

## Support

For issues and questions:
- GitHub Issues: https://github.com/nitahieb/ScholarSeek/issues
- Documentation: See README.md for development setup