import csv
import getpass
import logging
import os
import sys
import time
import traceback
from datetime import datetime

import psycopg
from shapely import wkt
from shapely.geometry import Polygon
from glob import glob

# Define folder
folder_path = 'predicted_roofmats'
attribute_name = 'PredictedRoofMaterials'

# Sensitivity for spatial matching
spatial_ratio = 0.15

# Init logging
log_file = 'run.log'
# Check if run.log exists
if os.path.exists(log_file):
    # Rename it with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.rename(log_file, f'run_{timestamp}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("run.log"),
        logging.StreamHandler(sys.stdout)  # This prints to console too
    ]
)
start_time = time.time()

# Load CSV into a dictionary
value_to_label = {}
logging.info('Load mapping of roof materials')
with open('roof_materials.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        value, label = row
        value_to_label[int(value)] = label

# Connect to an existing database
logging.info('Connect to database')
dbname = 'bremen_citygml3_2024_citydbv5_match15'
user = 'postgres'
password = getpass.getpass("Enter database password: ")
host = 'localhost'
port = '5432'
db_credentials = f"dbname={dbname} user={user} password={password} host={host} port={port}"
with psycopg.connect(db_credentials) as conn:
    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Create spatial index if not exists
        logging.info('Initialize spatial index')
        cur.execute("""
                    CREATE INDEX IF NOT EXISTS spatial_envelopes
                        ON citydb.feature
                        USING GIST (envelope);
                    """)
        conn.commit()

        # Loop through files
        logging.info('Iterate through files of predicted roof materials')
        file_list = glob(os.path.join(folder_path, '*'))
        file_count = len(file_list)
        file_i = 0;
        for file_path in file_list:
            file_i += 1
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f):
                    try:
                        material_index, poly_wkt = line.strip().split(';', 1)
                        roof_material = value_to_label[int(material_index)]
                        # polygon = wkt.loads(poly_wkt.strip())

                        # Query: find the best match using Jaccard Index
                        cur.execute("""
                                    WITH input_polygon AS (SELECT ST_GeomFromText(%s, 25832) AS geom),
                                         intersections AS (SELECT f.id,
                                                                  i.building_area,
                                                                  ST_Area(ST_Intersection(i.geom, p.geom)) AS intersection_area,
                                                                  CASE
                                                                      WHEN i.building_area = 0 THEN 0
                                                                      ELSE ST_Area(ST_Intersection(i.geom, p.geom)) / i.building_area
                                                                      END                                  AS ratio
                                                           FROM citydb.feature f
                                                                    JOIN input_polygon p ON TRUE
                                                                    JOIN LATERAL (
                                                               SELECT ST_GeomFromEWKB(f.envelope)          AS geom,
                                                                      ST_Area(ST_GeomFromEWKB(f.envelope)) AS building_area
                                                                   ) i ON ST_Intersects(i.geom, p.geom)
                                                           WHERE f.objectclass_id = 901)
                                    SELECT *
                                    FROM intersections
                                    WHERE ratio >= %s
                                    ORDER BY ratio DESC;
                                    """, (poly_wkt, spatial_ratio))
                        res = cur.fetchall()
                        if res:
                            for feature_id, building_area, intersection_area, ratio in res:
                                cur.execute("""
                                            INSERT INTO citydb.property (feature_id, datatype_id, namespace_id, name, val_string)
                                            SELECT %s,
                                                   %s,
                                                   %s,
                                                   %s,
                                                   %s WHERE NOT EXISTS (
                                                SELECT 1 FROM citydb.property
                                                WHERE feature_id = %s
                                                AND datatype_id = %s
                                                AND namespace_id = %s
                                                AND name = %s
                                                AND val_string = %s
                                                )
                                            """,
                                            # -- AND val_string = %s -- Comment this out to allow multiple roof materials in a feature
                                            (
                                                feature_id, 5, 3, attribute_name, roof_material,
                                                feature_id, 5, 3, attribute_name, roof_material
                                            ))
                                log_msg = (f"{'Processed = ' + format(file_i / file_count * 100, '5.2f') + ' %':<25}"
                                           f"{'Feature ID = ' + str(feature_id):<25}"
                                           f"{'Building area = ' + format(building_area, '.2f'):<30}"
                                           f"{'Intersection area = ' + format(intersection_area, '.2f'):<35}"
                                           f"{'Spatial ratio = ' + format(ratio, '.4f'):<30}"
                                           f"{'RoofMaterial = ' + roof_material:<30}")
                                if cur.rowcount > 0:
                                    logging.info(log_msg + "INSERTED")
                                    conn.commit()
                                else:
                                    logging.info(log_msg + "IGNORED")

                    except Exception as e:
                        print(traceback.format_exc())

end_time = time.time()
duration = end_time - start_time
logging.info(f"Finished in {duration:.3f} seconds")
