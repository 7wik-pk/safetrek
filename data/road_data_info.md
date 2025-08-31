<h2>Source(s)</h2>

Our road data is sourced from VicMap (https://discover.data.vic.gov.au/dataset/vicmap-transport) - the ESRI shapefile(s) are processed & imported using `ogr2ogr` onto our PostGreSQL database.

While VicMap continuously updates their road network data, we are yet to set up an automated data pipeline to fetch and update our database regularly with the latest data. As of now, we are using the VicMap road network data as of 30th August 2025.

<h2>Road types</h2>

Road types (classes) are derived from the `road_type` column of the VicMap shapefile `TR_ROAD.shp`

<h3>Major Roads</h3>
h_road_type : "major"

road_type : any of
("freeway", "highway", "bypass", "parkway", "route", "road")

<h3>Suburban Roads</h3>

h_road_type : "suburban"

<h4>Prominent Suburban Roads & Arterials</h4>
road_type : any of
("street", "avenue", "boulevard", "boulevarde", "drive", "lane", "road", "crescent", "court", "terrace", "place", "way", "row", "circuit", "close", "strip", "ridge", "rise", "turn", "wynd", "loop", "chase", "link", "round", "maze", "cluster", "connection", "divide", "corner", "extension", "return", "deviation")

<h4>Suburban Access & Service Roads</h4>
road_type : any of
("access", "driveway", "entrance", "gate", "gateway", "outlet", "approach", "ramp", "edge", "elbow", "end", "key", "keys", "landing")

<h4>Inner Residential & Decorative Streets</h4>
road_type : any of
("bend", "bowl", "common", "grove", "green", "garden", "gardens", "glade", "grange", "manor", "mews", "nook", "pocket", "rest", "retreat", "view", "views", "vista")

<hr>

<h3>Rural & Low Traffic Roads</h3>
h_road_type : "rural_and_low_traffic"

road_type : any of
("track", "trail", "firebreak", "firetrail", "fireline", "cutting", "ford", "pass", "spur", "slope", "dale", "glen", "gully", "vale", "valley", "ridge", "rising", "brae", "heath", "hill", "hollow", "woods")

<h3>Pedestrian Paths & Recreational Routes</h3>
h_road_type : "pedestrian_and_recreational_paths"

road_type : any of
("path", "pathway", "walk", "walkway", "boardwalk", "promenade", "steps", "cruiseway")

<h3>Commercial & Civic Spaces</h3>
h_road_type : "commerical_and_civic"

road_type : any of
("arcade", "mall", "plaza", "centre", "centreway", "domain", "hub", "square", "concourse", "circus")

<h3>Infrastructure</h3>
h_road_type : "infrastructure"

road_type : any of
("bridge", "tunnel", "junction", "island", "quay", "quays", "wharf")

<h3>Ambiguous Types</h3>
h_road_type : "ambiguous"

road_type : any of
("amble", "break", "chase", "course", "dash", "dell", "dene", "fairway", "flats", "pursuit", "quadrant", "throughway", "top", "traverse", "line")
<hr>

todo:
geocode roads to store sa2, sa3 & sa4 codes/names -- DONE