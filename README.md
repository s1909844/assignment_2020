# assignment_2020
This contains the files needed for the 2020 OOSA assignment,which can help handle the NASA LVIS sensor data to make the spatial analysis.We will be using files from Operation IceBridge, which bridged the gap between ICESat and ICESat-2 using aircraft.
## Task1.py
A main block to call the function inside lvisClass, handleTiff and processLVIS files to process a flight line of one single LVIS flight line to a DEM of any chosen resolution in geotiff format.

The data is stored as the variables:

    outepsg: output coordinate system
    inepsg:  input coordinate system
