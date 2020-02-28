from lvisClass import lvisData
from processLVIS import lvisGround
from handleTiff import tiffHandle
from pyproj import Proj, transform # package for reprojecting data
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np





def readfiles(self,file,filename):
    '''
    Read files into list
    '''
    files = []
    with open(file,'r') as f:
        for line in f:
            newfile = filename + line
            files.append(newfile.strip())
            

def overlay(self,filename1,filename2):
    """
    Function to find intersection of two 2D arrays.
    Returns index of rows in X that are common to Y.
    """
    tiffHandle.readTiff()
    intersection = np.empty((filename1.shape[0],filename1.shape[1]))   #get the bounds and create a new array

    for y in range(intersection.shape[0]):
        for x in range(intersection.shape[1]):
            if(filename1[y,x] != 0 and filename2[y,x] != 0):           #Find the overlap area
                intersection[y,x] = filename1[y,x]-filename2[y,x]      #Get the elevation change
    
    tiffHandle.writeTiff(intersection)



if __name__=="__main__":
    afile = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/x.list'
    afilename = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/' 
    
    bfile = '/home/s1982773/OOSA/src (copy)/2009_x.list'
    bfilename = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2009/'
    
    a = readfiles(afile,afilename)
    b = readfiles(bfile,bfilename)
    
    overlay(a.data,b.data)
    
    c = tiffHandle.readTiff(geotiff_a)
    d = tiffHandle.readTiff(geotiff_b)
    overlay(a,b)
    
    
    
    

 