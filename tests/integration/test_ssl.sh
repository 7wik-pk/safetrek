#!/bin/bash
DOMAIN=${1:-7wik-pk.online}
echo "Checking SSL certificate for $DOMAIN..."

openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" < /dev/null 2>/dev/null | openssl x509 -noout -dates
