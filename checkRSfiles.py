"""

A program written to check the DICOM RS-files of the patients. 

The program checks for missing slices in the esophagus. 
It also checks if the CT slice thickness and the voxel size in the z direction are equal or not. 
"""

import numpy as np
from HelperFunctions import collectCSVData
import os
from Parameters import All_patients
from dicompylercore import dicomparser

for pat_number in All_patients:

    # Loading the RS-file and voxelsizes
    
    dir_path = "D:/Data/RS-DICOMfiles/" + str(pat_number)
    
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
            if file.endswith('.dcm'):
                print (root+'/'+str(file))

    RSfile = root+'/'+str(file)
    data_dim_sliceThickness = collectCSVData("D:/Data/DimAndPositions/Dim_Patnumber" + str(pat_number) +".csv")
    voxelsize_z = data_dim_sliceThickness[3]

    # Reading the RSfile and locating the structure information for the esophagus
    
    dp = dicomparser.DicomParser(RSfile)

    structures = dp.GetStructures()

    for elem in structures.items():
        if elem[1]['name'] == 'Esophagus':
            num_roi = elem[0]
            
    # Getting the coordinates of the contour of the esophagus. 
    coords = dp.GetStructureCoordinates(num_roi)

    list_keys = []

    for elem in coords.keys():
        list_keys.append(float(elem))

    slice_thickness = list_keys[5]-list_keys[4]

    a = len(list_keys)
    b = (list_keys[-1] - list_keys[0])/slice_thickness + 1
    
    # Checking if the slice thickness and the voxelsizes are equal or not
    
    if slice_thickness != voxelsize_z*10:
        print("Voxelsize and slicethikness not the same: " + str(pat_number))

    # Checking if the structure of the esophagus is whole or if slices are missing. 
    
    if a != round(b, 0):
        print("Missing one/several slices: " + str(pat_number))

    print(str(pat_number) + '::' + str(slice_thickness))

