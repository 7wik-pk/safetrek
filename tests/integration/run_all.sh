#!/bin/bash
DOMAIN=${1:-7wik-pk.online}
echo "Running all integration tests on domain $DOMAIN..."
echo "================================="
./tests/integration/test_backend.sh "$DOMAIN"
echo "================================="
./tests/integration/test_ssl.sh "$DOMAIN"
echo "================================="
./tests/integration/test_proxy.sh "$DOMAIN"
echo "================================="
# docker exec -i strek-db psql -U postgres -d strek < tests/integration/test_db.sql 
./tests/integration/test_db.sh
echo "================================="
echo "All integration tests completed"