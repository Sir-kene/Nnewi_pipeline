# RECLASSIFY.py
import rasterio
import numpy as np
import CONFIG
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QInputDialog

def reclassify(array, breaks_and_scores, nodata_val=-9999.0):
    # Initialize array with NoData so background empty spaces remain unclassified
    out = np.full(array.shape, nodata_val, dtype=np.float32)
    for lo, hi, score in breaks_and_scores:
        out[(array >= lo) & (array < hi)] = score
    return out

def get_percentile_edges(n_classes, flatness_rating):
    if flatness_rating <= 1:
        base = [0, 10, 25, 50, 75, 100]
    elif flatness_rating == 2:
        base = [0, 15, 35, 60, 85, 100]
    elif flatness_rating == 3:
        import numpy as np
        return np.linspace(0, 100, n_classes + 1).tolist()
    elif flatness_rating == 4:
        base = [0, 20, 45, 70, 90, 100]
    else: # 5, hilly
        base = [0, 30, 55, 80, 95, 100]
        
    # Dynamically extract intermediate breaks and anchor the final edge strictly to 100
    percentiles = base[:n_classes] + [100]
    return percentiles


def ask_flatness_rating():
    title = "Terrain Profile Input"
    label = "How flat is your region?\n1 = low-lying / very flat land\n5 = hilly / steep terrain"
    val, ok = QInputDialog.getInt(iface.mainWindow(), title, label, value=3, min=1, max=5, step=1)
    if ok:
        print(f"User selected flatness rating: {val}")
        return val
    else:
        print("No rating selected. Defaulting to standard terrain split (3).")
        return 3

def auto_breaks_and_scores(arr, scores, flatness_rating):
    n = len(scores)
    percentiles = get_percentile_edges(n, flatness_rating)
    
    # Filter out NoData and background zeroes so they don't corrupt percentiles
    valid_data = arr[(arr > -9000) & (~np.isnan(arr))]
    if len(valid_data) == 0:
        valid_data = np.array([0, 1]) # Fallback safety array
        
    edges = np.nanpercentile(valid_data, percentiles)
    edges = np.unique(edges) # Removes duplicate values

    breaks = []
    # Fix: Guard against index overflow if unique edges are fewer than expected scores
    for i in range(len(edges) - 1):
        lo = edges[i]
        hi = edges[i + 1] if i < len(edges) - 2 else edges[i + 1] + 1e-6
        score_idx = min(i, len(scores) - 1)
        breaks.append((lo, hi, scores[score_idx]))
    return breaks

def reclassify_layer_auto(src_path, out_path, scores, flatness_rating):
    with rasterio.open(src_path) as src:
        arr = src.read(1).astype(np.float32)
        profile = src.profile.copy()

    breaks_and_scores = auto_breaks_and_scores(arr, scores, flatness_rating)
    print(f"\nProcessing {src_path}\nAuto-breaks (flatness={flatness_rating}): {breaks_and_scores}")

    score_array = reclassify(arr, breaks_and_scores, nodata_val=-9999.0)
    
    profile.update(
        dtype=rasterio.float32,
        nodata=-9999.0,
        compress='lzw'
    )
    
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(score_array, 1)
    print(f"Saved Reclassified Raster: {out_path}")

def run():
    flatness = ask_flatness_rating()

    print("=== Processing: Running Multi-Layer Auto Reclassification ===")
    reclassify_layer_auto(CONFIG.SLOPE_PATH, CONFIG.SLOPE_SCORE_PATH, [10, 8, 6, 4, 2], flatness)
    reclassify_layer_auto(CONFIG.FLOW_ACC_PATH, CONFIG.FLOW_SCORE_PATH, [2, 5, 8, 10], flatness)
    reclassify_layer_auto(CONFIG.NDVI_PATH, CONFIG.NDVI_SCORE_PATH, [9, 6, 2], flatness)
    reclassify_layer_auto(CONFIG.SOIL_STD_PATH, CONFIG.SOIL_SCORE_PATH, [2, 5, 8, 10], flatness)
    
if __name__ == "__main__":
    run()
