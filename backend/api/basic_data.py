from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Literal, Optional

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

VALID_ROAD_TYPES = [
    "commerical_and_civic",
    "major",
    "pedestrian_and_recreational_paths",
    "rural_and_low_traffic",
    "suburban"
]

@app.get("/roads_by_region")
def get_roads_by_region(
    sa2_name: str,
    road_types: Optional[List[str]] = Query(default=None),
    db: Session = Depends(get_db)
):
    # Mapping of road_type to frontend labels
    ROAD_TYPE_LABELS = {
        "ambiguous": "Ambiguous Classification",
        "commerical_and_civic": "Commercial & Civic Roads",
        "infrastructure": "Infrastructure Roads",
        "major": "Major Roads",
        "pedestrian_and_recreational_paths": "Pedestrian & Recreational Paths",
        "rural_and_low_traffic": "Rural & Low-Traffic Roads",
        "suburban": "Suburban Roads",
        "-NULL-": "Unclassified"
    }

    # Validate road_types
    if road_types:
        invalid = [rt for rt in road_types if rt not in ROAD_TYPE_LABELS]
        if invalid:
            return {"error": f"Invalid road_types: {invalid}"}

    # Build dynamic SQL
    region_column = "vr.sa2_name21"  # fixed at SA2 for now
    
    if road_types:
        quoted_types = ",".join(f"'{rt}'" for rt in road_types)
        road_type_filter = f"AND vr.h_road_type IN ({quoted_types})"
    else:
        road_type_filter = ""

    query = f"""
        SELECT DISTINCT vr.ezirdnmlbl AS road_name,
                        vr.h_road_type,
                        ST_Length(ST_Union(vr.geom)::geography)/1000 AS road_length_km
        FROM vicmap_road vr
        WHERE LOWER({region_column}) = LOWER(:region_name)
        AND vr.h_road_type IS NOT NULL
        {road_type_filter}
        GROUP BY vr.ezirdnmlbl, vr.h_road_type
        ORDER BY vr.ezirdnmlbl;
    """

    result = db.execute(text(query), {"region_name": sa2_name}).fetchall()

    return [
        {
            "road_name": row[0],
            "road_type": ROAD_TYPE_LABELS.get(row[1], row[1]),
            "road_length_km": round(row[2], 2) if row[2] else None
        }
        for row in result
    ]

