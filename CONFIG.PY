# ---raw inputs (downloaded, clipped merged files) ---
AOI_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\Nnewi_N&S_AOI.gpkg" #Area of interest four cornered with buffer
TRUE_BOUNDARY_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\NNEWI_NORTH_AND_SOUTH_NGA_ADMIN2.gpkg" # precise area of interest
DEM_RAW_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\Nnewi_DEM_clipped.TIF" # clipped merged DEM of this AREA of interest size
SENTINEL_NIR_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\B8_10m.tif"    # clipped sentinel_2 image nir
SENTINEL_RED_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\B4_10m.tif"    # clipped sentinel_2 image red
WORLD_COVER_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\ESA_NnewiSth_n_Nth_10_N03E006_N06E006_merged_clip.tif" # clipped merged Worldcover
SOIL_GRID_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\raw_data\soil_properties_clipped.tif" # clipped soil properties

# --- processed outputs ----
DEM_STD_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\dem_std.tif"
NIR_STD_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\nir_std.tif"
RED_STD_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\red_std.tif"
WORLDCOVER_STD_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\worldcover_std.tif"
SOIL_STD_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\soilgrids_std.tif"
FLOW_DIR_PATH =  r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flow_direction.tif"
WATERSHED_PATH =  r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\watershed.tif"

DEM_FILLED_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\dem_filled.tif"
SLOPE_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\slope.tif"
FLOW_ACC_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flow_accumulation.tif"
NDVI_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\NDVI.tif"


SLOPE_SCORE_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\slope_score.tif"
FLOW_SCORE_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flow_score.tif"
NDVI_SCORE_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\ndvi_score.tif"
SOIL_SCORE_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\soil.tif"

EROSION_RISK_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\erosion_risk_raw.tif"
FLOOD_RISK_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flood_risk_raw.tif"



EROSION_FINAL_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\erosion_risk_final.tif"
FLOOD_FINAL_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flood_risk_final.tif"


EROSION_CLASSED_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\erosion_risk_5class.tif"
FLOOD_CLASSED_PATH = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline\processed\flood_risk_5class.tif"


# ---settings---
TARGET_CRS = "EPSG:32632"
TARGET_RESOLUTION	= 30

WEIGHTS	=	{"slope" : 0.25, "flow" :	0.35, "ndvi" : 0.20, "soil" : 0.20}