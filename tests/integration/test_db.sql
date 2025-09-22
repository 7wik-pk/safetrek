-- Run this inside the PostGIS container using psql
\conninfo
SELECT COUNT(*) FROM accident;
SELECT COUNT(*) FROM mesh_block_vic_21;
SELECT COUNT(*) FROM vicmap_road;

-- usage : docker exec -i safetrek-postgis psql -U postgres -d safetrek < tests/integration/test_db.sql
