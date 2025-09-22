#!/bin/bash
echo "Testing backend API endpoints..."

DOMAIN=${1:-7wik-pk.online}
BASE_URL="https://$DOMAIN/api"

curl -s "$BASE_URL/health" | grep -q "ok" && echo "/api/health passed" || echo "/api/health failed"
curl -s "$BASE_URL/distinct_sa2" | grep -q "Melbourne CBD - East" && echo "/api/distinct_sa2 passed" || echo "/api/distinct_sa2 failed"
curl -s "$BASE_URL/distinct_sa3" | grep -q "Melbourne City" && echo "/api/distinct_sa3 passed" || echo "/api/distinct_sa3 failed"