import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, checklist, companies, glossary, incidents, locations, professions, progress, support, users


def _run_seed():
    try:
        from app.scripts.seed_all import seed_all
        seed_all()
    except Exception as e:
        import traceback
        print(f"[SEED] Error: {e}")
        traceback.print_exc()


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=_run_seed, daemon=True).start()
    yield


app = FastAPI(
    title="Cybersicherheitsassistent Demo API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(users.router)
app.include_router(checklist.router)
app.include_router(progress.router)
app.include_router(glossary.router)
app.include_router(incidents.router)
app.include_router(support.router)
app.include_router(locations.router)
app.include_router(professions.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "1.0.0"}