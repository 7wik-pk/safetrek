FROM postgres:16

ENV DEBIAN_FRONTEND=noninteractive
ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=pass \
    POSTGRES_DB=strek

# Install PostGIS and GDAL
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgis postgresql-16-postgis-3 gdal-bin \
    && rm -rf /var/lib/apt/lists/* 

# Copy data and scripts
# COPY MB_2021_AUST_SHP_GDA2020/ /data/MB_2021_AUST_SHP_GDA2020
# COPY vicmap_road /data/vicmap_road
# COPY *.csv /data/

# COPY ./read_csvs.sql /docker-entrypoint-initdb.d/read_csvs.sql
COPY ./import_shp.sh /docker-entrypoint-initdb.d/import_shp.sh

EXPOSE 5432
