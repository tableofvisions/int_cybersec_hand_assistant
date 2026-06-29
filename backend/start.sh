#!/bin/sh
echo "[START] Running alembic migrations..."
alembic upgrade head
echo "[START] Starting uvicorn on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}