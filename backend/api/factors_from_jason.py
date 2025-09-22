from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from db import get_db

app = APIRouter()

class FactorCountItem(BaseModel):
    category: str
    severity: str
    count: int

ORDER_CASES = {
    "time_bucket": """
        CASE category
          WHEN 'Late Night' THEN 1
          WHEN 'Morning'    THEN 2
          WHEN 'Afternoon'  THEN 3
          WHEN 'Evening'    THEN 4
          ELSE 99
        END
    """,
    "light_condition": """
        CASE category
          WHEN 'Day'                      THEN 1
          WHEN 'Dusk/Dawn'                THEN 2
          WHEN 'Dark Street light on'     THEN 3
          WHEN 'Dark Street light off'    THEN 4
          WHEN 'Dark Street light unknown' THEN 5
          WHEN 'Dark No street lights'    THEN 6
          ELSE 99
        END
    """,
    "road_geometry": """
        CASE category
          WHEN 'Cross intersection'    THEN 1
          WHEN 'Not at intersection'   THEN 2
          WHEN 'Y intersection'        THEN 3
          WHEN 'T intersection'        THEN 4
          WHEN 'Multiple intersection' THEN 5
          WHEN 'Private property'      THEN 6
          WHEN 'Dead end'              THEN 7
          WHEN 'Road closure'          THEN 8
          ELSE 99
        END
    """,
    "speed_zone": """
        CASE category
          WHEN 'below 40'  THEN 1
          WHEN '50 to 60'  THEN 2
          WHEN '70 to 80'  THEN 3
          WHEN '80 to 90'  THEN 4
          WHEN 'above 100' THEN 5
          ELSE 99
        END
    """,
    "atmospheric_condition": """
        CASE category
          WHEN 'Clear'        THEN 1
          WHEN 'Fog'          THEN 2
          WHEN 'Snowing'      THEN 3
          WHEN 'Smoke'        THEN 4
          WHEN 'Raining'      THEN 5
          WHEN 'Strong winds' THEN 6
          WHEN 'Dust'         THEN 7
          ELSE 99
        END
    """,
    "sex": """
        CASE category
          WHEN 'M' THEN 1
          WHEN 'F' THEN 2
          ELSE 99
        END
    """,
    "age_group": """
        CASE category
          WHEN '0-17' THEN 1
          WHEN '18-25' THEN 2
          WHEN '26-39' THEN 3
          WHEN '40-59' THEN 4
          WHEN '60-69' THEN 5
          WHEN '70+'   THEN 6
          ELSE 99
        END
    """,
    "helmet_belt_worn": """
        CASE category
          WHEN 'worn'     THEN 1
          WHEN 'not worn' THEN 2
          ELSE 99
        END
    """
}

VALID_FACTORS = set(ORDER_CASES.keys())

