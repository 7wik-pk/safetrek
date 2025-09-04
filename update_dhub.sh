docker compose build

docker tag safetrek-postgis 7wikmonash/safetrek-postgis
docker tag safetrek-backend 7wikmonash/safetrek-backend
docker tag safetrek-frontend 7wikmonash/safetrek-frontend

docker push 7wikmonash/safetrek-postgis
docker push 7wikmonash/safetrek-backend
docker push 7wikmonash/safetrek-frontend

## on cloud VM:
# docker compose pull
# docker compose up -d