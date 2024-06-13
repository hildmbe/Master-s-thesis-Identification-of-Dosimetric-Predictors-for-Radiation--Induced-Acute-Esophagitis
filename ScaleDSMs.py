"""
Performing a scaling of DSMs to a standard pixel-size so that when we create average DSMs, 
the length in the superior - inferior direction will be absolute and not relative. 
"""

import numpy as np
from extrahelpers import rotateHorizontally, rotateVertically, collectCSVData, get_pointcloud
from skimage.transform import resize
import os

from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients

for pat_number in All_patients: 

    # Loading the original DSMs (EQD2) and associated dimensions
    dir_path_DSM = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_EQD2/"
    
    for root, dirs, files in os.walk(dir_path_DSM):
        for file in files: 
    
            if file.endswith("pat" + str(pat_number)):
                #print (root+'/'+str(file))

                DSM_1d= np.genfromtxt(root+'/'+str(file), dtype = float)

    dir_path_dim = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/"
    
    for root1, dirs1, files1 in os.walk(dir_path_dim):
        for file1 in files1: 
            if file1.endswith("Pat" + str(pat_number)):
                #print (root1+'/'+str(file1))

                DSM_shape = np.genfromtxt(root1+'/'+str(file1), dtype=int)

    # Loading the point cloud of the esophagus to retrive the slice thickness. Needed to correctly scale the DSMs. 
    dir_path = "D:/Data/RS-DICOMfiles/"  + str(pat_number) 
    
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
    
            if file.endswith('.dcm'):
                print (root+'/'+str(file))

    Filename1 = root+'/'+str(file)

    pointdata, centroiddata = get_pointcloud('Esophagus',Filename1)

    slice_pos = centroiddata[:, 2]

    labels = []
    for elem in np.arange(0, len(slice_pos)*abs(slice_pos[1]-slice_pos[0])*0.1, 5):
        labels.append(str(elem))

    
    DSM = DSM_1d.reshape((DSM_shape[0], DSM_shape[1]))

    slice_thick = abs(slice_pos[1]-slice_pos[0])*0.1
    
    # Scale the DSM to a pixelsize corresponding to a longitudinal distance of 
    # 0.05 cm along the esophageal length (in the superior - inferior direction)
    # Using the slice thickness to get the correct scaling 
    # resize perfroms an interpolation between the pixels in the DSM. 
    
    DSM_scaled= resize(DSM,(DSM_shape[0]*(slice_thick*10/0.5), 100))
    scaled_shape = np.array([DSM_scaled.shape[0], DSM_scaled.shape[1]])
    
    # Saving the scaled DSM with dimensions. 

    #DSM_scaled.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_EQD2_scaled/pat" + str(pat_number), sep = '\n')
    
    #scaled_shape.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" + str(pat_number), sep = '\n')

    
    

