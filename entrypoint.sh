#!/bin/sh

# Exit on error
set -e

# Apply database migrations
if [ "$CONTAINER_NAME" = "CELERY" ]; then
    echo "Applying database migrations"
    python manage.py migrate

fi

exec "$@"