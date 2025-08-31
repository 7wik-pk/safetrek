-- final updates after ogr2ogr commands

-- delete unwanted columns
ALTER TABLE vicmap_road
DROP COLUMN ogc_fid,
DROP COLUMN ufi,
DROP COLUMN pfi,
DROP COLUMN nfeat_id,
DROP COLUMN ezi_rdname,
DROP COLUMN road_name,
DROP COLUMN rd_suf,
DROP COLUMN rdnameuse,
DROP COLUMN rd_name1,
DROP COLUMN rd_type1,
DROP COLUMN rd_suf1,
DROP COLUMN rdnameuse1,
DROP COLUMN rd_name2,
DROP COLUMN rd_type2,
DROP COLUMN rd_suf2,
DROP COLUMN rdnameuse2,
DROP COLUMN rd_name3,
DROP COLUMN rd_type3,
DROP COLUMN rd_suf3,
DROP COLUMN rdnameuse3,
DROP COLUMN rd_name4,
DROP COLUMN rd_type4,
DROP COLUMN rd_suf4,
DROP COLUMN rdnameuse4,
DROP COLUMN rd_name5,
DROP COLUMN rd_type5,
DROP COLUMN rd_suf5,
DROP COLUMN rdnameuse5,
DROP COLUMN rd_name6,
DROP COLUMN rd_type6,
DROP COLUMN rd_suf6,
DROP COLUMN rdnameuse6,
DROP COLUMN rd_name7,
DROP COLUMN rd_type7,
DROP COLUMN rd_suf7,
DROP COLUMN rdnameuse7,
DROP COLUMN left_loc,
DROP COLUMN right_loc,
DROP COLUMN class_code,
DROP COLUMN dir_code,
DROP COLUMN route_no,
DROP COLUMN ht_limit,
DROP COLUMN restrictn,
DROP COLUMN const_type,
DROP COLUMN road_seal,
DROP COLUMN rd_status,
DROP COLUMN vecaccess,
DROP COLUMN seasopendt,
DROP COLUMN seasclsedt,
DROP COLUMN load_limit,
DROP COLUMN ldlmtassdt,
DROP COLUMN cons_mat,
DROP COLUMN length_m,
DROP COLUMN width_m,
DROP COLUMN deck_area,
DROP COLUMN respauthcd,
DROP COLUMN coordauthc,
DROP COLUMN urban,
DROP COLUMN nre_route,
DROP COLUMN from_ufi,
DROP COLUMN to_ufi,
DROP COLUMN fqid,
DROP COLUMN task_id,
DROP COLUMN crdate_pfi,
DROP COLUMN super_pfi,
DROP COLUMN crdate_ufi;

ALTER TABLE vicmap_road_structures
DROP COLUMN ogc_fid,
DROP COLUMN ufi,
DROP COLUMN pfi,
DROP COLUMN nfeat_id,
DROP COLUMN rotation,
DROP COLUMN deck_area,
DROP COLUMN coordauthc,
DROP COLUMN urban,
DROP COLUMN conpfi1,
DROP COLUMN conpfi2,
DROP COLUMN fqid,
DROP COLUMN task_id,
DROP COLUMN crdate_pfi,
DROP COLUMN super_pfi,
DROP COLUMN crdate_ufi;

-- adding index(es)
CREATE INDEX idx_mesh_geom ON mesh_block_vic_21 USING GIST (geom);
VACUUM analyze mesh_block_vic_21;

CREATE INDEX idx_vicmap_road_geom ON vicmap_road USING GIST (geom);
VACUUM ANALYZE vicmap_road;

CREATE INDEX idx_accident_road_name_lower ON accident(LOWER(road_name));

-- update vicmap_road table to store sa2, sa3, sa4 info

--alter table vicmap_road 
--drop column sa2_name21,
--drop column sa3_name21,
--drop column sa4_name21;

ALTER TABLE vicmap_road
ADD COLUMN sa2_name21 VARCHAR(50),
ADD COLUMN sa3_name21 VARCHAR(50),
ADD COLUMN sa4_name21 VARCHAR(50)
;

UPDATE vicmap_road r
set
	sa2_name21 = m.sa2_name21,
    sa3_name21 = m.sa3_name21,
    sa4_name21 = m.sa4_name21
FROM mesh_block_vic_21 m
WHERE ST_Contains(m.geom, ST_Centroid(r.geom));

delete from vicmap_road r where (r.sa2_name21 is null) or (r.sa3_name21 is null);

-- Index for SA2 area name
CREATE INDEX idx_vicmap_road_sa2_name ON vicmap_road(sa2_name21);

-- Index for SA3 area name
CREATE INDEX idx_vicmap_road_sa3_name ON vicmap_road(sa3_name21);

-- Index for SA4 area name
CREATE INDEX idx_vicmap_road_sa4_name ON vicmap_road(sa4_name21);

-- update vicmap_road to store higher classifications of road_types

--alter table vicmap_road drop column h_road_type;

-- Step 1: Add the new column
ALTER TABLE vicmap_road
ADD COLUMN h_road_type varchar(50);

-- Step 2: Populate it based on road_type
UPDATE vicmap_road
SET h_road_type = CASE
  WHEN LOWER(road_type) IN ('freeway', 'highway', 'bypass', 'parkway', 'route', 'road') THEN 'major'
  WHEN LOWER(road_type) IN ('street', 'avenue', 'boulevard', 'boulevarde', 'drive', 'lane', 'crescent', 'court', 'terrace', 'place', 'way', 'row', 'circuit', 'close', 'strip', 'ridge', 'rise', 'turn', 'wynd', 'loop', 'chase', 'link', 'round', 'maze', 'cluster', 'connection', 'divide', 'corner', 'extension', 'return', 'deviation', 'access', 'driveway', 'entrance', 'gate', 'gateway', 'outlet', 'approach', 'ramp', 'edge', 'elbow', 'end', 'key', 'keys', 'landing', 'bend', 'bowl', 'common', 'grove', 'green', 'garden', 'gardens', 'glade', 'grange', 'manor', 'mews', 'nook', 'pocket', 'rest', 'retreat', 'view', 'views', 'vista') THEN 'suburban'
  WHEN LOWER(road_type) IN ('track', 'trail', 'firebreak', 'firetrail', 'fireline', 'cutting', 'ford', 'pass', 'spur', 'slope', 'dale', 'glen', 'gully', 'vale', 'valley', 'ridge', 'rising', 'brae', 'heath', 'hill', 'hollow', 'woods') THEN 'rural_and_low_traffic'
  WHEN LOWER(road_type) IN ('path', 'pathway', 'walk', 'walkway', 'boardwalk', 'promenade', 'steps', 'cruiseway') THEN 'pedestrian_and_recreational_paths'
  WHEN LOWER(road_type) IN ('arcade', 'mall', 'plaza', 'centre', 'centreway', 'domain', 'hub', 'square', 'concourse', 'circus') THEN 'commerical_and_civic'
  WHEN LOWER(road_type) IN ('bridge', 'tunnel', 'junction', 'island', 'quay', 'quays', 'wharf') THEN 'infrastructure'
  WHEN LOWER(road_type) IN ('amble', 'break', 'chase', 'course', 'dash', 'dell', 'dene', 'fairway', 'flats', 'pursuit', 'quadrant', 'throughway', 'top', 'traverse', 'line') THEN 'ambiguous'
  ELSE NULL
END;

CREATE INDEX idx_vicmap_road_hroadtype ON vicmap_road(h_road_type);

ALTER SYSTEM RESET max_wal_size;
SELECT pg_reload_conf();
