from readTiff import tiffHandle
from osgeo import gdal
import numpy as np
import osr
import argparse
from perpendicular_distance import perp_dist 
from exampleDP.py import generaliseDP
import matplotlib.pyplot as plt
from interpolatePoints import interpolateLine
from scipy import interpolate
import pseudoRaster


class contour_lines_(tiffHandle):
    
    def sortZ(self):
        '''
        Function to make sure each z is int for the following calculation
        '''
        self.newZ = int(self.z)


    def contour_lines_range(self,interval):
        '''
        Function to determine interval by user and set each value based on the interval
        '''
        maxZ = max(self.newZ)
        minZ = min(self.newZ)
        lenZ = maxZ-minZ

        self.block = int(lenZ/interval)

        # set values
        if(np.where(self.data == 0)):
            return -999.0
        else:
            for i in range(1,self.block):
                newblock = self.block*i
                eachrange = minZ+self.block*i
                self.interval_range= np.where(self.data == newblock, eachrange)
                i = i + 1


    def plot_contour_line(self,res,bounds):
        '''
        Function to plot contour line by interpolateline
        '''
        pseudoRaster(res,bounds)

        #Construct a 2-D grid and interpolate on it
        x = np.arrange(self.minX,self.maxX,self.interval_range)
        y = np.arrange(self.minY,self.maxY,self.interval_range)
        xx, yy = np.meshgrid(x, y)
        z = self.newZ
        f = interpolate.interp2d(x, y, z, kind='cubic')

        #use the obtained interpolation function and plot the result
        xnew = np.arange(self.minX,self.maxX,self.interval_range)
        ynew = np.arange(self.minY,self.maxY,self.interval_range)
        znew = f(xnew, ynew)

        #process of connecting the dots by plt.contourf(it can also help create contour line)
        contourf = plt.contourf(xnew, ynew, znew, self.interval_range, alpha=.6, cmap=plt.cm.jet)

        #use Douglas-Peucker line generalisation(maybe unnecessary due to the type of 'cubic') 
        startInd=0
        endInd=len(xnew)-1
        # create a list to hold the results. Put first two breakpoints in
        nodeIndices=[startInd,endInd]
        # call generaliser
        generaliseDP(startInd,endInd,xnew,ynew,contourf,nodeIndices)
        # sort the indices, as they will be in a funny order
        sortedIndices=np.sort(nodeIndices)

        plt.show(sortedIndices)





if __name__=="__main__":
    filename = 'task2_map1_3.tif'
    
    tiffHandle.readTiff(filename)
    contour_lines_range(10)
