# standardize.py — corrected, single source of truth for the grid
import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import geopandas as gpd
import CONFIG

def get_reference_grid():
    """Computes ONE shared grid from the AOI — every raster will be forced onto this."""
    aoi = gpd.read_file(CONFIG.AOI_PATH).to_crs(CONFIG.TARGET_CRS)
    minx, miny, maxx, maxy = aoi.total_bounds
    res = CONFIG.TARGET_RESOLUTION

    width = int((maxx - minx) / res)
    height = int((maxy - miny) / res)
    transform = rasterio.transform.from_origin(minx, maxy, res, res)
    return transform, width, height

def standardize_raster(src_path, out_path, ref_transform, ref_width, ref_height,
                        dst_crs=CONFIG.TARGET_CRS):
    with rasterio.open(src_path) as src:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        profile = src.profile.copy()
        profile.update({'crs': dst_crs, 'transform': ref_transform,
                         'width': ref_width, 'height': ref_height})
        with rasterio.open(out_path, 'w', **profile) as dst:
            reproject(source=rasterio.band(src, 1), destination=rasterio.band(dst, 1),
                      src_transform=src.transform, src_crs=src.crs,
                      dst_transform=ref_transform, dst_crs=dst_crs,
                      resampling=Resampling.bilinear)
    print(f"Saved (on shared grid): {out_path}")

def standardize_vector(src_path, out_path, dst_crs=CONFIG.TARGET_CRS):
    gdf = gpd.read_file(src_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if gdf.crs != dst_crs:
        gdf = gdf.to_crs(dst_crs)
    gdf.to_file(out_path)
    print(f"Saved: {out_path}")

def run():
    ref_transform, ref_width, ref_height = get_reference_grid()
    print(f"Reference grid: {ref_width} x {ref_height} pixels")

    standardize_raster(CONFIG.DEM_RAW_PATH, CONFIG.DEM_STD_PATH, ref_transform, ref_width, ref_height)
    standardize_raster(CONFIG.SENTINEL_NIR_PATH, CONFIG.NIR_STD_PATH, ref_transform, ref_width, ref_height)
    standardize_raster(CONFIG.SENTINEL_RED_PATH, CONFIG.RED_STD_PATH, ref_transform, ref_width, ref_height)
    standardize_raster(CONFIG.WORLD_COVER_PATH, CONFIG.WORLDCOVER_STD_PATH, ref_transform, ref_width, ref_height)
    standardize_raster(CONFIG.SOIL_GRID_PATH, CONFIG.SOIL_STD_PATH, ref_transform, ref_width, ref_height)

    standardize_vector(CONFIG.AOI_PATH, r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\Nnewi_N&S_AOI.gpkg")
    standardize_vector(CONFIG.NNEWI_NORTH_AND_SOUTH_TRUE_BOUNDARY_PATH, r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\NNEWI_NORTH_AND_SOUTH_NGA_ADMIN2.gpkg")
    print("Standardization complete — every raster now shares one identical grid.")

if __name__ == "__main__":
    run()