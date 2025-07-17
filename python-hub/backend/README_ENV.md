# Python Hub Environment Variables

Copy these variables to a `.env` file in your backend directory and edit as needed.

## General
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `CORS_ORIGINS`: Allowed CORS origins (default: *)

## Local Development
- `DEV_DATABASE_URL`: PostgreSQL URI for local dev (default: `postgresql://postgres:postgres@localhost:5432/postgres`)

## Docker Compose
- `DOCKER_DATABASE_URL`: PostgreSQL URI for Docker Compose (default: `postgresql://postgres:postgres@db:5432/postgres`)

## Production (Railway, etc.)
- `DATABASE_URL`: Production PostgreSQL URI (required in production)

## Celery/Redis
- `CELERY_BROKER_URL`: Redis broker URI
- `CELERY_RESULT_BACKEND`: Redis result backend URI

## Environment Selection
- `PYTHON_HUB_ENV`: Set to `production`, `docker`, `testing`, or leave blank for local dev 