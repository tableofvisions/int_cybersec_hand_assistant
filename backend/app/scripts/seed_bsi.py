"""
Seed BSI checklist data from pre-generated dump.

Usage:
  python -m app.scripts.seed_bsi
"""
import json
from pathlib import Path

from app.database import SessionLocal
from app.models.bsi import Area, BsiVersion, ChecklistItem, Mapping, Measure

DATA_FILE = Path(__file__).parent / "bsi_seed_data.json"


def seed():
    data = json.loads(DATA_FILE.read_text())
    db = SessionLocal()

    try:
        if db.query(BsiVersion).count() > 0:
            print("[SEED] BSI data already seeded — skipping")
            return

        print(f"[SEED] Inserting {len(data['versions'])} versions...")
        db.execute(BsiVersion.__table__.insert(), data["versions"])

        print(f"[SEED] Inserting {len(data['areas'])} areas...")
        db.execute(Area.__table__.insert(), data["areas"])

        print(f"[SEED] Inserting {len(data['measures'])} measures...")
        db.execute(Measure.__table__.insert(), data["measures"])

        print(f"[SEED] Inserting {len(data['mappings'])} mappings...")
        db.execute(Mapping.__table__.insert(), data["mappings"])

        print(f"[SEED] Inserting {len(data['checklist_items'])} checklist items...")
        db.execute(ChecklistItem.__table__.insert(), data["checklist_items"])

        db.commit()
        print("[SEED] BSI data seeded successfully")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
