#!/usr/bin/env bash
set -Eeuo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
mkdir -p "$BACKUP_DIR"
timestamp=$(date -u +%Y%m%dT%H%M%SZ)

if [[ "${DATABASE_URL:-}" == postgresql://* || "${DATABASE_URL:-}" == postgres://* ]]; then
  output="$BACKUP_DIR/price_tracker_${timestamp}.dump"
  pg_dump --format=custom --no-owner --file="$output" "$DATABASE_URL"
else
  db_path="${SQLITE_PATH:-backend/instance/price_tracker.db}"
  output="$BACKUP_DIR/price_tracker_${timestamp}.sqlite"
  sqlite3 "$db_path" ".backup '$output'"
fi

find "$BACKUP_DIR" -type f -mtime "+$RETENTION_DAYS" -delete
printf 'Backup criado: %s\n' "$output"
