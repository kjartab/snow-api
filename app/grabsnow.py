import os
import datetime

def retrieve_layer(layer, target_date=None):

	target_date = "2017-03-08"
	# get_date = datetime.now() 	
	print datetime.date(2002, 3, 11)

	dst = layer+'.tiff'
	cmd = "-outsize 1275 1530"
	src = '/vagrant/toptourcollection/snow-api/app/sources/' + layer + '.xml'
	os.system("gdal_translate -of GTiff " + cmd + " " + src + " " + dst)

for layer in ["sd"]:
	tmp_image = retrieve_layer(layer)