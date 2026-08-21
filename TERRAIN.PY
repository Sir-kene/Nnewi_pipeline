# TERRAIN.py
from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsProject
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import QEventLoop
import processing
import CONFIG

def run():
    """Executes the complete terrain and watershed processing pipeline.
    
    This function blocks script execution synchronously using an event loop
    until a map canvas interaction click event registers.
    """
    # --- Step 1: fill sinks ---
    processing.run("grass:r.fill.dir", {
        'input': CONFIG.DEM_STD_PATH, 
        'format': 0,
        'output': CONFIG.DEM_FILLED_PATH, 
        'direction': 'TEMPORARY_OUTPUT',
        'areas': 'TEMPORARY_OUTPUT',
    })

    # --- Step 2: slope ---
    processing.run("native:slope", {
        'INPUT': CONFIG.DEM_FILLED_PATH, 
        'OUTPUT': CONFIG.SLOPE_PATH,
    })

    # --- Step 3: flow direction + flow accumulation ---
    processing.run("grass:r.watershed", {
        'elevation': CONFIG.DEM_FILLED_PATH, 
        'threshold': 1000,
        'accumulation': CONFIG.FLOW_ACC_PATH,
        'drainage': CONFIG.FLOW_DIR_PATH,
        'areas': 'TEMPORARY_OUTPUT',
    })

    # --- Step 4: load flow accumulation so you can see where to click ---
    flow_acc_layer = QgsRasterLayer(CONFIG.FLOW_ACC_PATH, "flow_accumulation")
    if not flow_acc_layer.isValid():
        print("Failed to load flow accumulation layer.")
        return False
        
    QgsProject.instance().addMapLayer(flow_acc_layer)
    iface.mapCanvas().setExtent(flow_acc_layer.extent())
    iface.mapCanvas().refresh()

    print("Zoom into a bright channel on flow_accumulation, then click your outlet point on the map canvas.")

    # --- Step 5: wait for your click ---
    loop = QEventLoop()
    clicked_point = {}

    def on_click(point, button):
        clicked_point['x'], clicked_point['y'] = point.x(), point.y()
        print(f"Outlet selected at: {clicked_point['x']}, {clicked_point['y']}")
        loop.quit()

    canvas = iface.mapCanvas()
    click_tool = QgsMapToolEmitPoint(canvas)
    click_tool.canvasClicked.connect(on_click)
    canvas.setMapTool(click_tool)

    loop.exec_()   # Script execution halts here until user clicks the canvas
    canvas.unsetMapTool(click_tool)

    # --- Step 6: delineate the watershed ---
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
        print("Watershed output raster loaded to map canvas.")
    else:
        print(f"Warning: Map canvas failed to initialize target file at {CONFIG.WATERSHED_PATH}")
        return False

    print("Terrain and watershed derivation complete.")
    return True

if __name__ == "__main__":
    run()
