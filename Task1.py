



from pyproj import Proj, transform # package for reprojecting data
from processLVIS import lvisGround
from handleTiff import tiffHandle
from scipy.ndimage.filters import gaussian_filter1d
from osgeo import gdal             # pacage for handling geotiff data
from osgeo import osr              # pacage for handling projection information
from gdal import Warp
import numpy as np
import h5py

# class RasterProcessing(lvisGround,tiffHandle):




if __name__=="__main__":
  '''Main block'''

  filename='/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/ILVIS1B_AQ2015_1017_R1605_043439.h5'

  b=lvisGround(filename,onlyBounds=True)
  k = 0

  # set some bounds
  for i in range(15):
      for j in range(15):
          x0=(b.bounds[2]-b.bounds[0])*i/15 + b.bounds[0]
          y0=(b.bounds[3]-b.bounds[1])*j/15 + b.bounds[1]
          x1=(b.bounds[2]-b.bounds[0])*(i+1)/15+b.bounds[0]
          y1=(b.bounds[3]-b.bounds[1])*(j+1)/15+b.bounds[1]

    
          c = lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)
          
          if(c.value=='no data'):
              print('no data')
          
              
          else:
              k = k + 1
              epsg = 3031
              c.reproject(4326,epsg)
              if(k==1):                 # if it is the first part of data
                  
                
                  x = c.lon
                  y = c.lat
                  c.setElevations()
                
                  data = c.estimateGround()             #get elevation data after denoised and save in 'data'
                  minX=np.min(x)
                  maxX=np.max(x)
                  minY=np.min(y)
                  maxY=np.max(y)
                
                  res = 10                              #set the resolution
                
                  nx=int((maxX-minX)/res+1)
                  ny=int((maxY-minY)/res+1)
              else:                                     #combine data of each part into one array
                  x = np.concatenate([x,c.lon])
                  y = np.concatenate([y,c.lat])
                  c.setElevations()
                  data = np.concatenate([data,c.estimateGround()])
                  
                  minX=np.min(x)
                  maxX=np.max(x)
                  minY=np.min(y)
                  maxY=np.max(y)
                
                  res = 10
                  
                  nx=int((maxX-minX)/res+1)
                  ny=int((maxY-minY)/res+1)
            
            
            
  tiff = tiffHandle(filename,minX,minY,maxX,maxY,nx,ny,x,y)
  new_filename = 'task1_1.tif'
  f=h5py.File(filename,'r')
  tiff.writeTiff(data,res,new_filename,epsg)
