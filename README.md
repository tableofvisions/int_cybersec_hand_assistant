# Initiative Cybersicherheit Handwerk — Demo

Self-contained demo instance of the Initiative Cybersicherheit Handwerk platform. Includes a Python FastAPI backend and a Next.js frontend, each with its own Docker Compose setup.

## Repository Layout

```
csa-demo/
├── backend/     ← Python FastAPI + PostgreSQL (port 8000)
└── frontend/    ← Next.js user-facing app (port 3001)
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

## Environment Setup

### Backend

```bash
cp backend/.env.example backend/.env
```

Key variables in `backend/.env`:

| Variable | Description |
|---|---|
| `SECRET_KEY` | JWT signing key — generate with `openssl rand -hex 32` |
| `DATABASE_URL` | PostgreSQL connection string |
| `RESEND_API_KEY` | Required for invite and password reset emails |
| `CORS_ORIGINS` | Comma-separated allowed origins (Vercel URL + localhost) |
| `FRONTEND_URL` | Base URL of the frontend (used in email links) |
| `DEV_AUTO_VERIFY` | Set `true` to skip email verification in local dev |

### Frontend

```bash
cp frontend/.env.example frontend/.env
```

Key variables in `frontend/.env`:

| Variable | Description |
|---|---|
| `BACKEND_API_URL` | API base URL — `http://host.docker.internal:8000/api/v1` for local dev |
| `NEXTAUTH_SECRET` | NextAuth signing secret — generate with `openssl rand -hex 32` |
| `NEXTAUTH_URL` | Public base URL of the frontend — `http://localhost:3001` for local dev |
| `NEXTAUTH_URL_INTERNAL` | Container-internal URL — `http://csagent_v2:3000` |

## Starting the Services

### Backend (FastAPI + PostgreSQL)

```bash
cd backend
docker compose up -d
```

This starts:
- **PostgreSQL** on port `5433` (host) → `5432` (container)
- **API** on port `8000`

Migrations run automatically on container start.

### Frontend (Next.js)

```bash
cd frontend
docker compose up -d
```

This starts the Next.js app on port `3001`.

### Service URLs

| Service | URL |
|---|---|
| FastAPI (Swagger UI) | http://localhost:8000/api/docs |
| Frontend | http://localhost:3001 |

## Stopping the Services

```bash
cd backend && docker compose down
cd frontend && docker compose down
```

## Logs

```bash
# Backend API logs
cd backend && docker compose logs -f api

# Frontend logs
cd frontend && docker compose logs -f
```

## Rebuild after code changes

Source files are mounted as volumes so most changes are picked up automatically. If you add Python dependencies, rebuild the image:

```bash
cd backend && docker compose up -d --build api
```

## Running one-off commands

```bash
# Run migrations manually
cd backend && docker compose run --rm api alembic upgrade head

# Open a shell inside the API container
cd backend && docker compose run --rm api sh
```

## Production Deployment

| Service | Platform | Trigger |
|---|---|---|
| Backend | Railway | Auto-deploy on push to `main` |
| Frontend | Vercel | Manual via Vercel CLI |

```bash
# Deploy frontend via Vercel CLI (from frontend/src/)
cd frontend/src && npx vercel deploy --prod
```

Environment variables must be configured in the respective platforms:

**Railway (backend):** `SECRET_KEY`, `DATABASE_URL` (provided by Railway), `RESEND_API_KEY`, `CORS_ORIGINS`, `FRONTEND_URL`

**Vercel (frontend):** `BACKEND_API_URL`, `NEXTAUTH_SECRET`, `NEXTAUTH_URL`