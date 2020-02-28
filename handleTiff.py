

'''
A class to handle geotiffs
'''

#######################################################
# import necessary packages

from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np



#######################################################

class tiffHandle():
  '''
  Class to handle geotiff files
  '''

  ########################################

  def __init__(self,filename,x0,y0,x1,y1,nx,ny,x,y):
    '''
    Class initialiser
    Does nothing as this is only an example
    '''
    self.minX = x0
    self.minY = y0
    self.maxX = x1
    self.maxY = y1
    self.nX = nx
    self.nY = ny
    self.x = x
    self.y = y


  ########################################

  def writeTiff(self,data,res,filename="chm.tif",epsg=27700):
    '''
    Write a geotiff from a raster layer
    '''

    # self.data=data.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)

    # set geolocation information (note geotiffs count down from top edge in Y)
    # self.data=data.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)
    # pack in to array
    imageArr=np.full((self.nY,self.nX),-999.0)        # make an array of missing data flags
    xInds=np.array((self.x-self.minX)/res,dtype=int)  # determine which pixels the data lies in
    yInds=np.array((self.maxY-self.y)/res,dtype=int)  # determine which pixels the data lies in
    #this is a simple pack which will assign a single footprint to each pixel

    imageArr[yInds,xInds]=data

    geotransform = (self.minX, res, 0, self.maxY, 0, -1*res)

    # load data in to geotiff object
    dst_ds = gdal.GetDriverByName('GTiff').Create(filename, self.nX, self.nY, 1, gdal.GDT_Float32)

    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(epsg)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(imageArr)  # write image to the raster
    dst_ds.GetRasterBand(1).SetNoDataValue(-999)  # set no data value
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    print("Image written to",filename)
    return


  ########################################

  def readTiff(self,filename,epsg=27700):
    '''
    Read a geotiff in to RAM
    '''

    # open a dataset object
    ds=gdal.Open(filename)
    # could use gdal.Warp to reproject if wanted?

    # read data from geotiff object
    self.nX=ds.RasterXSize             # number of pixels in x direction
    self.nY=ds.RasterYSize             # number of pixels in y direction
    # geolocation tiepoint
    transform_ds = ds.GetGeoTransform()# extract geolocation information
    self.xOrigin=transform_ds[0]       # coordinate of x corner
    self.yOrigin=transform_ds[3]       # coordinate of y corner
    self.pixelWidth=transform_ds[1]    # resolution in x direction
    self.pixelHeight=transform_ds[5]   # resolution in y direction
    # read data. Returns as a 2D numpy array
    self.data=ds.GetRasterBand(1).ReadAsArray(0,0,self.nX,self.nY)


#######################################################
