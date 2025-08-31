#!/bin/sh
set -e

PGUSER=${POSTGRES_USER:-postgres}
PGDB=${POSTGRES_DB:-strek}
PGPASSWORD=${POSTGRES_PASSWORD:-pass}

export PGPASSWORD="$PGPASSWORD"

# Wait for Postgres to be ready
until pg_isready -U "$PGUSER" -d "$PGDB"; do
  echo "Waiting for database..."
  sleep 2
done


psql -U "$PGUSER" -d "$PGDB" -c "CREATE EXTENSION IF NOT EXISTS postgis;"

echo "Running read_csvs.sql..."
psql -U "$PGUSER" -d "$PGDB" -f /data/read_csvs.sql

# Run your ogr2ogr commands
echo "Importing mesh blocks..."
ogr2ogr PG:"dbname=$PGDB user=$PGUSER" /data/MB_2021_AUST_SHP_GDA2020/MB_2021_AUST_GDA2020.shp \
  -nln mesh_block_vic_21 -where "STE_CODE21 = '2'" -lco GEOMETRY_NAME=geom -overwrite -nlt MULTIPOLYGON

echo "Importing VicMap road data..."
ogr2ogr PG:"dbname=$PGDB user=$PGUSER" /data/vicmap_road/TR_ROAD.shp \
  -nln vicmap_road -lco GEOMETRY_NAME=geom -nlt MULTILINESTRING

echo "Importing VicMap road structures data..."
ogr2ogr PG:"dbname=$PGDB user=$PGUSER" /data/vicmap_road/TR_ROAD_INFRASTRUCTURE.shp \
  -nln vicmap_road_structures -lco GEOMETRY_NAME=geom -nlt POINT

echo "Running final_db_updates.sql..."
psql -U "$PGUSER" -d "$PGDB" -f /data/final_db_updates.sql