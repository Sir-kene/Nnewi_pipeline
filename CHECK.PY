# diagnose.py
import rasterio
import CONFIG

for name, path in [
    ("dem_std", CONFIG.DEM_STD_PATH),
    ("slope", CONFIG.SLOPE_PATH),
    ("flow_acc", CONFIG.FLOW_ACC_PATH),
    ("ndvi", CONFIG.NDVI_PATH),
    ("soilgrids_std", CONFIG.SOIL_STD_PATH),
    ("slope_score", CONFIG.SLOPE_SCORE_PATH),
    ("flow_score", CONFIG.FLOW_SCORE_PATH),
    ("ndvi_score", CONFIG.NDVI_SCORE_PATH),
    ("soil_score", CONFIG.SOIL_SCORE_PATH),
]:
    try:
        with rasterio.open(path) as src:
            print(f"{name}: shape={src.shape}, transform={src.transform}")
    except Exception as e:
        print(f"{name}: FILE MISSING or ERROR — {e}")