#!/bin/bash
DOMAIN=${1:-7wik-pk.online}
echo "Checking SSL certificate for $DOMAIN..."

CERT_INFO=$(openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" < /dev/null 2>/dev/null | openssl x509 -noout -dates)

if [[ $CERT_INFO == *"notBefore"* && $CERT_INFO == *"notAfter"* ]]; then
  echo "$CERT_INFO"
  echo "SSL certificate is valid"
else
  echo "SSL certificate check failed"
fi
