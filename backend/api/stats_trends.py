from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, model_validator, conint
from fastapi import HTTPException

from typing import List, Literal, Optional, Dict, Tuple
from datetime import date, time

from db import get_db

app = APIRouter()

## accident stats endpoint

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

    # Allow equal; only forbid strictly higher
    if hierarchy.index(group_level) > hierarchy.index(filter_level):
        raise ValueError("EW RULE: group_by must NOT be higher")

    return values

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
            ST_Y(
              ST_Centroid(
                ST_Transform(s.geom, 4326)
              )
            ) AS centroid_lat,
            ST_X(
              ST_Centroid(
                ST_Transform(s.geom, 4326)
              )
            ) AS centroid_lon,
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

## trends endpoint

class YearlyTrendItem(BaseModel):
    year: conint(ge=1900, le=2100)
    crashes: int
    total_injuries: int
    serious_injuries: int

@app.get("/trends/yearly", response_model=List[YearlyTrendItem])
def get_yearly_trend(
    year_from: conint(ge=1900, le=2100) = 2020,
    year_to:   conint(ge=1900, le=2100) = 2024,
    db: Session = Depends(get_db),
):
    sql = text("""
        SELECT
          EXTRACT(YEAR FROM accident_date)::int AS year,
          COUNT(*)                               AS crashes,
          COALESCE(SUM(inj_or_fatal), 0)         AS total_injuries,
          COALESCE(SUM(seriousinjury), 0)        AS serious_injuries
        FROM accident
        WHERE accident_date BETWEEN :start_date AND :end_date
        GROUP BY year
        ORDER BY year;
    """)

    params = {
        "start_date": f"{year_from}-01-01",
        "end_date":   f"{year_to}-12-31",
    }

    rows = db.execute(sql, params).fetchall()
    return [YearlyTrendItem(**dict(r._mapping)) for r in rows]

## monthly trends endpoint (accidents + serious injuries + injuries total)

class MonthlyTrendItem(BaseModel):
    period: str              # 'YYYY-MM'
    crashes: int             # number of accidents per month
    total_injuries: int      # sum of total injuries
    serious_injuries: int    # sum of seriousinjury

class MonthlyTrendResponse(BaseModel):
    year: conint(ge=1900, le=2100)
    data: List[MonthlyTrendItem]

@app.get("/trends/monthly", response_model=MonthlyTrendResponse)
def get_monthly_trend(year: conint(ge=1900, le=2100), db: Session = Depends(get_db)):

    sql = text("""
        WITH months AS (
            SELECT generate_series(1, 12) AS m
        ),
        agg AS (
            SELECT
              EXTRACT(MONTH FROM accident_date)::int AS m,
              COUNT(*)                                AS crashes,
              COALESCE(SUM(inj_or_fatal), 0)          AS total_injuries,
              COALESCE(SUM(seriousinjury), 0)         AS serious_injuries
            FROM accident
            WHERE EXTRACT(YEAR FROM accident_date) = :year
            GROUP BY 1
        )
        SELECT
          to_char(make_date(:year, months.m, 1), 'YYYY-MM') AS period,
          COALESCE(agg.crashes, 0)                          AS crashes,
          COALESCE(agg.total_injuries, 0)                   AS total_injuries,
          COALESCE(agg.serious_injuries, 0)                 AS serious_injuries
        FROM months
        LEFT JOIN agg ON agg.m = months.m
        ORDER BY period;
    """)

    rows = db.execute(sql, {"year": year}).fetchall()
    data = [MonthlyTrendItem(**dict(row._mapping)) for row in rows]
    return MonthlyTrendResponse(year=year, data=data)

class ForecastYearlyResponse(BaseModel):
    method: Literal["ols", "mean"]
    history: List[YearlyTrendItem]   # 2012-2024 yearly totals
    forecast_year: conint(ge=1900, le=2100)
    forecast: YearlyTrendItem
    model_info: Optional[Dict[str, Dict[str, float]]] = None  # slopes/intercepts (if ols)

def ols_fit(xs: List[int], ys: List[float]) -> Tuple[float, float]:
    # OLS: y = a + b*x
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    sxx = sum((x - mean_x) ** 2 for x in xs) or 1e-9
    sxy = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    b = sxy / sxx
    a = mean_y - b * mean_x
    return a, b

