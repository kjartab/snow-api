from osgeo import gdal,ogr,osr
import psycopg2
import json
from pyproj import *
import datetime

src_filename = 'out.tiff'
# shp_filename = '/tmp/test.shp'

databaseServer = "10.0.0.125"
databaseName = "geodata"
databaseUser = "postgres"
databasePW = "postgres"



def get_transform(source_srid, target_srid):

    source = osr.SpatialReference()
    source.ImportFromEPSG(source_srid)
    target = osr.SpatialReference()
    target.ImportFromEPSG(target_srid)
    return osr.CoordinateTransformation(source, target)

def get_point(east, north):
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(east, north)
    return point

def transform_coordinates(coordinates, from_srid, to_srid):
    transform = get_transform(from_srid, to_srid)

    point = get_point(coordinates[0], coordinates[1])
    point.Transform(transform)
    p = json.loads(point.ExportToJson())

    return p['coordinates']

conn = psycopg2.connect(dbname=databaseName, user=databaseUser, password=databasePW, host=databaseServer)

src_ds=gdal.Open(src_filename) 
gt=src_ds.GetGeoTransform()
rb=src_ds.GetRasterBand(1)

t0 = datetime.datetime.now()

cursor = conn.cursor()
geom = None
i = 0
j = 0
cursor.execute("SELECT id, ST_AsGeoJson(geom) FROM utno.turer LIMIT 100000")
for row in cursor:
    i+=1
    snow = []
    geom = ogr.CreateGeometryFromJson(row[1])

    for i in xrange(0, geom.GetPointCount()):
        j+=1
        pt = transform_coordinates(geom.GetPoint(i), 4326, 32633)

        px = int((pt[0] - gt[0]) / gt[1])
        py = int((pt[1] - gt[3]) / gt[5])

        intval=rb.ReadAsArray(px,py,1,1)
        snow.append(int(intval[0]))

conn.close()




t1 = datetime.datetime.now()

print t1-t0
print "loaded %s points with a total of %s points" % (i, j)