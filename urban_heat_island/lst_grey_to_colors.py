import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import LinearSegmentedColormap

# === Step 1: Load the LST GeoTIFF ===
tif_path = 'bremen_lst_13082024.tif'  # Replace with your file path

with rasterio.open(tif_path) as src:
    lst = src.read(1)
    profile = src.profile
    transform = src.transform
    crs = src.crs

# Mask invalid values (optional)
lst = np.ma.masked_where((lst <= 0) | (np.isnan(lst)), lst)

# === Step 2: Define Custom Colormap (Green to Red) ===
colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # green → yellow → red
cmap = LinearSegmentedColormap.from_list('GreenRed', colors, N=256)

# Normalize LST for colormap (0-1)
lst_norm = (lst - lst.min()) / (lst.max() - lst.min())
lst_rgb = cmap(lst_norm.filled(0))[:, :, :3]  # Drop alpha channel
lst_rgb = (lst_rgb * 255).astype(np.uint8)  # Convert to 8-bit RGB

# Transpose to match (band, row, col) layout
rgb_bands = np.transpose(lst_rgb, (2, 0, 1))

# === Step 3: Save RGB image as GeoTIFF ===
profile.update({
    'count': 3,
    'dtype': 'uint8',
    'driver': 'GTiff'
})

output_tif = 'bremen_lst_colored.tif'
# Remove nodata for RGB output
profile.pop('nodata', None)
with rasterio.open(output_tif, 'w', **profile) as dst:
    dst.write(rgb_bands[0], 1)  # Red
    dst.write(rgb_bands[1], 2)  # Green
    dst.write(rgb_bands[2], 3)  # Blue

print(f"✅ Colorized GeoTIFF saved as: {output_tif}")

# === Step 4: Display the colorized GeoTIFF ===
with rasterio.open('bremen_lst_colored.tif') as src:
    rgb = src.read()  # shape: (3, height, width)

# Transpose for plotting (height, width, bands)
rgb_image = np.transpose(rgb, (1, 2, 0))

plt.figure(figsize=(10, 8))
plt.imshow(rgb_image)
plt.title("Colorized LST GeoTIFF (Green to Red)")
plt.axis('off')
plt.show()