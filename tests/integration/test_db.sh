#!/bin/bash
echo "Testing database connectivity and table integrity..."

check_table_count() {
  TABLE=$1
  EXPECTED_MIN=$2
  COUNT=$(docker exec -i strek-db psql -U postgres -d strek -t -c "SELECT COUNT(*) FROM $TABLE;" 2>/dev/null | xargs)

  if [[ "$COUNT" =~ ^[0-9]+$ ]] && [ "$COUNT" -ge "$EXPECTED_MIN" ]; then
    echo "$TABLE has $COUNT rows"
  else
    echo "$TABLE check failed or has too few rows (found: $COUNT)"
  fi
}

# Run checks
docker exec -i strek-db psql -U postgres -d strek -c "\conninfo" >/dev/null && echo "Connected to DB" || echo "Failed to connect to DB"

check_table_count "accident" 100000
check_table_count "mesh_block_vic_21" 50000
check_table_count "vicmap_road" 500000

