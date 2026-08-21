# Automated Flood & Erosion Risk Mapping Pipeline

This project is an automated Python pipeline built to run inside QGIS. It replaces manual desktop clicks with a single master script to clip geographic data, run hydrological models, and produce both **Flood Risk** and **Erosion Risk** maps for any selected study area.

## 🌟 What This Project Does

Instead of doing hours of manual clipping, reclassifying, and calculations in QGIS, this pipeline automates the entire workflow. It takes your raw data layers and handles them in order:

- **Standardizes Your Study Area**: Takes any area boundary (like a `.gpkg` or `.shp` file) and clips all environmental data to match it perfectly.
- **Calculates Terrain & Water Flow**: Cleans the Digital Elevation Model (DEM), figures out water flow directions, and automatically calculates the slope of the land.
- **Pauses for User Input**: It automatically loads a map of water channels, pauses for you to click your chosen drainage outlet point on the screen, and then instantly picks back up to outline the watershed basin.
- **Processes Satellite Imagery**: Automatically processes Sentinel-2 bands (Band 4 and Band 8) to calculate vegetation cover (NDVI).
- **Creates the Final Risk Maps**: Combines the terrain, vegetation (NDVI), SoilGrids, and ESA Landcover data to calculate exactly where the highest risks for flooding and soil erosion are located.

---

## 🛠️ How the Code is Structured

The script **`ALL_RUNNER.PY`** is the main control switch. When you run it inside QGIS, it clears out QGIS's memory cache and runs these files one by one:

1. **`standardize.py`** – Clips raw datasets to your study area boundary.
2. **`TERRAIN.py`** – Processes the elevation model, calculates slopes, and handles the interactive canvas click for watershed creation.
3. **`NDVI.py`** – Runs the math on Sentinel bands to map vegetation density.
4. **`Reclassify.py`** – Organizes landcover types, soil data, and slope angles into ranked risk levels (e.g., 1 to 5).
5. **`Combine.py`** – Overlays the layers mathematically to find overlapping risk zones.
6. **`Finaling_output.py`** – Sets up the styles and exports the final risk GeoTIFF maps.

---

## 📁 Project Directory

```text
Nnewi_pipeline/
│
├── ALL_RUNNER.PY          # Main master script
├── CONFIG.py              # Stores file locations and directory paths
├── standardize.py         # Boundary clipping script
├── TERRAIN.py             # Terrain and watershed extraction
├── NDVI.py                # Sentinel band calculations
├── Reclassify.py          # Data ranking script
├── Combine.py             # Layer overlay calculations
├── Finaling_output.py     # Map styling and file export
│
├── raw_data/              # Put your input DEM, SoilGrids, Sentinel, and Landcover files here
└── processed_data/        # Where your final Flood and Erosion maps will save automatically
```

---

## 🚀 Required Input Files

To run this pipeline for your area, place these standard datasets inside your `raw_data/` folder:

| File Name/Type | Format | Why It is Needed |
| :--- | :--- | :--- |
| **Digital Elevation Model (DEM)** | `.tif` | To calculate slope steepness and track water movement. |
| **Sentinel-2 (Bands 4 & 8)** | `.tif` | To calculate NDVI and see where vegetation protects the soil. |
| **SoilGrids Data** | `.tif` | To factor in how easily the soil type can erode. |
| **ESA Landcover Map** | `.tif` | To see how buildings, forests, or farms affect rainwater runoff. |
| **Administrative Boundary** | `.gpkg` or `.shp` | The boundary outline used to cut all the data to size. |

---

## 💻 How To Run It

1. Open **QGIS** and open the Python Console (`Ctrl + Alt + P`).
2. Open the **`ALL_RUNNER.PY`** file inside the script editor.
3. Press **Run Script**.
4. When the map loads the `flow_accumulation` layer, zoom in and click on a bright stream channel. The script will take your click, build the watershed map, and automatically finish running the rest of the tools to output your final risk maps.
