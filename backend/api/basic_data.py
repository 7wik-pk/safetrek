from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from db import get_db

app = APIRouter()

### Additional endpoints for distinct area names

@app.get("/distinct_sa2", response_model=List[str])
def get_distinct_sa2(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT DISTINCT sa2_name21
        FROM mesh_block_vic_21
        WHERE sa2_name21 IS NOT NULL
        ORDER BY sa2_name21
    """)).fetchall()
    return [row[0] for row in result]

@app.get("/distinct_sa3", response_model=List[str])
def get_distinct_sa3(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT DISTINCT sa3_name21
        FROM mesh_block_vic_21
        WHERE sa3_name21 IS NOT NULL
        ORDER BY sa3_name21
    """)).fetchall()
    return [row[0] for row in result]

@app.get("/distinct_sa4", response_model=List[str])
def get_distinct_sa4(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT DISTINCT sa4_name21
        FROM mesh_block_vic_21
        WHERE sa4_name21 IS NOT NULL
        ORDER BY sa4_name21
    """)).fetchall()
    return [row[0] for row in result]

@app.get('/max_accident_date', response_model=str)
def get_max_accident_date(db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT MAX(accident_date) FROM accident
    """)).fetchone()
    return result[0].isoformat() if result and result[0] else None