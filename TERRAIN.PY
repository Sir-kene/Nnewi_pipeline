# TERRAIN.py — production version, clean processing bindings
from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsProject
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import QEventLoop, QCoreApplication
import processing
import CONFIG

def run():
    """Executes the complete terrain and watershed processing pipeline.
    
    This function halts execution until a map canvas interaction click event 
    registers, processing background GUI events to prevent QGIS from freezing.
    """
    print("=== Processing: Filling Sinks ===")
    # Fix: Changed None to empty strings "" to satisfy strict GRASS tool expectations
    processing.run("grass:r.fill.dir", {
        'input': CONFIG.DEM_STD_PATH, 
        'format': 0,
        'output': CONFIG.DEM_FILLED_PATH, 
        'direction': CONFIG.FILL_DIRECTION_PATH,
        'areas': 'TEMPORARY_OUTPUT'
        
    })

    print("=== Processing: Extracting Slope ===")
    processing.run("native:slope", {
        'INPUT': CONFIG.DEM_FILLED_PATH, 
        'OUTPUT': CONFIG.SLOPE_PATH,
    })

    print("=== Processing: Accumulation & Flow Direction ===")
    # Fix: Changed all optional outputs from None to empty strings "" to avoid type errors
    processing.run("grass:r.watershed", {
        'elevation': CONFIG.DEM_FILLED_PATH, 
        'threshold': 1000,
        'accumulation': CONFIG.FLOW_ACC_PATH,
        'drainage': CONFIG.FLOW_DIR_PATH,
        'basin': "",
        'stream': "",
        'half_basin': "",
        'slope_steepness': "",
        'tcap': "",
        'disturbed_land': "",
        'chlslope': ""
    })

    # --- Step 4: load flow accumulation so you can see where to click ---
    flow_acc_layer = QgsRasterLayer(CONFIG.FLOW_ACC_PATH, "flow_accumulation")
    if not flow_acc_layer.isValid():
        print("Failed to load flow accumulation layer.")
        return False
        
    QgsProject.instance().addMapLayer(flow_acc_layer)
    iface.mapCanvas().setExtent(flow_acc_layer.extent())
    iface.mapCanvas().refresh()

    print("\n[ACTION REQUIRED] Zoom into a bright channel on flow_accumulation, then click your outlet point on the map canvas.")

    # --- Step 5: wait for your click safely ---
    loop = QEventLoop()
    clicked_point = {}

    def on_click(point, button):
        clicked_point['x'], clicked_point['y'] = point.x(), point.y()
        print(f"Outlet selected at Coordinate: {clicked_point['x']}, {clicked_point['y']}")
        loop.quit()

    canvas = iface.mapCanvas()
    click_tool = QgsMapToolEmitPoint(canvas)
    click_tool.canvasClicked.connect(on_click)
    canvas.setMapTool(click_tool)

    # Flush the GUI thread events so the canvas unfreezes and accepts user mouse input
    while not clicked_point:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
        if loop.isRunning():
            break
        loop.exec_()

    canvas.unsetMapTool(click_tool)

    print("=== Processing: Delineating Watershed Basin ===")
    processing.run("grass:r.water.outlet", {
        'input': CONFIG.FLOW_DIR_PATH,
        'coordinates': f"{clicked_point['x']},{clicked_point['y']}",
        'output': CONFIG.WATERSHED_PATH,
    })

    # --- Step 7: Load watershed layer automatically to map view ---
    watershed_layer = QgsRasterLayer(CONFIG.WATERSHED_PATH, "watershed_output")
    if watershed_layer.isValid():
        QgsProject.instance().addMapLayer(watershed_layer)
        iface.mapCanvas().refresh()
        print("Watershed output raster loaded to map canvas successfully.")
    else:
        print(f"Warning: Map canvas failed to initialize target file at {CONFIG.WATERSHED_PATH}")
        return False

    print("Terrain and watershed derivation complete.")
    return True

if __name__ == "__main__":
    run()
