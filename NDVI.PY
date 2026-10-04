# NDVI.py
import rasterio
import numpy as np
import CONFIG

def calculate_ndvi():
    print("=== Processing: Computing NDVI Array Math ===")
    
    with rasterio.open(CONFIG.NIR_STD_PATH) as src_nir:
        nir = src_nir.read(1).astype(np.float32)
        profile = src_nir.profile.copy()
        
    with rasterio.open(CONFIG.RED_STD_PATH) as src_red:
        red = src_red.read(1).astype(np.float32)

    # Force absolute dimension conformity to avoid any single-pixel broadcast errors
    if nir.shape != red.shape:
        print(f"Warning: Array dimensions mismatch! Adjusting red {red.shape} to match nir {nir.shape}")
        # Crop/pad red array to exactly match the target NIR matrix dimensions
        red = red[:nir.shape[0], :nir.shape[1]]

    # Step 1: Create a safety mask for real data (exclude background zeroes/nodata values)
    # Assuming standard Sentinel-2 unmapped areas are 0
    valid_mask = (nir > 0) & (red > 0) & ((nir + red) != 0)

    # Step 2: Initialize full matrix with target NoData values (-9999.0)
    ndvi = np.full(nir.shape, -9999.0, dtype=np.float32)

    # Step 3: Compute NDVI arithmetic strictly on valid data locations
    # This prevents division-by-zero errors AND border zero contamination
    np.divide(
        (nir - red), 
        (nir + red), 
        out=ndvi, 
        where=valid_mask
    )

    # Step 4: Safely update raster header metrics with compression rules
    profile.update(
        dtype=rasterio.float32,
        nodata=-9999.0,
        compress='lzw'
    )

    with rasterio.open(CONFIG.NDVI_PATH, "w", **profile) as dst:
        dst.write(ndvi, 1)
        print(f"Saved Clean NDVI Array to: {CONFIG.NDVI_PATH}") 

def run():
    calculate_ndvi()

if __name__ == "__main__":
    run()
