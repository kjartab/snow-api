from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import csv
import numpy as np
import datetime
 
def convert_to_raster(layer, wms_legend):
	
	output_file = "out.tiff"

	ds = gdal.Open("/vagrant/snow_api/app/sources/" + layer + ".xml")

	band_r = ds.GetRasterBand(1)
	band_g = ds.GetRasterBand(2)
	band_b = ds.GetRasterBand(3)
	
	data_r = BandReadAsArray(band_r)
	data_g = BandReadAsArray(band_g)
	data_b = BandReadAsArray(band_b)

	xlen = len(data_r)
	ylen = len(data_r[0])

	def map_value(val):
		return wms_legend.get(val)['est']

	# output = data_r*data_g*data_b + data_r*data_g*data_b + data_r*data_g*data_b
	output = np.zeros([xlen,ylen])
	for i in xrange(0, xlen):
		for j in xrange(0, ylen):
			output[i][j] = map_value(data_r[i][j].astype(np.uint16) + data_g[i][j] + data_b[i][j])

	driver = gdal.GetDriverByName("GTiff")
	dsOut = driver.Create(output_file, ds.RasterXSize, ds.RasterYSize, 1, band_r.DataType)
	CopyDatasetInfo(ds, dsOut)
	bandOut=dsOut.GetRasterBand(1)
	BandWriteArray(bandOut, output)


def get_legend(file):
	with open(file, 'r') as reader:
		
		header = reader.readline().strip().split(";")
		legendinfo = dict()
		for line in reader:
			d = dict()
			cols = line.rstrip().split(";")
			for i in xrange(0, len(cols)):
				if header[i] in ['r','g','b']:
					d[header[i]] = int(cols[i])	
				else:
					d[header[i]] = cols[i]

			d['rgbsum'] = d['r'] + d['g'] + d['b']
			legendinfo[d['rgbsum']] = d

		return legendinfo



t0 = datetime.datetime.now()
linfo = get_legend("snodybde.csv")
t1 = datetime.datetime.now()
convert_to_raster("sd", linfo)
t2 = datetime.datetime.now()

print t1-t0, t2-t1