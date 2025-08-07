
import overpass
import xml.etree.ElementTree as ET
import geojson


api = overpass.API(timeout=9999)
query = """
area[name="Deutschland"]->.searchArea;
(
  way["roof:material"](area.searchArea);
  relation["roof:material"](area.searchArea);
);
out body;
>;
out skel qt;
"""

response = api.get(query, responseformat="xml")
with open("overpass_data.xml", mode="w") as f:
    f.write(response)
root = ET.fromstring(response)
node_coords = {}
for node in root.findall(".//node"):
    node_id = node.attrib['id']
    lat = float(node.attrib['lat'])
    lon = float(node.attrib['lon'])
    node_coords[node_id] = (lon, lat)

def convert_to_geojson(xml_root, node_coordinates):
    features = []

    for element in xml_root.findall(".//way"):
        coords = []
        for nd in element.findall(".//nd"):
            ref = nd.attrib['ref']
            if ref in node_coordinates:
                coords.append(node_coordinates[ref])
        
        if coords:
            properties = {"id": element.attrib['id']}
            for tag in element.findall(".//tag"):
                properties[tag.attrib['k']] = tag.attrib['v']

            feature = geojson.Feature(
                type="Feature",
                geometry=geojson.Polygon([coords]),
                properties=properties
            )
            features.append(feature)
    
    return geojson.FeatureCollection(features)

geojson_data = convert_to_geojson(root, node_coords)
with open("overpass_data_germany.geojson", mode="w") as f:
    geojson.dump(geojson_data, f)

