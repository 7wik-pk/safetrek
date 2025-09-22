from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# --- Database setup ---
engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()