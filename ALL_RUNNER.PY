# run_pipeline.py — open and run this in QGIS's Python Console Script Editor
import sys
import importlib

# 1. This correctly tells QGIS where to find your files
pipeline_path = r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline"
if pipeline_path not in sys.path:
    sys.path.insert(0, pipeline_path) 

# 2. This imports all 6 modules perfectly matching your disk names
# 2. This imports all 7 modules perfectly matching your disk names
import CONFIG  # Added this import
import STANDARDIZE
import TERRAIN  
import NDVI
import RECLASSIFY
import COMBINE
import FINALIZE_OUTPUT  

# 3. This cleanly reloads them so any code edits are caught dynamically
importlib.reload(CONFIG)  # Moved here, right at the top of reloads
importlib.reload(STANDARDIZE)
importlib.reload(TERRAIN)
importlib.reload(NDVI)
importlib.reload(RECLASSIFY) 
importlib.reload(COMBINE)
importlib.reload(FINALIZE_OUTPUT)  


# 4. This executes the 5 steps in the precise logical order required
def run_all():
    print("=== 1/5 STANDARDIZE ===")
    STANDARDIZE.run()

    print("=== 2/5 TERRIAN (GRASS) ===")
    TERRAIN.run()

    print("=== 3/5 NDVI ===")
    NDVI.run()

    print("=== 4/5 RECLASSIFY ===")
    RECLASSIFY.run()

    print("=== 5/5 COMBINE + FINALING_OUTPUT ===")
    COMBINE.run()
    FINALIZE_OUTPUT.run()

    print("\nPipeline complete — check data/processed/ for outputs.")

run_all()
