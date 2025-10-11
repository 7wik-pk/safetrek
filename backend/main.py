from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api import stats_trends

load_dotenv(".env")  # Load variables from .env file

from typing import List

from config import settings

# --- FastAPI app ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    # allow all origins (temporary)
    allow_credentials=False,
    
    # to disallow all origins later
    # allow_credentials=True,

    allow_origins = (settings.allowed_origins or ["*"]),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Registering endpoints from different modules/groups of endpoints
from api import basic_data, stats_trends, factors_dry as factors, blackspot_corridor

app.include_router(basic_data.app)
app.include_router(stats_trends.app)
app.include_router(factors.app)
app.include_router(blackspot_corridor.router)

### Additional endpoints for distinct area names

# @app.get("/distinct_sa2", response_model=List[str])
# def get_distinct_sa2(db: Session = Depends(get_db)):
#     result = db.execute(text("""
#         SELECT DISTINCT sa2_name21
#         FROM mesh_block_vic_21
#         WHERE sa2_name21 IS NOT NULL
#         ORDER BY sa2_name21
#     """)).fetchall()
#     return [row[0] for row in result]

# @app.get("/distinct_sa3", response_model=List[str])
# def get_distinct_sa3(db: Session = Depends(get_db)):
#     result = db.execute(text("""
#         SELECT DISTINCT sa3_name21
#         FROM mesh_block_vic_21
#         WHERE sa3_name21 IS NOT NULL
#         ORDER BY sa3_name21
#     """)).fetchall()
#     return [row[0] for row in result]

# @app.get("/distinct_sa4", response_model=List[str])
# def get_distinct_sa4(db: Session = Depends(get_db)):
#     result = db.execute(text("""
#         SELECT DISTINCT sa4_name21
#         FROM mesh_block_vic_21
#         WHERE sa4_name21 IS NOT NULL
#         ORDER BY sa4_name21
#     """)).fetchall()
#     return [row[0] for row in result]

# @app.get('/max_accident_date', response_model=str)
# def get_max_accident_date(db: Session = Depends(get_db)):
#     result = db.execute(text("""
#         SELECT MAX(accident_date) FROM accident
#     """)).fetchone()
#     return result[0].isoformat() if result and result[0] else None

# --- Yearly trend (accidents + serious injuries + injuries total) ---
