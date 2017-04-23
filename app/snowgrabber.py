from osgeo import gdal

src_ds = gdal.Open( "/vagrant/snow_api/app/sources/sd.xml" )

img_format = "GTiff"
driver = gdal.GetDriverByName(img_format)

#Output to new format
dst_ds = driver.CreateCopy( "test4.tiff", src_ds, 0)
