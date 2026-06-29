"""Run all seed scripts in order. Safe to run multiple times (idempotent)."""
from app.scripts.seed_bsi import seed as seed_bsi
from app.scripts.seed_glossary import run as seed_glossary
from app.scripts.seed_incidents import seed as seed_incidents
from app.scripts.seed_locations import run as seed_locations
from app.scripts.seed_professions import seed as seed_professions
from app.scripts.seed_support import seed as seed_support


def seed_all():
    seed_locations()
    seed_professions()
    seed_bsi()
    seed_glossary()
    seed_incidents()
    seed_support()
    print("[SEED] All done")


if __name__ == "__main__":
    seed_all()