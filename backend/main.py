from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, model_validator, conint
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Literal, Optional, List, Dict
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

load_dotenv(".env")  # Load variables from .env file

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    allowed_origins_raw: str = ""  # Raw string from .env

    @property
    def allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]

    class Config:
        env_file = ".env"

settings = Settings()

# --- Database setup ---
engine = create_engine(settings.database_url, echo=True)
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

allowed_origins = settings.allowed_origins or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

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
# --- Yearly trend (accidents + serious injuries + injuries total) ---

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

# --- Monthly trend (accidents + serious injuries + injuries total) ---

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

def ols_fit(xs: List[int], ys: List[float]) -> (float, float):
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
