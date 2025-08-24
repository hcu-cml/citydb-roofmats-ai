from flask import Flask, send_file, request, Response
from flask_cors import CORS
import logging
import os

# Setup logger
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Hide HTTP request logs
logging.basicConfig(level=logging.INFO, format='🔧 %(message)s')

app = Flask(__name__)
CORS(app)

LAYER_NAME = 'lst_layer'
TILE_MATRIX_SET = 'EPSG:3857'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TILE_DIR = os.path.join(BASE_DIR, 'bremen_lst_2024_wmts')  # folder from gdal2tiles.py

# Minimal WMTS GetCapabilities XML template
GET_CAPABILITIES_XML = f'''<?xml version="1.0" encoding="UTF-8"?>
<Capabilities xmlns="http://www.opengis.net/wmts/1.0"
  xmlns:ows="http://www.opengis.net/ows/1.1"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.opengis.net/wmts/1.0
  http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"
  version="1.0.0">

  <ows:ServiceIdentification>
    <ows:Title>Minimal WMTS Service</ows:Title>
    <ows:ServiceType>OGC WMTS</ows:ServiceType>
    <ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion>
  </ows:ServiceIdentification>

  <Contents>
    <Layer>
      <ows:Title>{LAYER_NAME}</ows:Title>
      <ows:Identifier>{LAYER_NAME}</ows:Identifier>
      <Style isDefault="true">
        <ows:Identifier>default</ows:Identifier>
      </Style>
      <Format>image/png</Format>
      <TileMatrixSetLink>
        <TileMatrixSet>{TILE_MATRIX_SET}</TileMatrixSet>
      </TileMatrixSetLink>
    </Layer>

    <TileMatrixSet>
      <ows:Identifier>{TILE_MATRIX_SET}</ows:Identifier>
      <SupportedCRS>urn:ogc:def:crs:EPSG::3857</SupportedCRS>
      <!-- Simplified matrix list for zoom levels 0-12 -->
'''

# Add TileMatrix entries for zoom 0-12
for z in range(13):
    GET_CAPABILITIES_XML += f'''
      <TileMatrix>
        <ows:Identifier>{z}</ows:Identifier>
        <ScaleDenominator>{559082264.028 / (2 ** z)}</ScaleDenominator>
        <TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
        <TileWidth>256</TileWidth>
        <TileHeight>256</TileHeight>
        <MatrixWidth>{2 ** z}</MatrixWidth>
        <MatrixHeight>{2 ** z}</MatrixHeight>
      </TileMatrix>
'''

GET_CAPABILITIES_XML += '''
    </TileMatrixSet>
  </Contents>
</Capabilities>
'''


@app.route('/wmts')
def wmts():
    req = request.args
    service = req.get('service')
    request_type = req.get('request')

    if service != 'WMTS':
        return "Service parameter must be WMTS", 400

    if request_type == 'GetCapabilities':
        return Response(GET_CAPABILITIES_XML, mimetype='application/xml')

    elif request_type == 'GetTile':
        layer = req.get('layer')
        tileMatrixSet = req.get('tilematrixset')
        tileMatrix = req.get('tilematrix')
        tileRow = req.get('tilerow')
        tileCol = req.get('tilecol')
        format_ = req.get('format', 'image/png')

        if not all([layer, tileMatrixSet, tileMatrix, tileRow, tileCol]):
            return "Missing parameters", 400

        # Convert to integers
        z = int(tileMatrix)
        x = int(tileCol)
        y = int(tileRow)

        # GDAL tiles are TMS (flipped Y), WMTS uses regular
        # y = (2 ** z - 1) - y

        tile_path = os.path.join(TILE_DIR, str(z), str(x), f'{y}.png')

        if os.path.exists(tile_path):
            return send_file(tile_path, mimetype=format_)
        else:
            return f"Tile not found: {tile_path}", 404

    return "Invalid WMTS request", 400


if __name__ == '__main__':
    logging.info("\n✅  3DCityDB Web Map Client and WMTS Server running...")
    logging.info("🌐 Buildings highlighted by 5 different roof materials: http://localhost:8080/buildings_all")
    logging.info("🌐 Buildings (with all colors) in Urban Heat Analysis: http://localhost:8080/buildings_all_lst")
    logging.info("🌐 Buildings (with green potential) in Urban Heat Analysis: http://localhost:8080/buildings_green_lst")
    app.run(debug=False, host='0.0.0.0', port=5000)
