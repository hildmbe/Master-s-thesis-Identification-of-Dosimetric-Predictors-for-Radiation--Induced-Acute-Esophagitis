import numpy as np
import matplotlib.pyplot as plt 
from extrahelpers import collectCSVData, get_pointcloud
from Parameters import All_patients, grad_01, grad_2, grad_3, armA, armB
import os

for pat_number in All_patients:
    print(pat_number)
    # Collect RS-file, dose matrix with dimensions and positions for each patient. 

    dir_path = "D:/Data/RS-DICOMfiles/"  + str(pat_number) 
    
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
    
            if file.endswith('.dcm'):
                print (root+'/'+str(file))
                
    Filename1 = root+'/'+str(file)
    data_dim_sliceThickness = collectCSVData("D:/Data/DimAndPositions/Dim_Patnumber" + str(pat_number) +".csv")

    dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimDSM/DimDSMPat" + str(pat_number), dtype = int)

    DSM = np.reshape(np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs/DSMpat" + str(pat_number) + ".txt")/100, (dim[0], 100))

    pointdata, centroiddata = get_pointcloud('Esophagus',Filename1)

    slice_pos = centroiddata[:, 2]

    labels = []
    for elem in np.arange(0, len(slice_pos)*abs(slice_pos[1]-slice_pos[0])*0.1, 5):
        labels.append(str(elem))

    fig, ax = plt.subplots()  
    f = ax.pcolormesh(DSM, cmap='jet')
    fig.colorbar(f,ax=ax, label = 'Gy')
    plt.title("Dose Surface Map - Patient nr. " + str(pat_number))
    ax.set_yticks(np.arange(0, len(slice_pos), 5/(abs(slice_pos[1]-slice_pos[0])*0.1)), labels=labels)
    ax.set_xticks([])
    plt.ylabel("Length along the Esophagus (cm)")
    plt.xlabel("L                   P                  R                  A                   L")
    plt.show()