@app.get("/factor_counts", response_model=List[FactorCountItem])
def get_factor_counts(
    factor: str = Query(..., description="factor: time_bucket | light_condition | road_geometry | speed_zone | atmospheric_condition | sex | age_group | helmet_belt_worn"),
    db: Session = Depends(get_db),
):
    if factor not in VALID_FACTORS:
        raise HTTPException(status_code=400, detail=f"Invalid factor: {factor}")

    order_by = ORDER_CASES[factor]

    # --- Accident-based factors ---
    if factor in ["time_bucket", "light_condition", "road_geometry", "speed_zone", "atmospheric_condition"]:
        if factor == "time_bucket":
            sql = f"""
                WITH accident_prepared AS (
                  SELECT
                    a.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    CASE
                      WHEN a.accident_time IS NULL THEN 'Unknown'
                      WHEN EXTRACT(HOUR FROM a.accident_time) BETWEEN 0  AND 5  THEN 'Late Night'
                      WHEN EXTRACT(HOUR FROM a.accident_time) BETWEEN 6  AND 11 THEN 'Morning'
                      WHEN EXTRACT(HOUR FROM a.accident_time) BETWEEN 12 AND 17 THEN 'Afternoon'
                      ELSE 'Evening'
                    END AS category
                  FROM accident a
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                )
                SELECT category, severity, COUNT(*) AS count
                FROM accident_prepared
                WHERE severity IS NOT NULL AND category IS NOT NULL
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        elif factor == "light_condition":
            sql = f"""
                WITH accident_prepared AS (
                  SELECT
                    a.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    a.light_condition AS category
                  FROM accident a
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                    AND a.light_condition IS NOT NULL
                    AND a.light_condition <> 'Unk.'
                )
                SELECT category, severity, COUNT(*) AS count
                FROM accident_prepared
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        elif factor == "road_geometry":
            sql = f"""
                WITH accident_prepared AS (
                  SELECT
                    a.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    a.road_geometry AS category
                  FROM accident a
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                    AND a.road_geometry IS NOT NULL
                    AND a.road_geometry <> 'Unknown'
                )
                SELECT category, severity, COUNT(*) AS count
                FROM accident_prepared
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        elif factor == "speed_zone":
            sql = f"""
                WITH accident_prepared AS (
                  SELECT
                    a.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    CASE
                      WHEN REPLACE(TRIM(a.speed_zone), ' ', '') IN ('30km/hr','40km/hr') THEN 'below 40'
                      WHEN REPLACE(TRIM(a.speed_zone), ' ', '') IN ('50km/hr','60km/hr') THEN '50 to 60'
                      WHEN REPLACE(TRIM(a.speed_zone), ' ', '') IN ('70km/hr','75km/hr','80km/hr') THEN '70 to 80'
                      WHEN REPLACE(TRIM(a.speed_zone), ' ', '') =  '90km/hr' THEN '80 to 90'
                      WHEN REPLACE(TRIM(a.speed_zone), ' ', '') IN ('100km/hr','110km/hr') THEN 'above 100'
                      ELSE NULL
                    END AS category
                  FROM accident a
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                    AND REPLACE(TRIM(a.speed_zone), ' ', '') IN (
                        '30km/hr','40km/hr','50km/hr','60km/hr',
                        '70km/hr','75km/hr','80km/hr','90km/hr','100km/hr','110km/hr'
                    )
                )
                SELECT category, severity, COUNT(*) AS count
                FROM accident_prepared
                WHERE category IS NOT NULL AND severity IS NOT NULL
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        else:  # atmospheric_condition from accident_conditions table
            sql = f"""
                WITH accident_prepared AS (
                  SELECT
                    a.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    ac.atmosph_cond_desc AS category
                  FROM accident a
                  JOIN accident_conditions ac
                    ON ac.accident_no = a.accident_no
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                    AND ac.atmosph_cond_desc IN ('Clear','Fog','Snowing','Smoke','Raining','Strong winds','Dust')
                )
                SELECT category, severity, COUNT(*) AS count
                FROM accident_prepared
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """

    # ----- Person-based factors -----
    else:
        if factor == "sex":
            sql = f"""
                WITH person_prepared AS (
                  SELECT
                    p.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    CASE
                      WHEN UPPER(p.sex) IN ('M','F') THEN UPPER(p.sex)
                      ELSE NULL
                    END AS category
                  FROM person p
                  JOIN accident a ON a.accident_no = p.accident_no
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                )
                SELECT category, severity, COUNT(*) AS count
                FROM person_prepared
                WHERE category IS NOT NULL AND severity IS NOT NULL
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        elif factor == "age_group":
            sql = f"""
                WITH person_prepared AS (
                  SELECT
                    p.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    CASE
                      WHEN p.age_group IN ('0-4','5-12','13-15','16-17') THEN '0-17'
                      WHEN p.age_group IN ('18-21','22-25') THEN '18-25'
                      WHEN p.age_group IN ('26-29','30-39') THEN '26-39'
                      WHEN p.age_group IN ('40-49','50-59') THEN '40-59'
                      WHEN p.age_group IN ('60-64','65-69') THEN '60-69'
                      WHEN p.age_group = '70+' THEN '70+'
                      ELSE NULL 
                    END AS category
                  FROM person p
                  JOIN accident a ON a.accident_no = p.accident_no
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                )
                SELECT category, severity, COUNT(*) AS count
                FROM person_prepared
                WHERE category IS NOT NULL AND severity IS NOT NULL
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """
        else:  # helmet_belt_worn
            sql = f"""
                WITH person_prepared AS (
                  SELECT
                    p.accident_no,
                    CASE
                      WHEN a.severity = 'Other injury accident'   THEN 'Injury'
                      WHEN a.severity = 'Serious injury accident' THEN 'SeriousInjury'
                      ELSE NULL
                    END AS severity,
                    CASE
                      WHEN TRIM(COALESCE(p.helmet_belt_worn::text, '')) IN ('1','3','6') THEN 'worn'
                      WHEN TRIM(COALESCE(p.helmet_belt_worn::text, '')) IN ('2','4','5','7') THEN 'not worn'
                      ELSE NULL
                    END AS category
                  FROM person p
                  JOIN accident a ON a.accident_no = p.accident_no
                  WHERE a.severity IN ('Other injury accident', 'Serious injury accident')
                )
                SELECT category, severity, COUNT(*) AS count
                FROM person_prepared
                WHERE category IS NOT NULL AND severity IS NOT NULL
                GROUP BY category, severity
                ORDER BY {order_by}, severity;
            """

    # rows = db.execute(text(sql)).mappings().all()
    # return [FactorCountItem(**r) for r in rows]
    rows = db.execute(text(sql)).fetchall()
    return [dict(r._mapping) for r in rows]