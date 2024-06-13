""" 
Converting the DSMs to EQD2 with an alpha/beta = 10. 

""" 

import numpy as np
from extrahelpers import get_pointcloud, convertDSMtoEQD2
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
import os

for pat_number in All_patients:

    # Loading point cloud of esophagus to retrive the CT slice thickness. Used for plotting correct lengths. 
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

    # Loading the original DSMs (physical dose) with associated dimensions

    dimDSM = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/DimDSMPat" + str(pat_number), dtype = int)

    DSM_1d= np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs/DSMpat" + str(pat_number) + ".txt")/100

    DSM = DSM_1d.reshape((dimDSM[0], dimDSM[1]))
    
    aB = 10 

    # Converting the DSMs to EQD2 and saving the result.

    DSM_EQD2 = convertDSMtoEQD2(DSM, n_frac, aB)
    
    #DSM_EQD2.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_EQD2/pat" + str(pat_number), sep = '\n')

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()  
    f = ax.pcolormesh(DSM_EQD2, cmap='jet', vmin = 0, vmax = 60)
    fig.colorbar(f,ax=ax, label = 'Gy')
    plt.title("Dose Surface Map - Patient nr. " + str(pat_number) + ' - $EQD_2$ with $\\alpha / \\beta$=10', fontsize = 10)
    ax.set_yticks(np.arange(0, len(slice_pos), 5/(abs(slice_pos[1]-slice_pos[0])*0.1)), labels=labels)
    ax.set_xticks([])
    plt.ylabel("Length along the Esophagus (cm)")
    plt.xlabel("L                   P                  R                  A                   L")
    plt.show()


    

