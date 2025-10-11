from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, Literal, List
from datetime import date, time
from db import get_db

router = APIRouter()

@router.get("/corridor_crash_density")
def get_corridor_crash_density(
    region_level: Literal["sa2", "sa3"],
    region_name: str,
    road_name: str,
    start_date: date,
    end_date: date,
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
    order_by: Literal["density", "count"] = "density",
    order_dir_asc: bool = False,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Mapping of segment_type to frontend labels
    SEGMENT_LABELS = {
        "bridge": "Bridge",
        "connector": "Connector Road",
        "ferry_route": "Ferry Route",
        "foot_bridge": "Footbridge",
        "ford": "Low-Water Crossing (Ford)",
        "road": "Road Segment",
        "roundabout": "Roundabout",
        "trail": "Trail or Pathway",
        "tunnel": "Tunnel"
    }

    # Build dynamic filters
    region_column = f"vr.{region_level}_name21"
    time_filter = ""
    if start_time and end_time:
        time_filter = "AND a.accident_time BETWEEN :start_time AND :end_time"

    order_column = "accs_per_km" if order_by == "density" else "num_accs"
    order_direction = "ASC" if order_dir_asc else "DESC"

    query = f"""
        WITH road_segments_in_sax AS (
            SELECT vr.geom,
                   ST_Length(vr.geom::geography)/1000 AS seg_length_km,
                   vr.ezirdnmlbl AS road_name,
                   vr.ftype_code AS seg_type
            FROM vicmap_road vr
            WHERE LOWER({region_column}) = LOWER(:region_name)
              AND LOWER(vr.ezirdnmlbl) = LOWER(:road_name)
        ),
        acc_in_rs AS (
            SELECT a.geom AS acc_geom,
                   a.accident_no,
                   a.accident_date,
                   a.accident_time,
                   rs.geom AS rs_geom,
                   rs.road_name,
                   rs.seg_length_km,
                   rs.seg_type
            FROM accident a
            JOIN road_segments_in_sax rs
              ON ST_DWithin(a.geom::geography, rs.geom::geography, 10)
            WHERE a.accident_date BETWEEN :start_date AND :end_date
              {time_filter}
        )
        SELECT ST_AsText(a.rs_geom) rs_geom,
               a.road_name,
               a.seg_type,
               COUNT(a.accident_no) AS num_accs,
               COUNT(a.accident_no)/a.seg_length_km AS accs_per_km
        FROM acc_in_rs a
        GROUP BY a.rs_geom, a.road_name, a.seg_type, a.seg_length_km
        ORDER BY {order_column} {order_direction}
        LIMIT :limit;
    """

    params = {
        "region_name": region_name,
        "road_name": road_name,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit
    }
    if start_time and end_time:
        params["start_time"] = start_time
        params["end_time"] = end_time

    result = db.execute(text(query), params).fetchall()

    return [
        {
            "road_name": row[1],
            "segment_geom_wkt": row[0],
            "segment_type": SEGMENT_LABELS.get(row[2], row[2]),
            "num_accidents": row[3],
            "accidents_per_km": round(row[4], 2)
        }
        for row in result
    ]


@router.get("/blackspot_crash_density")
def get_blackspot_crash_density(
    region_level: Literal["sa2", "sa3"],
    region_name: str,
    road_name: str,
    start_date: date,
    end_date: date,
    start_time: Optional[time] = None,
    end_time: Optional[time] = None,
    structure_types: Optional[List[str]] = Query(default=None),
    order_dir_asc: bool = False,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Mapping of structure_type to frontend labels
    STRUCTURE_LABELS = {
        "barrier": "Road Barrier",
        "bridge": "Bridge",
        "ford": "Low-Water Crossing (Ford)",
        "gate": "Road Gate",
        "int_attribute": "Intersection (Attribute Only)",
        "int_coast": "Coastal Intersection",
        "int_locality": "Locality Intersection",
        "int_nosignal": "Unsignalized Intersection",
        "int_paper": "Paper Road Intersection",
        "int_signal": "Signalized Intersection",
        "level_crossing": "Railway Level Crossing",
        "road_end": "Road End",
        "roundabout": "Roundabout",
        "tunnel": "Tunnel"
    }

    # Dynamic region column
    region_column = f"vr.{region_level}_name21"

    # Optional filters
    time_filter = ""
    if start_time and end_time:
        time_filter = "AND a.accident_time BETWEEN :start_time AND :end_time"

    struct_type_filter = ""
    if structure_types:
        quoted_types = ",".join(f"'{stype}'" for stype in structure_types)
        struct_type_filter = f"AND vrs.ftype_code IN ({quoted_types})"

    order_direction = "ASC" if order_dir_asc else "DESC"

    query = f"""
        WITH road AS (
            SELECT ST_Union(vr.geom) AS geom,
                   vr.ezirdnmlbl AS road_name
            FROM vicmap_road vr
            WHERE LOWER(vr.ezirdnmlbl) = LOWER(:road_name)
              AND LOWER({region_column}) = LOWER(:region_name)
            GROUP BY vr.ezirdnmlbl
        ),
        rs_in_road AS (
            SELECT vrs.geom,
                   vrs.ftype_code AS struct_type,
                   road.road_name
            FROM vicmap_road_structures vrs
            JOIN road ON ST_DWithin(vrs.geom::geography, road.geom::geography, 5)
            {struct_type_filter}
        )
        SELECT COUNT(a.accident_no) AS num_accidents,
               ST_AsText(rs.geom) AS rs_geom,
               rs.road_name,
               rs.struct_type
        FROM accident a
        JOIN rs_in_road rs ON ST_DWithin(a.geom::geography, rs.geom::geography, 10)
        WHERE a.accident_date BETWEEN :start_date AND :end_date
        {time_filter}
        GROUP BY rs_geom, rs.road_name, rs.struct_type
        ORDER BY COUNT(a.accident_no) {order_direction}
        LIMIT :limit;
    """

    params = {
        "region_name": region_name,
        "road_name": road_name,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit
    }
    if start_time and end_time:
        params["start_time"] = start_time
        params["end_time"] = end_time

    result = db.execute(text(query), params).fetchall()

    return [
        {
            "road_name": row[2],
            "structure_geom_wkt": row[1],
            "structure_type": STRUCTURE_LABELS.get(row[3], row[3]),
            "num_accidents": row[0]
        }
        for row in result
    ]

