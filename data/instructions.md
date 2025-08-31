<h1>Instructions</h1>

Before you can run the Dockerfile or setup the PostGreSQL database locally, you need to download raw data.

There are 2 ways of doing this:

1. Download the readymade .zip from Google Drive: https://drive.google.com/file/d/11Avlz0j24QAZB5LQfaP9rboDofuYKiMc/view?usp=sharing

    Extract all the contents of this zip file directly into the same folder as this instructions file and run `docker compose up -d`

    This zip file contains data as of 30th August, 2025.

2. The official way [NOT recommended for local testing]

    Download the latest data from the following official sources and name them appropriately, and then - at the end - run `docker compose up -d`:

<h2>Victorian Road Crash Data (3 CSVs)</h2>

1. Download the following CSVs in the same directory as this instructions.md file:

victorian_road_crash_data.csv : https://discover.data.vic.gov.au/dataset/victoria-road-crash-data/resource/5df1f373-0c90-48f5-80e1-7b2a35507134

person.csv : https://discover.data.vic.gov.au/dataset/victoria-road-crash-data/resource/60c8fc0c-2806-40f3-bb33-5c52691120e8

atmospheric_cond.csv : https://discover.data.vic.gov.au/dataset/victoria-road-crash-data/resource/891a8e3a-2fbd-4974-badc-b5616c25b0ab

and then run the provided `read_csvs.sql` script - **you might need to change the paths** to all the CSVs in this .sql script for the initial setup, but **PLEASE DON'T PUSH the updates** to this file.

<h2>Victorian Mesh Block Data</h2>

1. Download the `Mesh Blocks - 2021 - Shapefile` .zip [217.44 MB] from this page - https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files

2. Extract all the files within the downloaded .zip into a directory named `MB_2021_AUST_SHP_GDA2020` here

3. And then run the following `ogr2ogr` command (lookup how to install `ogr2ogr` if you don't have it):

```
ogr2ogr PG:"dbname=strek user=postgres" "/data/MB_2021_AUST_SHP_GDA2020/MB_2021_AUST_GDA2020.shp" -nln mesh_block_vic_21 -where "STE_CODE21 = '2'" -lco GEOMETRY_NAME=geom -overwrite -nlt MULTIPOLYGON
```

<h2>VicMap Road Network Data</h2>

<h3>Downloading the official way [NOT recommended for local testing]</h3>

This data is originally procured from https://discover.data.vic.gov.au/dataset/vicmap-transport - but this method requires sign-in and waiting for the link to the dataset to be sent by email.

In this method, you will receive a download link to a .zip file with a name of the form `Order_XXXXXX.zip` which contains several shapefiles in the path `ll_gda2020/esrishape/whole_of_dataset/victoria/VMTRANS/` inside the .zip, but we will only be importing `TR_ROAD.shp` & `TR_ROAD_INFRASTRUCTURE.shp` for SafeTrek's operation as of now [subject to change].

<h3>Downloading ready data for local development</h3>

Extract only the necessary shapefiles (`TR_ROAD.*` & `TR_ROAD_INFRASTRUCTURE.*`) inside the zip file from the Google Drive link into a directory named `vicmap_road` and run the following ogr2ogr commands:

```
ogr2ogr PG:"dbname=strek user=postgres" /data/vicmap_road/TR_ROAD.shp -nln vicmap_road -lco GEOMETRY_NAME=geom -nlt MULTILINESTRING

ogr2ogr PG:"dbname=strek user=postgres" /data/vicmap_road/TR_ROAD_INFRASTRUCTURE.shp -nln vicmap_road_structures -lco GEOMETRY_NAME=geom -nlt POINT
```
