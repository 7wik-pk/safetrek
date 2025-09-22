#!/bin/bash
DOMAIN=${1:-7wik-pk.online}
echo "Running all integration tests..."

./tests/integration/test_backend.sh "$DOMAIN"
./tests/integration/test_ssl.sh "$DOMAIN"
./tests/integration/test_proxy.sh "$DOMAIN"
docker exec -i strek-db psql -U postgres -d strek < tests/integration/test_db.sql
