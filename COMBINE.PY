# combine.py
import rasterio
import numpy as np
import CONFIG

# Refined structural weight metrics matching MCDA standards
EROSION_WEIGHTS = {"slope": 0.35, "soil": 0.35, "ndvi": 0.20, "flow": 0.10}
FLOOD_WEIGHTS   = {"flow": 0.50, "slope": 0.25, "soil": 0.15, "ndvi": 0.10}

def _load_scores():
    with rasterio.open(CONFIG.SLOPE_SCORE_PATH) as src:
        slope = src.read(1).astype(np.float32)
        profile = src.profile.copy()
    with rasterio.open(CONFIG.FLOW_SCORE_PATH) as src:
        flow = src.read(1).astype(np.float32)
    with rasterio.open(CONFIG.NDVI_SCORE_PATH) as src:
        ndvi = src.read(1).astype(np.float32)
    with rasterio.open(CONFIG.SOIL_SCORE_PATH) as src:
        soil = src.read(1).astype(np.float32)
        
    assert slope.shape == flow.shape == ndvi.shape == soil.shape, \
        f"Shape mismatch: slope {slope.shape} flow {flow.shape} ndvi {ndvi.shape} soil {soil.shape}"
    return slope, flow, ndvi, soil, profile

def build_risk(weights, out_path):
    print(f"=== Processing: Building Layer Overlay for {out_path} ===")
    slope, flow, ndvi, soil, profile = _load_scores()
    
    # Step 1: Create a combined mask identifying where all data layers are valid
    # Pixels must be above our reclassified background baseline (-9000)
    valid_mask = (slope > -9000) & (flow > -9000) & (ndvi > -9000) & (soil > -9000)
    
    # Step 2: Initialize output matrix populated with standard NoData flag values
    risk = np.full(slope.shape, -9999.0, dtype=np.float32)
    
    # Step 3: Run the weighted overlay computation strictly on the valid data regions
    risk_calc = (
        (slope * weights["slope"]) + 
        (flow * weights["flow"]) + 
        (ndvi * weights["ndvi"]) + 
        (soil * weights["soil"])
    )
    
    # Assign calculations back to valid locations only
    np.putmask(risk, valid_mask, risk_calc)
    
    # Step 4: Finalize file profiles with LZW disk compression settings
    profile.update(
        dtype=rasterio.float32,
        nodata=-9999.0,
        compress='lzw'
    )
    
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(risk, 1)
    print(f"Saved Weighted Index Model to: {out_path}")

def run():
    build_risk(EROSION_WEIGHTS, CONFIG.EROSION_RISK_PATH)
    build_risk(FLOOD_WEIGHTS, CONFIG.FLOOD_RISK_PATH)

if __name__ == "__main__":
    run()
