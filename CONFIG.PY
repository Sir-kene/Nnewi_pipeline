# CONFIG.py — single source of truth for the project paths and configurations
import os

# Base directory for ease of configuration
BASE_DIR = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline"
RAW_DIR = os.path.join(BASE_DIR, "raw_data")
PROC_DIR = os.path.join(BASE_DIR, "processed")
OUT_DIR = os.path.join(BASE_DIR, "output_files")

# Ensure core directories exist automatically
for folder in [PROC_DIR, OUT_DIR]:
    os.makedirs(folder, exist_ok=True)

# --- raw inputs ---
AOI_PATH = os.path.join(RAW_DIR, "Nnewi_N&S_AOI.gpkg")
NNEWI_NORTH_AND_SOUTH_TRUE_BOUNDARY_PATH = os.path.join(RAW_DIR, "NNEWI_NORTH_AND_SOUTH_NGA_ADMIN2.gpkg")
DEM_RAW_PATH = os.path.join(RAW_DIR, "Nnewi_DEM_clipped.TIF")
SENTINEL_NIR_PATH = os.path.join(RAW_DIR, "B8_10m.tif")
SENTINEL_RED_PATH = os.path.join(RAW_DIR, "B4_10m.tif")
WORLD_COVER_PATH = os.path.join(RAW_DIR, "ESA_NnewiSth_n_Nth_10_N03E006_N06E006_merged_clip.tif")
SOIL_GRID_PATH = os.path.join(RAW_DIR, "soil_properties_clipped.tif")

# --- processed intermediate outputs ---
DEM_STD_PATH = os.path.join(PROC_DIR, "dem_std.tif")
NIR_STD_PATH = os.path.join(PROC_DIR, "nir_std.tif")
RED_STD_PATH = os.path.join(PROC_DIR, "red_std.tif")
WORLDCOVER_STD_PATH = os.path.join(PROC_DIR, "worldcover_std.tif")
SOIL_STD_PATH = os.path.join(PROC_DIR, "soilgrids_std.tif")
FILL_DIRECTION_PATH = os.path.join(PROC_DIR, "flow_direction.tif")

DEM_FILLED_PATH = os.path.join(PROC_DIR, "dem_filled.tif")
SLOPE_PATH = os.path.join(PROC_DIR, "slope.tif")
FLOW_DIR_PATH = os.path.join(PROC_DIR, "flow_direction.tif")
FLOW_ACC_PATH = os.path.join(PROC_DIR, "flow_accumulation.tif")
WATERSHED_PATH = os.path.join(PROC_DIR, "watershed.tif")
NDVI_PATH = os.path.join(PROC_DIR, "NDVI.tif")

SLOPE_SCORE_PATH = os.path.join(PROC_DIR, "slope_score.tif")
FLOW_SCORE_PATH = os.path.join(PROC_DIR, "flow_score.tif")
NDVI_SCORE_PATH = os.path.join(PROC_DIR, "ndvi_score.tif")
SOIL_SCORE_PATH = os.path.join(PROC_DIR, "soil.tif")

# --- final pipeline output files ---
EROSION_FINAL_PATH = os.path.join(OUT_DIR, "erosion_risk_clipped.tif")
EROSION_CLASSED_PATH = os.path.join(OUT_DIR, "erosion_risk_5class.tif")
FLOOD_FINAL_PATH = os.path.join(OUT_DIR, "flood_risk_clipped.tif")
FLOOD_CLASSED_PATH = os.path.join(OUT_DIR, "flood_risk_5class.tif")

EROSION_RISK_PATH = os.path.join(OUT_DIR, "erosion_risk_final.tif")
FLOOD_RISK_PATH = os.path.join(OUT_DIR, "flood_risk_final.tif")

# --- spatial settings ---
# EPSG:32632 is WGS 84 / UTM zone 32N (Perfect for Anambra State, Nigeria)
TARGET_CRS = "EPSG:32632" 
TARGET_RESOLUTION = 30  # Change to 10 if you want to match the raw Sentinel crispness

# --- MCDA Weights ---
WEIGHTS = {"slope": 0.25, "flow": 0.35, "ndvi": 0.20, "soil": 0.20}
