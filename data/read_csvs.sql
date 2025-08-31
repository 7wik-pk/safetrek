-- csv reads

create extension if not exists postgis;

ALTER SYSTEM SET max_wal_size = '2GB';
ALTER SYSTEM SET checkpoint_timeout = '30min';
ALTER SYSTEM SET wal_writer_delay = '200ms';
ALTER SYSTEM SET shared_buffers = '512MB';
SELECT pg_reload_conf();

-- accident/crash data
DROP TABLE IF EXISTS accident;
CREATE TABLE accident (
    accident_no        CHAR(12) PRIMARY KEY,  
    accident_date      DATE,
    accident_time      TIME,
    accident_type      VARCHAR(100),          
    day_of_week        VARCHAR(30),
    dca_code           CHAR(3),               
    dca_code_description VARCHAR(100),
    light_condition    VARCHAR(100),
    police_attend      VARCHAR(100),
    road_geometry      VARCHAR(100),
    severity           VARCHAR(100),
    speed_zone         VARCHAR(100),
    run_offroad        VARCHAR(3),
    road_name          VARCHAR(50),
    road_type          VARCHAR(22),
    road_route_1       INTEGER,
    lga_name           VARCHAR(100),
    dtp_region         VARCHAR(35),
    latitude           DECIMAL(10,6),
    longitude          DECIMAL(10,6),
    vicgrid_x          NUMERIC(20,6),
    vicgrid_y          NUMERIC(20,6),
    total_persons      INTEGER,
    inj_or_fatal       INTEGER,
    fatality           INTEGER,
    seriousinjury      INTEGER,
    otherinjury        INTEGER,
    noninjured         INTEGER,
    males              INTEGER,
    females            INTEGER,
    bicyclist          INTEGER,
    passenger          INTEGER,
    driver             INTEGER,
    pedestrian         INTEGER,
    pillion            INTEGER,
    motorcyclist       INTEGER,
    unknown            INTEGER,
    ped_cyclist_5_12   INTEGER,
    ped_cyclist_13_18  INTEGER,
    old_ped_65_over    INTEGER,
    old_driver_75_over INTEGER,
    young_driver_18_25 INTEGER,
    no_of_vehicles     INTEGER,
    heavyvehicle       INTEGER,
    passengervehicle   INTEGER,
    motorcycle         INTEGER,
    pt_vehicle         INTEGER,
    deg_urban_name     VARCHAR(40),
    srns               VARCHAR(1),
    rma                VARCHAR(16),
    divided            VARCHAR(9),
    stat_div_name      VARCHAR(40),

    -- Generated geometry fields (WGS84: EPSG 4326)
    geom geometry(Point, 7844)
        GENERATED ALWAYS AS (
            CASE
              WHEN longitude IS NULL OR latitude IS NULL THEN NULL
              ELSE ST_SetSRID(ST_MakePoint(longitude, latitude), 7844)
            END
        ) STORED,

    -- check
    CONSTRAINT chk_lat CHECK (latitude  IS NULL OR (latitude  BETWEEN -90  AND 90)),
    CONSTRAINT chk_lon CHECK (longitude IS NULL OR (longitude BETWEEN -180 AND 180))
);

-- indexes
CREATE INDEX crash_date_idx ON accident(accident_date);
CREATE INDEX crash_geom_gix ON accident USING GIST (geom);

COPY accident 
--FROM '/data/crash_data_2020_2024_clean.csv'
from '/data/victorian_road_crash_data.csv'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ',',
    NULL ''
);

-- drop unwanted columns
BEGIN;

ALTER TABLE accident DROP COLUMN road_route_1;
ALTER TABLE accident DROP COLUMN lga_name;
ALTER TABLE accident DROP COLUMN dtp_region;
ALTER TABLE accident DROP COLUMN vicgrid_x;
ALTER TABLE accident DROP COLUMN vicgrid_y;
ALTER TABLE accident DROP COLUMN stat_div_name;

COMMIT;

-- person
DROP TABLE IF EXISTS person;
CREATE TABLE person (
    accident_no         char(12) NOT NULL,       
    person_id           varchar(5)  NOT NULL,       
    vehicle_id          varchar(5),                 
    sex                 char(1),                    
    age_group           varchar(10),                
    inj_level           char(1),                    
    inj_level_desc      varchar(100),
    seating_position    varchar(5),
    helmet_belt_worn    char(1),                    
    road_user_type      varchar(5),                 
    road_user_type_desc varchar(100),
    licence_state       char(1),
    taken_hospital      char(1),                    
    ejected_code        char(1),                    
    PRIMARY KEY (accident_no, person_id),
    FOREIGN KEY (accident_no) REFERENCES accident(accident_no) on delete cascade
);

-- index
CREATE INDEX person_accident_idx ON person(accident_no);
CREATE INDEX person_role_idx     ON person(road_user_type);
CREATE INDEX person_injury_idx   ON person(inj_level);

COPY person
FROM '/data/person.csv'
WITH (
    FORMAT csv,
    HEADER true,
    NULL ''
);

-- atmos

drop table if exists accident_conditions;
CREATE TABLE accident_conditions (
    accident_no char(12) not null,
    atmosph_cond INTEGER,
    atmosph_cond_seq INTEGER,
    atmosph_cond_desc TEXT,
    FOREIGN KEY (accident_no) REFERENCES accident(accident_no) on delete cascade
);

COPY accident_conditions(accident_no, atmosph_cond, atmosph_cond_seq, atmosph_cond_desc)
FROM '/data/atmospheric_cond.csv'
DELIMITER ',' CSV HEADER;
