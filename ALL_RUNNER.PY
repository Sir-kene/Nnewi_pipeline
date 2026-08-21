# run_pipeline.py — open and run this in QGIS's Python Console Script Editor
import sys
import importlib
sys.path.insert(0, r"C:\Users\HP\Desktop\QGIS_Learning\Nnewi_pipeline") 

import STANDARDIZE
import TERRAIN  
import NDVI
import RECLASSIFY
import COMBINE
import FINALING_OUTPUT      



importlib.reload(STANDARDIZE
importlib.reload(TERRAIN)
importlib.reload(NDVI)
importlib.reload(RECLASSIFY
importlib.reload(COMBINE)
importlib.reload(FINALING_OUTPUT)

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
    FINALING_OUTPUT.run()

    print("\nPipeline complete — check data/processed/ for outputs.")

run_all()