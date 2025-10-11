# 🚧 API Documentation

## Region Accidents Endpoint
`POST /accident_stats`

Returns accident statistics grouped by SA2 or SA3 areas within a specified SA2/SA3/SA4 region. Results include accident counts, spatial density, and centroid coordinates.

---

### 🔐 Required Parameters

| **Field**             | **Type**   | **Description** |
|-----------------------|------------|------------------|
| `filter_area_level`   | `string`   | Area level to filter by. Valid values:<br>`"sa2"`, `"sa3"`, `"sa4"` |
| `filter_area_name`    | `string`   | Name of the area to filter (case-insensitive match) |
| `group_by_area_level` | `string`   | Area level to group results by. Valid values:<br>`"sa2"`, `"sa3"`<br>**Must not be higher than `filter_area_level`** |

---

### 🗓️ Optional Filters

| **Field**     | **Type** | **Description** |
|---------------|----------|-----------------|
| `date_from`   | `date`   | Start date for filtering accidents |
| `date_to`     | `date`   | End date for filtering accidents |

Dates should be provided as strings of the form "yyyy-MM-dd", for example "2020-01-01"

---

### 📐 Ordering & Limits

| **Field**     | **Type**   | **Description** |
|---------------|------------|-----------------|
| `order_by`    | `string`   | Sort results by:<br>`"count"` or `"density"`<br>**Default:** `"count"` |
| `order_dir`   | `string`   | Sort direction:<br>`"asc"` or `"desc"`<br>**Default:** `"desc"` |
| `limit`       | `int`      | Max number of results to return<br>**Default:** `10`, range: `1–100` |

---

### 📦 Response Format

Returns a list of grouped areas with accident statistics:

```json
[
  {
    "sa_name": "Example SA2",
    "num_accs": 42,
    "geom_area_sq_km": 12.34,
    "acc_per_sq_km": 3.4,
    "centroid_lat": -37.812,
    "centroid_lon": 144.963,
    "geom": "MULTIPOLYGON(...)"
  },
  ...
]
```

## Road Accident Density Endpoint
`POST /road_accident_density`

Returns accident density statistics for roads within a specified SA3 region, filtered by road type and optional accident/person conditions.

---

### 🔐 Required Parameters

| **Field**     | **Type** | **Description** |
|---------------|----------|-----------------|
| `sa_level`    | `string` | Level of the region within which road data is to be queried - can either be `sa2` or `sa3` |
| `sa_name`    | `string` | SA2/SA3 region name (e.g. `"monash"`) |
| `road_type`   | `string` | Road classification. Valid values:<br>`commerical_and_civic`, `infrastructure`, `major`, `pedestrian_and_recreational_paths`, `rural_and_low_traffic`, `suburban`<br>**Default:** `"major"` |

---

### 🗓️ Date Defaults

- If `road_type = "major"` → `date_from = 2023-01-01`, `date_to = 2024-12-31`
- Otherwise → `date_from = 2020-01-01`, `date_to = 2024-12-31`

---

### 🧩 Optional Filters

| **Field**                  | **Type**   | **Description** |
|----------------------------|------------|------------------|
| `date_from`, `date_to`     | `string`     | Override default date range - provide dates as strings of the form "yyyy-MM-dd", for example "2020-01-01" |
| `time_from`, `time_to`     | `string`     | Filter by accident time - provide times as strings of the form "hh:mm:ss" |
| `severity`                 | `string`   | `"fatal accident"`, `"non injury accident"`, `"other injury accident"`, `"serious injury accident"` |
| `speed_zone`               | `string`   | `"100 km/hr"`, `"110 km/hr"`, `"30km/hr"`, `"40 km/hr"`, `"50 km/hr"`, `"60 km/hr"`, `"70 km/hr"`, `"75 km/hr"`, `"80 km/hr"`, `"90 km/hr"`, `"camping grounds or off road"` |
| `age_group`                | `string`   | Age group of involved person(s) - valid values are `"0-4"`, `"5-12"`, `"13-15"`, `"16-17"`, `"18-21"`, `"22-25"`, `"26-29"`, `"30-39"`, `"40-49"`, `"50-59"`, `"60-64"`, `"65-69"`, `"70+"` |
| `sex`                      | `string`   | `"M"`, `"F"`, `"U"` |
| `road_user_type_desc`      | `string`   | `"bicyclists"`, `"drivers"`, `"e-scooter rider"`, `"motorcyclists"`, `"not known"`, `"passengers"`, `"pedestrians"`, `"pillion passengers"` |
| `victims_hospitalised`     | `string`   | `"y"` or `"n"` |
| `atmosph_cond_desc`        | `string`   | `"clear"`, `"dust"`, `"fog"`, `"not known"`, `"raining"`, `"smoke"`, `"snowing"`, `"strong winds"` |
| `min_accidents_per_road`   | `int`      | Minimum accident count per road |
| `min_road_length_km`       | `float`    | Minimum road length in km<br>**Default:** `0.2` |
| `order_by`                 | `string`   | `"accident_count"` or `"accident_density_per_km"`<br>**Default:** `"accident_density_per_km"` |
| `order_desc`               | `bool`     | Sort descending<br>**Default:** `true` |
| `limit`                    | `int`      | Max results<br>**Default:** `5`, range: `1–100` |

