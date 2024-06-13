
'''File used to convert the DSMs in the 40-fraction group to only include 30 fractions. 
The original DSMs (physical dose) were scaled so that only 30 fractions were included
and then the result were converted into EQD2 with n=30 fractions. '''

import numpy as np
from HelperFunctions import collectCSVData, get_pointcloud, convertDSMtoEQD2
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
import os


for pat_number in armB:

    # Loading original DSM (physical dose) with associated dimensions
    DSM_1d= np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs/DSMpat"+str(pat_number)+".txt", dtype = float)/100
    
    dimDSM = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/DimDSMPat" +str(pat_number), dtype=int)
    
    DSM = DSM_1d.reshape((dimDSM[0], dimDSM[1]))

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

    print(str(pat_number) + '::' + str(n_frac))

    aB = 10 

    # Scaling the orginal DSMs to only include 30 fractions

    Fractions30DSM = (DSM*1/n_frac) * 30

    # Converting the result into EQD2
    
    EQD2_30 = convertDSMtoEQD2(Fractions30DSM, 30, aB)

    # Saving the result
    
    #EQD2_30.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_armB_30frac_EQD2/Pat" + str(pat_number), sep = '\n')
    

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()  
    f = ax.pcolormesh(EQD2_30, cmap='jet', vmin = 0, vmax=60)
    fig.colorbar(f,ax=ax, label = 'Gy (EQD2)')
    plt.title("DSM 30 frac - Patient nr. " + str(pat_number) + ' - $EQD_2$ with $\\alpha / \\beta$=10', fontsize = 10)
    ax.set_yticks(np.arange(0, len(slice_pos), 5/(abs(slice_pos[1]-slice_pos[0])*0.1)), labels=labels)
    ax.set_xticks([])
    plt.ylabel("Length along the Esophagus (cm)")
    plt.xlabel("L                   P                  R                  A                   L")
    #plt.savefig("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Figures/Original_DSMs_armB_30frac_EQD2/Pat" + str(pat_number))
    #plt.show()

    
