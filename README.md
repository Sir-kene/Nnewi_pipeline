# Erosion & Flood Risk Pipeline

An automated, reusable GIS pipeline that derives erosion risk and flood risk maps for any area of interest, from elevation, satellite imagery, soil, and land cover data. Built with Python (rasterio, geopandas) for data processing and PyQGIS (GRASS provider) for terrain/hydrology analysis.

**Working example throughout this README and codebase:** Nnewi North & South, Anambra State, Nigeria — used purely as a concrete case, not a hardcoded limitation. See "Reusing This Pipeline for a Different Area" below.

---

## What This Pipeline Does

1. Standardizes all raw input data onto one shared CRS and grid
2. Derives slope, flow direction, flow accumulation, and a watershed boundary from a DEM
3. Calculates NDVI from Sentinel-2 imagery
4. Cross-validates NDVI-based land cover against ESA WorldCover
5. Reclassifies every input onto a common 0–10 risk score
6. Combines scores into **two separate outputs** — erosion risk and flood risk — using different weight profiles for each hazard
7. Clips both to the true Nnewi North/South boundary and produces final 5-class risk maps

---

## Requirements

### 1. QGIS (required — this is the core engine)
- **QGIS 3.x** (Long Term Release recommended for stability)
- Download: https://qgis.org/download/

### 2. GRASS GIS provider (required — runs inside QGIS)
- GRASS comes bundled with most QGIS installs, but must be **enabled**:
  `Settings → Options → Processing → Providers → GRASS` — confirm it's checked and points to a valid GRASS installation (no red error icon).
- Confirm your GRASS algorithm prefix before running anything — it varies by install:
  ```python
  # run in QGIS Python Console to check
  from qgis.core import QgsApplication
  for alg in QgsApplication.processingRegistry().algorithms():
      if "fill.dir" in alg.id() or "watershed" in alg.id() or "water.outlet" in alg.id():
          print(alg.id())
  ```
  Update the prefix (`grass:` vs `grass7:` vs `grass8:`) in `TERRIAN.py` to match what prints here.

### 3. Python environment (for everything except terrain/hydrology)
Two separate Python environments are involved in this pipeline:

| Environment | Used for | Has access to |
|---|---|---|
| **VS Code / system Python** | standardize, ndvi, reclassify, combine, finalize | rasterio, geopandas, numpy |
| **QGIS's bundled Python Console** | terrain.py only | PyQGIS, GRASS, `processing.run()` |

Install these in your VS Code / system Python:
```bash
pip install rasterio geopandas numpy fiona --break-system-packages
```

If QGIS's own Python environment is missing `rasterio` or `numpy` (needed inside `TERRIAN.py`), install via the **OSGeo4W Shell** (bundled with QGIS on Windows):
```
python -m pip install rasterio numpy
```

### 4. Required raw data (downloaded manually, not fetched by the pipeline)

| Dataset | Where to get it | Save as |
|---|---|---|
| DEM (elevation) | ALOS World 3D / Copernicus DEM | `alos_dem_merged.tif` |
| Sentinel-2 NIR band | Copernicus Data Space | `sentinel2_nir.tif` |
| Sentinel-2 Red band | Copernicus Data Space | `sentinel2_red.tif` |
| ESA WorldCover | esa-worldcover.org | `esa_worldcover.tif` |
| SoilGrids (clay/sand %) | soilgrids.org | `soilgrids_clay.tif` |
| Nigeria admin boundaries | data.humdata.org (HDX) | `nigeria_admin2.shp` |
| AOI (rectangular buffer) | drawn manually in QGIS | `nnewi_aoi_buffer.gpkg` |
| True Nnewi boundary | drawn/clipped manually | `nnewi_north_south.gpkg` |

Place all of these in `data/raw/` before running anything.

---

## Project Structure

```
nnewi_pipeline/
  CONFIG.py           # all paths and settings — the only file with real values
  STANDARDIZE.py       # aligns every raw file to one shared grid
  TERRIAN.py            # slope, flow accumulation, watershed (runs in QGIS Python Console)
  NDVI.py
  RECLASSIFY.py
  COMBINE.py            # produces erosion_risk and flood_risk separately
  FINALING_OUTPUT.py    # clips to true boundary, classifies into 5 bands, prints summary stats
  ALL_RUNNER.py         # orchestrates every step in order
  data/
    raw/                # your manually downloaded files go here
    processed/           # every script writes its output here
```

---

## How to Run

### Option A — step by step (recommended while still debugging)

```bash
python3 STANDARDIZE.py
```
Then, **inside QGIS's own Python Console** (Plugins → Python Console → Script Editor):
```
run TERRIAN.py
```
This step will pause and wait for you to click an outlet point on the map canvas once `flow_accumulation` loads — zoom into a bright channel first, then click.

