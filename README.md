# Nnewi Watershed & Terrain Automation Pipeline

An automated GIS processing pipeline built for QGIS using Python (`PyQGIS`). This project automates geospatial data standardization, terrain analysis, and hydrological modeling for the Nnewi region (Anambra State, Nigeria). It eliminates manual geoprocessing clicks by stringing together native QGIS algorithms and GRASS GIS processing tools into a structured, sequential workflow.

## 📌 Project Overview
The pipeline processes raw Digital Elevation Models (DEM) and vector layers to delineate watersheds and extract terrain characteristics. It uses a custom **`QEventLoop` synchronous pause mechanism** that halts script execution mid-way, allowing the user to visually inspect an automatically loaded Flow Accumulation raster, click a specific pour point (outlet) directly on the QGIS canvas, and instantly resume the automated downstream analysis.

---

## 🛠️ Pipeline Architecture & Execution Order

The project is driven by a master orchestrator (`ALL_RUNNER.PY`) which cleans QGIS's internal memory cache using `importlib` and triggers the following sub-scripts sequentially:

1. **`standardize.py`**: Reads raw datasets, handles multi-layer GeoPackage (`.gpkg`) boundary layers without throwing warnings, and clips inputs to the Nnewi study area.
2. **`TERRAIN.py`**: 
   - Fills sinks using `grass:r.fill.dir`.
   - Computes slope maps using `native:slope`.
   - Calculates accumulation and drainage structures via `grass:r.watershed`.
   - Halts using a PyQt `QEventLoop` to accept a manual map canvas click event.
   - Extracts localized watersheds using `grass:r.water.outlet` and renders results instantly.
3. **`NDVI.py`**: Computes Normalized Difference Vegetation Index tracking from satellite imagery bands.
4. **`Reclassify.py`**: Reclassifies raster layers into discrete environmental indicator metrics.
5. **`Combine.py`**: Overlays and combines multi-criteria raster datasets.
6. **`Finaling_output.py`**: Formats, styles, and exports final visualization maps.

---

## 📁 Repository Structure

```text
Nnewi_pipeline/
│
├── ALL_RUNNER.PY          # Master orchestrator script (Run this inside QGIS)
├── CONFIG.py              # Global environment paths and file parameters
├── standardize.py         # Data preprocessing and clipping
├── TERRAIN.py             # Hydrological analysis & interactive map tool logic
├── NDVI.py                # Vegetation index calculation script
├── Reclassify.py          # Raster reclassification tool
├── Combine.py             # Multi-layer overlay calculation
├── Finaling_output.py     # Final map production and export engine
│
├── raw_data/              # Directory for raw input DEM, GPKG, and Sat imagery
└── processed_data/        # Pipeline auto-generated geotiff results
```

---

## 🚀 How To Run This Project

### 1. Prerequisites
- **QGIS 3.x** installed with **GRASS GIS** enabled in your Processing Provider settings.
- Input data matching the file paths structured inside `CONFIG.py`.

### 2. Execution Steps
1. Open **QGIS**.
2. Open the **Python Console** (`Plugins` -> `Python Console` or `Ctrl + Alt + P`).
3. Click the **Show Editor** icon to open the script panel.
4. Open and load `ALL_RUNNER.PY`.
5. Press the green **Run Script** button.

### 3. Interactive Watershed Step
When the script reaches **Step 2 (Terrain processing)**, execution will temporarily freeze, and a `flow_accumulation` raster layer will appear on your screen:
1. Zoom into a high-value (bright white) pixel channel on your map canvas.
2. Click your mouse directly over your target **outlet / pour point** on the map canvas.
3. The pipeline will automatically capture your click coordinates, resume execution, run the watershed tool, load the `watershed_output` raster layer to your layers panel, and automatically proceed to run `NDVI.py` and the remaining pipeline tasks.

---

## ⚙️ Configuration (`CONFIG.py`)
All file routing utilizes absolute and relative system paths managed globally inside `CONFIG.py`. This ensures portability across different user local environments:

```python
BASE_DIR = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline"
RAW_DIR = os.path.join(BASE_DIR, "raw_data")
PROC_DIR = os.path.join(BASE_DIR, "processed_data")
# Additional automated output paths...
```
