# finalize_outputs.py — production version, safe masking, area stats, and visual symbology
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import CONFIG

def clip_to_true_boundary(src_path, out_path):
    print(f"=== Processing: Clipping {src_path} to True Boundary ===")
    boundary = gpd.read_file(CONFIG.NNEWI_NORTH_AND_SOUTH_TRUE_BOUNDARY_PATH)
    
    with rasterio.open(src_path) as src:
        if boundary.crs != src.crs:
            boundary = boundary.to_crs(src.crs)
        
        # out_image is returned as a 3D array [bands, height, width]
        out_image, out_transform = mask(src, boundary.geometry, crop=True, nodata=-9999.0)
        profile = src.profile.copy()
        
    # Isolate the first band as a clean 2D array to fix shape conflicts
    single_band = out_image[0]
    
    profile.update({
        "height": single_band.shape[0], 
        "width": single_band.shape[1],
        "transform": out_transform,
        "count": 1,
        "nodata": -9999.0,
        "compress": "lzw"
    })
    
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(single_band, 1) # Safely write 2D array to band 1
        
    print(f"Saved Clipped Raster: {out_path}")
    return single_band, profile

def classify_five_bands(array, out_path, profile):
    print("=== Processing: Categorizing Continuous Risk into 5 Classes ===")
    
    # Initialize background matrix with NoData values to protect boundary masks
    classes = np.full(array.shape, -9999.0, dtype=np.float32)
    
    # Create a mask tracking valid land cells only (skipping NoData values)
    valid_mask = (array > -9000)
    
    # Safely apply classification rules exclusively to real data cells
    classes[valid_mask & (array >= 0) & (array < 2)]  = 1   # Very Low
    classes[valid_mask & (array >= 2) & (array < 4)]  = 2   # Low
    classes[valid_mask & (array >= 4) & (array < 6)]  = 3   # Moderate
    classes[valid_mask & (array >= 6) & (array < 8)]  = 4   # High
    classes[valid_mask & (array >= 8)]                = 5   # Very High
    
    profile.update(
        dtype=rasterio.float32,
        nodata=-9999.0,
        compress="lzw"
    )
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(classes, 1)
        
    print(f"Saved Classed Raster: {out_path}")
    return classes

def print_summary(classes, label):
    # Isolate real data classes (1-5) and ignore negative background NoData values
    valid_pixels = classes[classes > 0]
    total = valid_pixels.size
    
    if total == 0:
        print(f"\n{label} — No valid data inside area bounds.")
        return

    labels = {1: "Very Low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
    print(f"\n{label} — True Internal Area Breakdown:")
    for val, name in labels.items():
        pct = np.sum(valid_pixels == val) / total * 100
        print(f"  {name}: {pct:.1f}%")

def apply_risk_symbology(layer, layer_name):
    """Automatically styles a 1-5 raster layer with a clear risk color ramp."""
    from qgis.core import QgsColorRampShader, QgsSingleBandPseudoColorRenderer, QgsRasterShader
    from qgis.PyQt.QtGui import QColor

    provider = layer.dataProvider()
    
    # Define exact colors matching your 5-class breakdown
    color_map = [
        QgsColorRampShader.ColorRampItem(1.0, QColor("#2b83ba"), "Very Low Risk"),
        QgsColorRampShader.ColorRampItem(2.0, QColor("#abdda4"), "Low Risk"),
        QgsColorRampShader.ColorRampItem(3.0, QColor("#ffffbf"), "Moderate Risk"),
        QgsColorRampShader.ColorRampItem(4.0, QColor("#fdae61"), "High Risk"),
        QgsColorRampShader.ColorRampItem(5.0, QColor("#d7191c"), "Very High Risk")
    ]
    
    # Initialize the color ramp shader configuration
    shader = QgsColorRampShader()
    shader.setColorRampType(QgsColorRampShader.Exact) # Forces discrete step jumps
    shader.setColorRampItemList(color_map)
    
    # Wrap the color ramp shader inside a raster shader block
    raster_shader = QgsRasterShader()
    raster_shader.setRasterShaderFunction(shader)
    
    # Bind the wrapped raster shader to the pseudo-color renderer engine
    custom_renderer = QgsSingleBandPseudoColorRenderer(provider, 1, raster_shader)
    layer.setRenderer(custom_renderer)
    layer.triggerRepaint()
    print(f"Applied production symbology legend to: {layer_name}")

def run():
    from qgis.core import QgsRasterLayer, QgsProject
    from qgis.utils import iface

    # 1. Process and extract arrays/profiles
    erosion_arr, erosion_profile = clip_to_true_boundary(CONFIG.EROSION_RISK_PATH, CONFIG.EROSION_FINAL_PATH)
    erosion_classes = classify_five_bands(erosion_arr, CONFIG.EROSION_CLASSED_PATH, erosion_profile)
    print_summary(erosion_classes, "Erosion Risk")

    flood_arr, flood_profile = clip_to_true_boundary(CONFIG.FLOOD_RISK_PATH, CONFIG.FLOOD_FINAL_PATH)
    flood_classes = classify_five_bands(flood_arr, CONFIG.FLOOD_CLASSED_PATH, flood_profile)
    print_summary(flood_classes, "Flood Risk")

    print("\n=== Loading and Styling Final Maps on Layer Board ===")
    
    # 2. Build the visual layers inside the QGIS working environment
    erosion_layer = QgsRasterLayer(CONFIG.EROSION_CLASSED_PATH, "Final Erosion Risk Model")
    flood_layer = QgsRasterLayer(CONFIG.FLOOD_CLASSED_PATH, "Final Flood Risk Model")
    
    if erosion_layer.isValid():
        apply_risk_symbology(erosion_layer, "Erosion Layer")
        QgsProject.instance().addMapLayer(erosion_layer)
        
    if flood_layer.isValid():
        apply_risk_symbology(flood_layer, "Flood Layer")
        QgsProject.instance().addMapLayer(flood_layer)
        
    iface.mapCanvas().refresh()
    print("\nPipeline complete — check your QGIS Layers Board to see your finished maps!")

if __name__ == "__main__":
    run()