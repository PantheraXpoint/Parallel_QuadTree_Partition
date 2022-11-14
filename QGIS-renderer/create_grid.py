# -*- coding: utf-8 -*-
td = iface.mapCanvas().layers()
extent = td[0].extent()
crs = QgsCoordinateReferenceSystem("EPSG:3857")
sourceCrs = QgsCoordinateReferenceSystem("EPSG:4326")
tr = QgsCoordinateTransform(sourceCrs, crs, QgsProject().instance())
td = tr.transformBoundingBox(extent)

params = {
    "TYPE": 2,
    "EXTENT": td,
    "HSPACING": 52,
    "VSPACING": 52,
    "HOVERLAY": 0,
    "VOVERLAY": 0,
    "CRS": crs,
    "OUTPUT": "memory",
}
out1 = processing.run("native:creategrid", params)
print(type(out1))
grid = QgsVectorLayer(out1["OUTPUT"], "grid", "ogr")
QgsProject().instance().addMapLayer(grid)
