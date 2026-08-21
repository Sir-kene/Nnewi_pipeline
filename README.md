# Multi-Criteria Automated Flood & Erosion Risk Modeling Pipeline

An enterprise-grade, high-throughput spatial data engineering pipeline built with `PyQGIS` (QGIS Python API) and `GRASS GIS`. This automation engine accepts **any arbitrary Area of Interest (AOI)** and seamlessly ingests heterogeneous multi-source spatial data to dynamically model, analyze, and generate high-resolution **Flood Risk** and **Soil Erosion Vulnerability** maps.

By eliminating manual desktop GIS mouse clicks, this pipeline converts complex multi-criteria evaluation workflows into a unified, reproducible headless data science engine.

---

## 🚀 Core Engine Capabilities

- **Dynamic AOI Adaptation**: Automatically ingests multi-layer vector administrative layers (e.g., HDX HDN `nga_admin2`), handles internal layer indexing safely, clips all spatial assets to the chosen study zone, and handles datum/CRS projection alignment.
- **Advanced Hydrological Extraction**: Leverages an interactive `QEventLoop` canvas click engine. It calculates flow routing paths, pauses execution for manual outlet verification on high-flux channels, and generates deterministic watershed catchments on the fly.
- **Multi-Source Data Fusion**: Programmatically handles disparate, raw raster formats across various scales and spatial resolutions to compute physical indices:
  - **Topographic Context**: Direct-derivation of localized surface slope and flow accumulation from raw Digital Elevation Models (DEM `.tiff`).
  - **Vegetation Dynamics**: Autonomous band-math ingestion of Sentinel satellite assets (Band 4 and Band 8) to compute Normalized Difference Vegetation Index (NDVI) arrays.
  - **Environmental Baselines**: Grid alignment and structural reclassification of global ESA Landcover data and high-resolution SoilGrids soil profile rasters.
- **Automated Risk Analytical Outputs**: Automatically weights and overlays intersecting spatial factors to map dual critical hazards:
  1. **Flood Risk Zoning**: Synthesizes slope profiles, land cover roughness, and watershed drainage accumulation networks.
  2. **Erosion Vulnerability Matrix**: Combines terrain slope velocity vectors, NDVI vegetation shelter factors, and SoilGrids soil texture susceptibility.

---

## 🛠️ Automated Processing Architecture

The entire project runs sequentially via a single orchestrator (`ALL_RUNNER.PY`), which clears QGIS memory caches via `importlib` and coordinates the modular script array:

```text
ALL_RUNNER.PY (Orchestration Engine)
│
├── 1. standardize.py       ──> Ingests boundary, clips, and standardizes CRS projections.
├── 2. TERRAIN.py           ──> Resolves sinks, builds Slope/Flow networks, captures pour points.
├── 3. NDVI.py              ──> Processes Sentinel B4/B8 rasters to generate vegetation index maps.
├── 4. Reclassify.py        ──> Standardizes landcover, soil profiles, and slope into ordinal risk values.
├── 5. Combine.py           ──> Multi-Criteria Evaluation (MCE) matrix overlay math.
└── 6. Finaling_output.py   ──> Renders symbology layouts and outputs analytical risk maps.
```

---

## 📁 Project Directory Structure

```text
Nnewi_pipeline/
│
├── ALL_RUNNER.PY          # Main pipeline compiler
├── CONFIG.py              # Centralized environment environment variable routing
├── standardize.py         # AOI clipping and vector layer handler
├── TERRAIN.py             # Hydrological flow routing & interactive click callback
├── NDVI.py                # Satellite band-math calculation script
├── Reclassify.py          # Value normalization matrix engine
├── Combine.py             # Flood/Erosion overlay algebra
├── Finaling_output.py     # GeoTIFF output renderer
│
├── raw_data/              # Place raw files here (DEM, SoilGrids, Sentinel B4/B8, ESA Landcover, GPKG)
└── processed_data/        # System auto-generated environmental metrics and Risk Maps
```

---

## 🏁 Input Data Specification

To execute the pipeline for your target AOI, place the following inputs inside the `raw_data/` folder and name them according to your `CONFIG.py` settings:

| Input Dataset | Format | Core Analytical Purpose |
| :--- | :--- | :--- |
| **Digital Elevation Model** | `.tif` / `.tiff` | Slope velocity, flow routing, drainage patterns |
| **Sentinel Imagery (B4 & B8)** | `.tif` / `.tiff` | Dense vegetation canopy calculation (NDVI) |
| **SoilGrids Raster** | `.tif` / `.tiff` | Soil erodibility parameters (K-factor metrics) |
| **ESA Landcover Map** | `.tif` / `.tiff` | Hydraulic roughness parameters and surface runoff retention |
| **Admin Boundary (AOI)** | `.gpkg` / `.shp` | Dynamic study area clipping mask |

---

## 💻 Running the Risk Pipeline

1. Open **QGIS** and open the Python Console (`Ctrl + Alt + P`).
2. Load **`ALL_RUNNER.PY`** inside the script editor.
3. Click **Run Script**.
4. **Interactive Component**: When the `flow_accumulation` raster renders, zoom into your target stream channel and click the canvas to register your drainage outlet. The engine will catch the coordinates, delineate the watershed basin, and automatically run the remaining scripts to output your final **Flood and Erosion Risk GeoTIFFs**.
