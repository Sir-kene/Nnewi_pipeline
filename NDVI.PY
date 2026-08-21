import rasterio
import numpy as np
import CONFIG

def calculate_ndvi():
    with rasterio.open(CONFIG.NIR_STD_PATH) as src:
        nir = src.read(1).astype(float)
        profile = src.profile
    with rasterio.open(CONFIG.RED_STD_PATH) as src:
        red = src.read(1).astype(float)
        ndvi = np.divide(
            (nir - red), (nir + red),
             out=np.zeros_like(nir,
        dtype=np.float32),
             where=(nir + red) != 0
             )
    profile.update(dtype=rasterio.float32)
    with rasterio.open(CONFIG.NDVI_PATH, "w", **profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)
        print(f"Saved: {CONFIG.NDVI_PATH}") 

def run():
    calculate_ndvi()
if __name__ == "__main__":
    run()