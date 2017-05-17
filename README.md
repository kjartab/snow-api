## Snow API

docker build -t "toptour/snowapi" ./

docker run -d -p 8000:8000 -v /vagrant/toptourcollection/snow-api/:/tmp/dev "toptour/snowapi"

Source: NVE

Simple solution:
- grab data from NVE when they are updated
- create geotiff
- 

10500 turer => map raster (snow depth): 


Steps:
1. Grab rasters:
    - snow depth (today + 7 days)
    - snow state
    - new snow depth last 24h (today + 7 days)
    - snow change last week

    14 + 2 = 16 
    3 * 16 * 5.7 MB = 288 MB
    


1. Put job to queue: download data
2. Respond to queue item: 
    a. grab snow from nve: get_layer('sd', '2017-05-17-15:27:00.000')
    b. convert to raster
    c. store to geoserver data
    b. update geoserver