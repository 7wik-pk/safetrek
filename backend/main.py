from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, model_validator, conint
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Literal, Optional, List
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
# --- Database setup ---
DATABASE_URL = "postgresql://postgres:pass@postgis:5432/strek"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Request schema ---
class AccidentStatsRequest(BaseModel):
    filter_area_level: Literal["sa2", "sa3", "sa4"]
    filter_area_name: str
    group_by_area_level: Literal["sa2", "sa3"]
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    order_by: Literal["count", "density"] = "count"
    order_dir: Literal["asc", "desc"] = "desc"
    limit: conint(ge=1, le=100) = 10

    @model_validator(mode="before")
    def validate_area_hierarchy(cls, values):
        hierarchy = ["sa2", "sa3", "sa4"]
        filter_level = values.get("filter_area_level")
        group_level = values.get("group_by_area_level")
        if hierarchy.index(group_level) >= hierarchy.index(filter_level):
            raise ValueError("group_by_area_level must be lower than filter_area_level")
        return values

# --- FastAPI app ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vue dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/accident_stats")
def get_accident_stats(req: AccidentStatsRequest, db: Session = Depends(get_db)):
    filter_column = {
        "sa2": "sa2_name21",
        "sa3": "sa3_name21",
        "sa4": "sa4_name21"
    }[req.filter_area_level]

    group_column = {
        "sa2": "sa2_name21",
        "sa3": "sa3_name21"
    }[req.group_by_area_level]

    # Mesh block filter clause
    mb_where = f"""
        WHERE lower(mbv.{filter_column}) = lower(:filter_area_name)
        AND lower(mbv.{group_column}) IS NOT NULL
    """

    # Accident date filter clause
    acc_where = []
    if req.date_from:
        acc_where.append("a.accident_date >= :date_from")
    if req.date_to:
        acc_where.append("a.accident_date <= :date_to")
    acc_where_clause = " AND ".join(acc_where)
    if acc_where_clause:
        acc_where_clause = "WHERE " + acc_where_clause

    # Ordering clause
    direction = "DESC" if req.order_dir.lower() == "desc" else "ASC"
    order_clause = {
        "count": f"ORDER BY COUNT(a.accident_no) {direction}",
        "density": f"ORDER BY COUNT(a.accident_no)/(ST_Area(s.geom::geography)/1000000) {direction}"
    }[req.order_by]

    # Final SQL
    sql = text(f"""
        WITH sas AS (
            SELECT
                ST_Union(mbv.geom) AS geom,
                mbv.{group_column} AS sa_name
            FROM mesh_block_vic_21 mbv
            {mb_where}
            GROUP BY sa_name
        )
        SELECT 
            COUNT(a.accident_no) AS num_accs,
            ST_Area(s.geom::geography)/1000000 AS geom_area_sq_km,
            COUNT(a.accident_no)/(ST_Area(s.geom::geography)/1000000) AS acc_per_sq_km,
            s.sa_name,
            ST_AsText(s.geom) AS geom
        FROM accident a
        JOIN sas s ON ST_Contains(s.geom, a.geom)
        {acc_where_clause}
        GROUP BY s.sa_name, s.geom
        {order_clause}
        LIMIT :limit
    """)

    params = {
        "filter_area_name": req.filter_area_name,
        "date_from": req.date_from,
        "date_to": req.date_to,
        "limit": req.limit
    }

    result = db.execute(sql, params).fetchall()
    return [dict(row._mapping) for row in result]

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
