# Install gdal (MacOS)
brew install gdal

# Convert GeoTIFF to WMTS
gdal2tiles --xyz -z 0-16 bremen_lst_colored.tif bremen_lst_2024_wmts/