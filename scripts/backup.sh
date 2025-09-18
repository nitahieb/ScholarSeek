#!/bin/bash

# Backup Script for ScholarSeek Production Database and Media Files
# This script creates automated backups with retention policy

set -e

# Configuration
BACKUP_DIR="/backups/scholarseek"
DATABASE_NAME="${DB_NAME:-scholarseek}"
DATABASE_USER="${DB_USER:-scholarseek_user}"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "🗄️ Starting ScholarSeek backup process..."

# Database backup
echo "📊 Backing up database..."
pg_dump -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -U "$DATABASE_USER" -d "$DATABASE_NAME" \
    > "$BACKUP_DIR/db_backup_$DATE.sql"

# Compress database backup
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

# Media files backup
if [ -d "backend/media" ]; then
    echo "📁 Backing up media files..."
    tar -czf "$BACKUP_DIR/media_backup_$DATE.tar.gz" -C backend media/
fi

# Log files backup
if [ -d "backend/logs" ]; then
    echo "📝 Backing up log files..."
    tar -czf "$BACKUP_DIR/logs_backup_$DATE.tar.gz" -C backend logs/
fi

# Clean up old backups
echo "🧹 Cleaning up old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

# Verify backup integrity
echo "✅ Verifying backup integrity..."
if gzip -t "$BACKUP_DIR/db_backup_$DATE.sql.gz"; then
    echo "✅ Database backup verified successfully"
else
    echo "❌ Database backup verification failed"
    exit 1
fi

# Calculate backup size
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "📊 Total backup size: $BACKUP_SIZE"

echo "✅ Backup completed successfully!"
echo "📁 Backup location: $BACKUP_DIR"
echo "📅 Backup timestamp: $DATE"