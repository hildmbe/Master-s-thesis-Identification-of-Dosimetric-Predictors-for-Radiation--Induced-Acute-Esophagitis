""" 

Calculating parameters of a DSM for doselevels between 0 and 60 Gy. 

Calculates the features of a DSM:  
- area: The percent of the total DSM area covered by the doseMask
- length: 
- length of full coverage: The length of the DSM that received at least 80% circumferential coverage
- areaXdose: The relative area of a dose mask multiplied with the mean dose within that area. 
- grade_circ: The average percentage of circumference irradiated in a dose mask. 
- grade_of_circ_max_consecutive: 
- grade_of_circ_max: 
- 
""" 

import numpy as np
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
from extrahelpers import collectCSVData, get_pointcloud, DSM_features
import matplotlib.pyplot as plt
import csv
import os
import pyvista as pv

dose_l = np.arange(0, 60, 1)

for pat_number in All_patients:

    # Collecting the point cloud of the esophagus in order to find the CT slice thickness. Used for the calculation of the DSM parameters. 
    dir_path = "D:/Data/RS-DICOMfiles/"  + str(pat_number)

    for root, dirs, files in os.walk(dir_path):
        for file in files: 
    
            if file.endswith('.dcm'):
                print (root+'/'+str(file))

    Filename1 = root+'/'+str(file)

    pointdata, centroiddata = get_pointcloud('Esophagus',Filename1)

    slice_pos = centroiddata[:, 2]

    slice_thick = abs(slice_pos[1]-slice_pos[0])*0.1 # [cm]

    dir_path_DSM = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_armB_30frac_EQD2/"
    
    for root, dirs, files in os.walk(dir_path_DSM):
        for file in files: 
    
            if file.endswith("Pat" + str(pat_number)):
                #print (root+'/'+str(file))

                DSM_1d= np.genfromtxt(root+'/'+str(file), dtype = float)

    dir_path_dim = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/"
    
    for root1, dirs1, files1 in os.walk(dir_path_dim):
        for file1 in files1: 
            if file1.endswith("DSMPat" + str(pat_number)):
                #print (root1+'/'+str(file1))

                dim = np.genfromtxt(root1+'/'+str(file1), dtype=int)

    DSM = DSM_1d.reshape(dim[0], dim[1])

    # Creating lists for DSM parameters to be collected 

    circ_max = []; length = []; area = []; length_full = []; areaXdose = []; circ_avg = []
    circ_max_consecutive = []
    counter = 0 
    
    for elem in dose_l:
    
        try: 
            # Creating a dose mask for each dose level and collecting features decribing this dose mask

            doseMask = (DSM>=elem).astype(int)
            
            features = DSM_features(doseMask, slice_thick)
            
            area.append(features['area']); length.append(features['length']); 
            circ_max.append(features['grade_of_circ_max'])
            length_full.append(features['length_full_coverage']); 
            circ_avg.append(features['mean_grade_of_circ'])
            circ_max_consecutive.append(features['grade_of_circ_max_concecutive'])

            doses = []
            for bin, dose in zip(doseMask.flatten(), DSM.flatten()):
                if bin == 1:
                    doses.append(dose)

            avg_dose = np.mean(doses)

            areaXdose.append(avg_dose*features['area']*0.01)

            counter += 1
        except:
            # If no doses above elem exist in the DSM: 
            break

    for i in range(60-counter):
        circ_max.append(0); 
        length.append(0); area.append(0); areaXdose.append(0)
        length_full.append(0); 
        circ_avg.append(0)
        circ_max_consecutive.append(0)

    #Saving the DSM features to CSV files. 

    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Circumference_average.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + circ_avg) 

    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Circumference_max.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + circ_max) 
    
    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Circumference_max_sammenhengende.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + circ_max_consecutive) 
    
    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Length_full_coverage.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + length_full) 

    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Length.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + length) 

    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/Area.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + area)

    with open("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/areaXdose.csv", 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        #csvwriter.writerow(['Pasient'] + dose_l.tolist())
        csvwriter.writerow([pat_number] + areaXdose)
