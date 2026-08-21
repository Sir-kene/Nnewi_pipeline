# finalize_outputs.py — run in VS Code, after combine.py
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import CONFIG

def clip_to_true_boundary(src_path, out_path):
    boundary = gpd.read_file(CONFIG.TRUE_BOUNDARY_PATH)
    with rasterio.open(src_path) as src:
        out_image, out_transform = mask(src, boundary.geometry, crop=True)
        profile = src.profile
    profile.update({"height": out_image.shape[1], "width": out_image.shape[2],
                     "transform": out_transform})
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(out_image)
    print(f"Saved: {out_path}")
    return out_image[0], profile   # return the array too, for the next steps

def classify_five_bands(array, out_path, profile):
    """Converts continuous risk score into the 5-class legend."""
    classes = np.zeros_like(array)
    classes[(array >= 0) & (array < 2)]  = 1   # Very Low
    classes[(array >= 2) & (array < 4)]  = 2   # Low
    classes[(array >= 4) & (array < 6)]  = 3   # Moderate
    classes[(array >= 6) & (array < 8)]  = 4   # High
    classes[array >= 8]                   = 5   # Very High
    profile.update(dtype=rasterio.float32)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(classes.astype(rasterio.float32), 1)
    print(f"Saved: {out_path}")
    return classes

def print_summary(classes, label):
    total = classes.size
    labels = {1: "Very Low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
    print(f"\n{label} — area breakdown:")
    for val, name in labels.items():
        pct = np.sum(classes == val) / total * 100
        print(f"  {name}: {pct:.1f}%")

def run():

    erosion_arr, erosion_profile = clip_to_true_boundary(CONFIG.EROSION_RISK_PATH, CONFIG.EROSION_FINAL_PATH)
    erosion_classes = classify_five_bands(erosion_arr, CONFIG.EROSION_CLASSED_PATH, erosion_profile)
    print_summary(erosion_classes, "Erosion Risk")

    flood_arr, flood_profile = clip_to_true_boundary(CONFIG.FLOOD_RISK_PATH, CONFIG.FLOOD_FINAL_PATH)
    flood_classes = classify_five_bands(flood_arr, CONFIG.FLOOD_CLASSED_PATH, flood_profile)
    print_summary(flood_classes, "Flood Risk")
if __name__ == "__main__":
    run()