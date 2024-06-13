"""File used to visualize dose masks created for a dose level of 50% of the maximum 
dose found in the DSM. Used to find the number of connected dose regions in the DSM. """

import numpy as np
from HelperFunctions import get_pointcloud
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
import os


grad_01b = [elem for elem in grad_3 if elem in armB]

for elem in All_patients: 

    
    dir_path = "D:/Data/RS-DICOMfiles/"  + str(elem)

    for root, dirs, files in os.walk(dir_path):
        for file in files: 
    
            if file.endswith('.dcm'):
                print (root+'/'+str(file))

    Filename1 = root+'/'+str(file)

    pointdata, centroiddata = get_pointcloud('Esophagus',Filename1)

    slice_pos = centroiddata[:, 2]

    slice_thick = abs(slice_pos[1]-slice_pos[0])*0.1 # [cm]

    DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_EQD2/pat" + str(elem), dtype = float)
    dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/DimDSMPat" + str(elem), dtype=int)
    
    DSM = DSM_1d.reshape((dim[0], 100))

    max_dose = np.max(DSM_1d)
    target_dose = 0.5*max_dose
        
    DoseMask = (DSM>=target_dose).astype(int)
    
    import matplotlib.pyplot as plt 
    fig, ((ax1, ax3)) = plt.subplots(1, 2)
    f1 = ax1.pcolormesh(DSM, cmap='jet', vmin = 0, vmax = 60)
    fig.colorbar(f1,ax=ax1, label = 'Gy')
    ax3.pcolormesh(DoseMask, cmap='gray')
    for ax in fig.get_axes():
        ax.label_outer()
    ax1.set_xticks([])
    ax3.set_xticks([])
    ax1.set_yticks([])
    ax3.set_yticks([])
    plt.show()
