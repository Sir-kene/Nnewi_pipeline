# combine.py — corrected version
import rasterio
import CONFIG

EROSION_WEIGHTS = {"slope": 0.35, "soil": 0.35, "ndvi": 0.20, "flow": 0.10}
FLOOD_WEIGHTS   = {"flow": 0.50, "slope": 0.25, "soil": 0.15, "ndvi": 0.10}

def _load_scores():
    
    with rasterio.open(CONFIG.SLOPE_SCORE_PATH) as src:
        slope = src.read(1); profile = src.profile
    with rasterio.open(CONFIG.FLOW_SCORE_PATH) as src:
        flow = src.read(1)
    with rasterio.open(CONFIG.NDVI_SCORE_PATH) as src:
        ndvi = src.read(1)
    with rasterio.open(CONFIG.SOIL_SCORE_PATH) as src:
        soil = src.read(1)
    assert slope.shape == flow.shape == ndvi.shape == soil.shape, \
        f"Shape mismatch: slope{slope.shape} flow{flow.shape} ndvi{ndvi.shape} soil{soil.shape}"
    return slope, flow, ndvi, soil, profile

def build_risk(weights, out_path):
    slope, flow, ndvi, soil, profile = _load_scores()
    risk = (slope * weights["slope"] + flow * weights["flow"]
            + ndvi * weights["ndvi"] + soil * weights["soil"])
    profile.update(dtype=rasterio.float32)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(risk.astype(rasterio.float32), 1)
    print(f"Saved: {out_path}")

def run():
    build_risk(EROSION_WEIGHTS, CONFIG.EROSION_RISK_PATH)
    build_risk(FLOOD_WEIGHTS, CONFIG.FLOOD_RISK_PATH)
if __name__ == "__main__":
    run()