Back in VS Code:
```bash
python3 NDVI.py
python3 RECLASSIFY.py
python3 COMBINE.py
python3 FINALING_OUTPUT.py
```

### Option B — one orchestrated run (once every step above is confirmed working individually)

Open `ALL_RUNNER.py` inside **QGIS's Python Console** (it must run there, since it calls `TERRIAN.py`, which needs PyQGIS/GRASS):
```
run ALL_RUNNER.py
```
It will run every stage in order and pause once, waiting for your outlet click during the terrain stage.

---

## Configuration

All adjustable settings live in `CONFIG.py`:

```python
TARGET_CRS = "EPSG:32632"      # UTM zone 32N — meters, correct for this region
TARGET_RESOLUTION = 30          # meters per pixel

EROSION_WEIGHTS = {"slope": 0.35, "soil": 0.35, "ndvi": 0.20, "flow": 0.10}
FLOOD_WEIGHTS   = {"flow": 0.50, "slope": 0.25, "soil": 0.15, "ndvi": 0.10}
```

Adjust weights to change how much each factor influences each hazard's final score. Adjust reclassify break values in `RECLASSIFY.py` based on your own data's real histogram (check via `rasterio` or QGIS's Symbology → Histogram tab) — the example breaks in that file are starting points, not universal values.

---

## Troubleshooting Notes (from real issues hit while building this)

- **Shape mismatch errors when combining layers** — almost always means one raster was reprojected independently and landed on a slightly different pixel grid than the others, even at the same resolution. `STANDARDIZE.py` forces everything onto one shared reference grid computed from the AOI to prevent this — if it still happens, confirm every raw file was actually reprocessed through the *current* version of `STANDARDIZE.py`, not a stale output from an earlier run.
- **GRASS outputs still misaligned after standardizing** — GRASS tools use their own internal "computational region" and can snap outputs to a slightly different extent even from a correctly standardized input. If this happens, re-align GRASS-derived layers (slope, flow accumulation) to a non-GRASS reference layer (e.g. `ndvi_score`) immediately before combining.
- **Stale `__pycache__`** — if an edited `.py` file's changes don't seem to take effect, delete the `__pycache__` folder and rerun.
- **`r.water.outlet` returns an empty watershed** — usually means the clicked coordinate wasn't precisely on a true high-accumulation stream cell. Zoom in much closer on `flow_accumulation` (with a log/cumulative-count stretch applied) before clicking.
- **Always do a full clean rerun after any fix to `STANDARDIZE.py` or `TERRIAN.py`** — delete everything in `data/processed/` first, then rerun the full chain in order. Partial reruns leave old and new files mixed together and reproduce errors that look fixed but aren't.

---

## Reusing This Pipeline for a Different Area

Nnewi is just the working example used throughout development — nothing in `STANDARDIZE.py`, `TERRIAN.py`, `NDVI.py`, `RECLASSIFY.py`, `COMBINE.py`, or `FINALING_OUTPUT.py` is hardcoded to Nnewi specifically. Every one of them reads its inputs and outputs entirely from `CONFIG.py`. To run this pipeline on a different area:

1. Download the same set of raw datasets (Section: Required raw data) for your new area of interest
2. Draw a new rectangular buffer AOI and a new true-boundary polygon for that area, same as `nnewi_aoi_buffer.gpkg` / `nnewi_north_south.gpkg`
3. Update the file paths in `CONFIG.py` to point at the new files — nothing else needs to change
4. Rerun `ALL_RUNNER.py`

No script logic changes are required — only `CONFIG.py`. This is also why every raw filename in this README is treated as an example naming convention (`nnewi_aoi_buffer.gpkg`, `alos_dem_merged.tif`, etc.) rather than a fixed requirement — name your files however makes sense for the new area, and point `CONFIG.py` at them.

**One thing that does need re-checking per area, not just re-pathing:** the reclassify break values in `RECLASSIFY.py` were calibrated to Nnewi's actual slope/flow/soil histograms. A different area — especially one with different terrain (hillier, or near a larger river) — will likely need its own breaks recalculated from that area's real data range, following the same histogram-check process described earlier in this project. The weight profiles in `CONFIG.py` (`EROSION_WEIGHTS`, `FLOOD_WEIGHTS`) are also worth revisiting per area, since what drives erosion or flooding can shift depending on local terrain and land use.

---

## Outputs

After a full run, `data/processed/` will contain:
- `erosion_risk_final.tif`, `erosion_risk_5class.tif`
- `flood_risk_final.tif`, `flood_risk_5class.tif`
- `watershed.tif` — delineated catchment boundary
- Printed area-percentage breakdowns for both hazards (from `FINALING_OUTPUT.py`), for use in your write-up
