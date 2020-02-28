import gdal, ogr, osr, os
import numpy as np

def raster2array(rasterfn):
    '''
    Convert Raster to array
    '''

    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()

def getNoDataValue(rasterfn):
    '''
    Get no data value of array
    '''

    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.GetNoDataValue()

def array2raster(rasterfn,newRasterfn,array):
    '''
    Write updated array to new raster
    '''

    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()
    print("Image written to",newRasterfn)
    
def extract_data(rasterfn,rasterArray):
    '''
    Extracting the flight line data from the whole datasets
    '''
    noDataValue = getNoDataValue(rasterfn)       #get nodata from the datasets
    Vlocation = np.argwhere(rasterArray != noDataValue)     #find the location of the data which have true values from datasets

    #get the index of x and y
    Xlon = []
    Ylat = []

    #saving the index into lists
    for i in Vlocation:
        lonx = i[1]
        laty = i[0]
        Xlon.append(lonx)
        Ylat.append(laty)

    #geting the bounds of those true value data
    Xmax = max(Xlon)
    Xmin = min(Xlon)
    Ymax = max(Ylat)
    Ymin = min(Ylat)
    newArray = np.empty((Ymax-Ymin+1,Xmax-Xmin+1))
    Xindex = 0
    Yindex = 0

    #creat a new array to contain these data
    for yy in range(rasterArray.shape[0]):
        for xx in range(rasterArray.shape[1]):
            if(rasterArray[yy,xx]!=noDataValue):
                if(yy!=Yindex):             #save data when changing rows
                    Yindex = yy
                    Xindex = 0
                    newArray[Yindex,Xindex] = rasterArray[yy,xx]
                else:
                    newArray[Yindex,Xindex] = rasterArray[yy,xx]
                    Xindex = Xindex + 1
    return newArray,noDataValue  

def interpolation(noDataValue,newArray):
    '''
    Interpolation in the new array
    '''
    Location = np.argwhere(newArray == noDataValue)             #find the location of the nodata in the new array
    for i in Location:
        lonx = i[1]
        laty = i[0]
                                                               #set some bounds for interpolation to avoid out of bound
        if(lonx>1 and laty>1 and lonx<newArray.shape[1]-1 and laty<newArray.shape[0]-1):
            #define the value of pixels around the nodata value
            Vleft = newArray[laty,lonx-1]
            Vright = newArray[laty,lonx+1]
            Vup = newArray[laty+1,lonx]
            Vdown = newArray[laty-1,lonx]
            Vupleft = newArray[laty+1,lonx-1]
            Vupright = newArray[laty+1,lonx+1]
            Vdownleft = newArray[laty-1,lonx-1]
            Vdownright = newArray[laty-1,lonx+1]
    
            #To test whether the nodata is within the flight line datasets
            if((Vdown!=noDataValue and Vup!=noDataValue) or (Vleft!=noDataValue and Vright!=noDataValue) or (Vup!=noDataValue and Vleft!=noDataValue) or (Vup!=noDataValue and Vright!=noDataValue) or (Vleft!=noDataValue and Vdown!=noDataValue) or (Vright!=noDataValue and Vdown!=noDataValue)):
                #set the distances
                s1 = s2 = s3 = s4 = 1
                s5 = s6 = s7 = s8 = 1.414
    
                if(Vdown==noDataValue):
                    s1=0
                if(Vup==noDataValue):
                    s2=0
                if(Vleft==noDataValue):
                    s3=0
                if(Vright==noDataValue):
                    s4=0
                if(Vdownleft==noDataValue):
                    s5=0
                if(Vupleft==noDataValue):
                    s6=0
                if(Vdownright==noDataValue):
                    s7=0
                if(Vupright==noDataValue):
                    s8=0
                S=s1+s2+s3+s4+s5+s6+s7+s8
    
        #            print(laty)
                # if the nodata is out of the flight line
                if(Vdown==Vup==Vright==Vleft==noDataValue):
                    newArray[laty,lonx]=noDataValue
                else:
                #interpolate the new value
                    newArray[laty,lonx] = ((Vdown*s1+Vup*s2+Vleft*s3+Vright*s4+Vdownleft*s5+Vupleft*s6+Vdownright*s7+Vupright*s8)/S)
                    return newArray
                    
def conversion_back(rasterArray,newArray):
    location = np.argwhere(rasterArray != noDataValue)
    
    Xindex = 0
    Yindex = 0
    INdex = 1000000000
    for i in location:
        lonx = i[1]
        laty = i[0]
        if(laty==INdex):
            continue

        else:
            Len = newArray.shape[1]
            for l in range(Len):
                if(lonx+l<rasterArray.shape[1]):
                    rasterArray[laty,lonx+l] = newArray[Yindex,Xindex+l]   
                    print((laty,lonx+l))
                    print((Yindex,Xindex+l))
                    INdex = laty
            Yindex = Yindex + 1
    return rasterArray                  
    


rasterfn = 'task1_4.tif'
newValue = 0
newRasterfn = 'SlopeNew.tif'

# Convert Raster to array
rasterArray = raster2array(rasterfn)

#Extract the ture value fro mthe airfligt line data
newArray,noDataValue = extract_data(rasterfn,rasterArray)

#conversing the possible wrong value and 0 to noData before the interpolation
newArray[newArray<=-900]=noDataValue
newArray[newArray==0]=noDataValue

#Data interpolation
newArray = interpolation(noDataValue,newArray)

#transfer the value from newarray to the old array
rasterArray = conversion_back(rasterArray,newArray)






# Write updated array to new raster
array2raster(rasterfn,newRasterfn,rasterArray)
