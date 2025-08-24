1. Input: LST in greyscale (`bremen_lst_13082024.tif`)
2. Convert it to colored LST (green for cool, red for warm) (`bremen_lst_colored.tif`)
3. Convert GeoTIFF to WMTS:
   ```bash
   # Install gdal (MacOS)
    brew install gdal
    
    # Convert GeoTIFF to WMTS
    gdal2tiles --xyz -z 0-16 bremen_lst_colored.tif bremen_lst_2024_wmts/
   ```
4. Run WMTS server (`wmts.py`)
5. Add WMTS layer in CesiumJS
6. Make this as an overlay to compare with highlighted 3D building models