@app.get("/forecast/yearly", response_model=ForecastYearlyResponse)
def forecast_yearly(
    year_from: conint(ge=1900, le=2100) = 2012,
    year_to:   conint(ge=1900, le=2100) = 2024,
    target_year: conint(ge=1900, le=2100) = 2025,
    method: Literal["ols", "mean"] = "ols",
    db: Session = Depends(get_db),
):
    sql = text("""
        SELECT
          EXTRACT(YEAR FROM accident_date)::int AS y,
          COUNT(*)                               AS crashes,
          COALESCE(SUM(inj_or_fatal), 0)         AS total_injuries,
          COALESCE(SUM(seriousinjury), 0)        AS serious_injuries
        FROM accident
        WHERE accident_date BETWEEN :start_date AND :end_date
        GROUP BY y
        ORDER BY y;
    """)
    rows = db.execute(sql, {
        "start_date": f"{year_from}-01-01",
        "end_date":   f"{year_to}-12-31",
    }).fetchall()

    # Pack history
    years = list(range(year_from, year_to + 1))
    by_year: Dict[int, Dict[str, int]] = {y: {"crashes": 0, "total_injuries": 0, "serious_injuries": 0} for y in years}
    for r in rows:
        m = r._mapping
        by_year[m["y"]] = {
            "crashes": m["crashes"],
            "total_injuries": m["total_injuries"],
            "serious_injuries": m["serious_injuries"],
        }
    history = [YearlyTrendItem(year=y, **by_year[y]) for y in years]

    if not history:
        raise HTTPException(status_code=404, detail="No data in the specified range.")

    # Forecast per metric
    metrics = ["crashes", "total_injuries", "serious_injuries"]
    xs = years
    model_info: Dict[str, Dict[str, float]] = {}
    forecast_vals: Dict[str, int] = {}

    for k in metrics:
        ys = [float(getattr(h, k)) for h in history]
        if method == "mean":
            yhat = sum(ys) / len(ys)
            model_info[k] = {"mean": yhat}
        else:  # "ols"
            a, b = ols_fit(xs, ys) # y = a + b * year
            yhat = a + b * target_year
            model_info[k] = {"intercept": a, "slope": b, "fitted_for_target": yhat}
        # round & non-negative
        forecast_vals[k] = max(0, int(round(yhat)))

    forecast_row = YearlyTrendItem(
        year=target_year,
        crashes=forecast_vals["crashes"],
        total_injuries=forecast_vals["total_injuries"],
        serious_injuries=forecast_vals["serious_injuries"],
    )

    return ForecastYearlyResponse(
        method=method,
        history=history,
        forecast_year=target_year,
        forecast=forecast_row,
        model_info=model_info if method == "ols" else None
    )

## roads within region endpoint
class RoadAccidentDensityRequest(BaseModel):
    sa_level: Literal["sa2", "sa3"]  # required param
    sa_name: str  # required - SA2/SA3 name

    road_type: Literal[
        "commerical_and_civic", "infrastructure", "major",
        "pedestrian_and_recreational_paths", "rural_and_low_traffic", "suburban"
    ] = "major"

    date_from: Optional[date] = None
    date_to: Optional[date] = None

    time_from: Optional[time] = None
    time_to: Optional[time] = None

    severity: Optional[
        Literal["fatal accident", "non injury accident", "other injury accident", "serious injury accident"]
    ] = None

    speed_zone: Optional[
        Literal[
            "100 km/hr", "110 km/hr", "30km/hr", "40 km/hr", "50 km/hr", "60 km/hr",
            "70 km/hr", "75 km/hr", "80 km/hr", "90 km/hr", "camping grounds or off road"
        ]
    ] = None

    age_group: Optional[str] = None
    sex: Optional[Literal["M", "F", "U"]] = None
    road_user_type_desc: Optional[
        Literal[
            "bicyclists", "drivers", "e-scooter rider", "motorcyclists", "not known",
            "passengers", "pedestrians", "pillion passengers"
        ]
    ] = None

    victims_hospitalised: Optional[Literal["y", "n"]] = None

    atmosph_cond_desc: Optional[
        Literal["clear", "dust", "fog", "not known", "raining", "smoke", "snowing", "strong winds"]
    ] = None

    min_accidents_per_road: Optional[int] = None
    min_road_length_km: Optional[float] = 0.2

    order_by: Literal["accident_count", "accident_density_per_km"] = "accident_density_per_km"
    order_desc: bool = True

    limit: conint(ge=1, le=100) = 5

    @model_validator(mode="before")
    def set_default_dates(cls, values):
        road_type = values.get("road_type", "major")
        if not values.get("date_from"):
            values["date_from"] = date(2023, 1, 1) if road_type == "major" else date(2020, 1, 1)
        if not values.get("date_to"):
            values["date_to"] = date(2024, 12, 31)
        return values

