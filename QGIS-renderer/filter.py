td = QgsProject.instance().mapLayersByName("ThuDuc")[0]
gr = QgsProject.instance().mapLayersByName("grid")[0]

processing.run("native:selectbylocation", 
    {'INPUT': gr,
    'PREDICATE':[0],
    'INTERSECT': td,
    'METHOD':1})
    
crs = QgsCoordinateReferenceSystem("EPSG:3857")
_writer = QgsVectorFileWriter.writeAsVectorFormat(gr, 'Q:\\Ground_Data\\HCM\\ThuDuc\\grid.geojson', "utf-8", crs, "GEOJSON", onlySelected=True)