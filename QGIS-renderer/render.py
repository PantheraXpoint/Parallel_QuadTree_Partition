# -*- coding: utf-8 -*-
urlWithParams = "type=xyz&url=http://mt1.google.com/vt/lyrs%3Ds%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=22&zmin=0"
rlayer = QgsRasterLayer(urlWithParams, "Google Satellite", "wms")
QgsProject.instance().addMapLayer(rlayer)

renderer = rlayer.renderer()
provider = rlayer.dataProvider()

pipe = QgsRasterPipe()
pipe.set(provider.clone())
pipe.set(renderer.clone())

crs = QgsCoordinateReferenceSystem("EPSG:3857")

layerList = iface.mapCanvas().layers()
for layer in layerList:
    print(str(type(layer)))
    if type(layer) == "<class 'qgis._core.QgsRasterLayer'>":
        continue

    for feature in layer.getFeatures():
        extent = QgsRectangle(
            feature.attributes()[2],
            feature.attributes()[3],
            feature.attributes()[4],
            feature.attributes()[5],
        )
        file_name = (
            "Q:\\test\\" + layer.name() + "_" + str(feature.attributes()[0]) + ".tif"
        )
        print(file_name)
        file_writer = QgsRasterFileWriter(file_name)
        file_writer.Mode(0)
        file_writer.writeRaster(pipe, 300, 300, extent, crs)
