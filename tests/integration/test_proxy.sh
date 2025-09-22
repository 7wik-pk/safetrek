#!/bin/bash
DOMAIN=${1:-7wik-pk.online}
echo "Testing nginx proxy routing..."

curl -I "https://$DOMAIN" | grep -q "200 OK" && echo "Proxy routing OK" || echo "ERROR: Proxy routing failed"