---

### 📦 Response Format

Returns a list of roads with accident density metrics:

```json
[
  {
    "road_name": "Clayton Road",
    "accident_count": 12,
    "road_length_km": 1.8,
    "accident_density_per_km": 6.67,
    "road_geom": "...",          // WKB geometry
    "acc_geom_union": "..."      // WKB geometry
  },
  ...
]
```

## 🚧 GET `/corridor_crash_density`

Returns crash density statistics for segments of a specified road within a given SA2 or SA3 region. Useful for identifying high-risk corridors based on crash count or crash density (accidents per km).

---

### 🔧 Query Parameters

| Name            | Type                          | Required | Description |
|-----------------|-------------------------------|----------|-------------|
| `region_level`  | `"sa2"` or `"sa3"`             | ✅ Yes   | The spatial aggregation level to filter by. |
| `region_name`   | `string`                      | ✅ Yes   | Name of the SA2 or SA3 region (case-insensitive). |
| `road_name`     | `string`                      | ✅ Yes   | Name of the road to analyze (e.g., `"Clayton Road"`). |
| `start_date`    | `YYYY-MM-DD`                  | ✅ Yes   | Start of the accident date range. |
| `end_date`      | `YYYY-MM-DD`                  | ✅ Yes   | End of the accident date range. |
| `start_time`    | `HH:MM:SS`                    | ❌ No    | Start of the accident time range (optional). |
| `end_time`      | `HH:MM:SS`                    | ❌ No    | End of the accident time range (optional). |
| `order_by`      | `"density"` or `"count"`      | ❌ No    | Sort results by crash density (`accidents_per_km`) or raw count (`num_accidents`). Default: `"density"`. |
| `order_dir_asc` | `true` or `false`             | ❌ No    | Sort in ascending order if `true`, descending if `false`. Default: `false`. |

---

### 📦 Response Format

Returns a list of up to 10 road segments with crash statistics:

```json
[
  {
    "road_name": "Clayton Road",
    "segment_geom_wkt": "LINESTRING(145.123 -37.912, 145.125 -37.913)",
    "segment_type": "Road Segment",
    "num_accidents": 8,
    "accidents_per_km": 42.8
  },
  ...
]
```

## 🚧 GET `/blackspot_crash_density`

Returns crash counts for road structures (e.g., roundabouts, bridges) located along a specified road within a given SA2 or SA3 region. Useful for identifying high-risk blackspots based on structure type and proximity to crash clusters.

---

### 🔧 Query Parameters

| Name             | Type                          | Required | Description |
|------------------|-------------------------------|----------|-------------|
| `region_level`   | `"sa2"` or `"sa3"`             | ✅ Yes   | The spatial aggregation level to filter by. |
| `region_name`    | `string`                      | ✅ Yes   | Name of the SA2 or SA3 region (case-insensitive). |
| `road_name`      | `string`                      | ✅ Yes   | Name of the road to analyze (e.g., `"Clayton Road"`). |
| `start_date`     | `YYYY-MM-DD`                  | ✅ Yes   | Start of the accident date range. |
| `end_date`       | `YYYY-MM-DD`                  | ✅ Yes   | End of the accident date range. |
| `start_time`     | `HH:MM:SS`                    | ❌ No    | Start of the accident time range (optional). |
| `end_time`       | `HH:MM:SS`                    | ❌ No    | End of the accident time range (optional). |
| `structure_types`| `List[str]`                   | ❌ No    | Optional list of structure types to filter by. Valid values include:<br>• `bridge`<br>• `road`<br>• `roundabout`<br>• `tunnel`<br>• `foot_bridge` |
| `order_dir_asc`  | `true` or `false`             | ❌ No    | Sort results in ascending order if `true`, descending if `false`. Default: `false`. |
| `limit`          | `integer`                     | ❌ No    | Maximum number of results to return. Default: `10`. |

---

### 📦 Response Format

Returns a list of up to `limit` structures with crash statistics:

```json
[
  {
    "road_name": "Clayton Road",
    "structure_geom_wkt": "POINT(145.123 -37.912)",
    "structure_type": "Roundabout",
    "num_accidents": 7
  },
  ...
]
```