@app.post("/road_accident_density")
def get_road_accident_density(req: RoadAccidentDensityRequest, db: Session = Depends(get_db)):
    
    sa_column = {
        "sa2": "sa2_name21",
        "sa3": "sa3_name21",
        # "sa4": "sa4_name21"
    }[req.sa_level]

    filters = [
        f"lower(mbv.{sa_column}) = lower(:sa_name)",
        "h_road_type = :road_type",
        "accident_date BETWEEN :date_from AND :date_to"
    ]

    if req.time_from and req.time_to:
        filters.append("a.accident_time BETWEEN :time_from AND :time_to")
    if req.severity:
        filters.append("lower(a.severity) = lower(:severity)")
    if req.speed_zone:
        filters.append("lower(a.speed_zone) = lower(:speed_zone)")
    if req.age_group:
        filters.append("p.age_group = :age_group")
    if req.sex:
        filters.append("p.sex = :sex")
    if req.road_user_type_desc:
        filters.append("lower(p.road_user_type_desc) = lower(:road_user_type_desc)")
    if req.victims_hospitalised:
        filters.append("lower(p.taken_hospital) = :victims_hospitalised")
    if req.atmosph_cond_desc:
        filters.append("lower(ac.atmosph_cond_desc) = lower(:atmosph_cond_desc)")

    having_clause = []
    if req.min_accidents_per_road:
        having_clause.append("COUNT(*) > :min_accidents_per_road")
    if req.min_road_length_km is not None:
        having_clause.append("st_length(r.geom::geography)/1000 > :min_road_length_km")

    sql = text(f"""
        WITH sax AS (
            SELECT ST_Union(mbv.geom) AS geom
            FROM mesh_block_vic_21 mbv
            WHERE {filters[0]}
        ),
        roads_in_sax AS (
            SELECT ST_Union(vr.geom) AS geom, vr.ezirdnmlbl AS road_name
            FROM vicmap_road vr, sax
            WHERE ST_Intersects(vr.geom, sax.geom)
              AND {filters[1]}
            GROUP BY road_name
        ),
        accidents_in_sax AS (
            SELECT a.geom
            FROM accident a
            JOIN person p ON a.accident_no = p.accident_no
            JOIN accident_conditions ac ON a.accident_no = ac.accident_no,
            sax
            WHERE ST_Intersects(a.geom, sax.geom)
              AND {filters[2]}
              {"AND " + " AND ".join(filters[3:]) if len(filters) > 3 else ""}
        )
        SELECT
            r.road_name,
            ST_AsText(ST_Union(a.geom)::geography) AS acc_geom_union,
            ST_AsText(r.geom::geography) AS road_geom,
            COUNT(*) AS accident_count,
            ST_Length(r.geom::geography)/1000 AS road_length_km,
            COUNT(*)/(ST_Length(r.geom::geography)/1000) AS accident_density_per_km
        FROM accidents_in_sax a
        JOIN LATERAL (
            SELECT road_name, rm.geom
            FROM roads_in_sax rm
            ORDER BY rm.geom <-> a.geom
            LIMIT 1
        ) r ON true
        WHERE ST_DWithin(a.geom::geography, r.geom::geography, 5)
        GROUP BY r.road_name, r.geom
        {"HAVING " + " AND ".join(having_clause) if having_clause else ""}
        ORDER BY {req.order_by} {"DESC" if req.order_desc else "ASC"}
        LIMIT :limit
    """)

    params = req.model_dump()
    result = db.execute(sql, params).fetchall()
    return [dict(row._mapping) for row in result]
