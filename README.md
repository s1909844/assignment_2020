# assignment_2020
This contains the files needed for the 2020 OOSA assignment,which can help handle the NASA LVIS sensor data to make the spatial analysis.We will be using files from Operation IceBridge, which bridged the gap between ICESat and ICESat-2 using aircraft.
## Task1.py
A main block to call the function inside lvisClass, handleTiff and processLVIS files to process a flight line of one single LVIS flight line to a DEM of any chosen resolution in geotiff format.

The data is stored as the variables:

    outepsg:  output coordinate system
    inpepsg:  input coordinate system
    res:      resolution of input tiff
    data:     elevations 

The data should be read as:

    from processLVIS import lvisGround
    b=lvisGround(filename,onlyBounds=True)

There is an optional spatial subsetter for when dealing with large datasets.
    
    c = lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
 
Setting how many parts are divided before processing

    gap = 15
    for i in range(gap):
          for j in range(gap):
              x0=(b.bounds[2]-b.bounds[0])*i/gap + b.bounds[0]
              y0=(b.bounds[3]-b.bounds[1])*j/gap + b.bounds[1]
              x1=(b.bounds[2]-b.bounds[0])*(i+1)/gap+b.bounds[0]
              y1=(b.bounds[3]-b.bounds[1])*(j+1)/gap+b.bounds[1]

## Task2_1.py
A further version of the Task1.py. It can be used to combine multiple flight lines and merge a whole line in 2015.

### usage example
put the filenames into a text file

    listfile='/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/x.list'
    files = []
    with open(listfile,'r') as f:
          for line in f:
              filename='/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/' + line
              files.append(filename.strip())
              
## Task2_2.py
Example of how to interpoate data by replacing ondata within flight lines datasets.The following methods are added:

- raster2array():   convert Raster to array
- getNoDataValue(): Get no data value of array
- 
