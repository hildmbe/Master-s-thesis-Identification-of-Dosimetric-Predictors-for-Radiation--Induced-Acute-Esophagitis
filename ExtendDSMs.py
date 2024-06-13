"""
Program used to extend the DSMs in order to create average DSMs. 

"""

import numpy as np
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
import matplotlib.pyplot as plt

# The maximal dimension for the scaled DSMs observed in the patient population
# The DSMs will be scaled to this dimension (546, 100) which was the maximum 
# observed dimension in the patient population
# The extention of the DSMs is necessary in order to be able to create 
# average DSMs.

max_dim = 546 

pat = 0

for pat_number in All_patients: 

    pat += 1
    print(pat)
    # Loading the flattened DSM and corresponding shape of the DSM. Reshape the flattened DSM to the correct 2d-array

    DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated/pat" + str(pat_number), dtype = float)

    dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

    DSM = DSM_1d.reshape((dim[0], dim[1]))

    # Finding the difference in dimensions between the current DSM and the maximal dimension. 

    diff_dim = max_dim - dim[0]

    # Adding rows of zero dose on the top and bottom of the dose map until 
    # the dimensions corresponds to the maximal dimension observed among the patients. 

    for i in range(diff_dim//2):
        arr_ny = np.insert(DSM, 0, 0, axis = 0)
        np.insert(arr_ny, 0, 0, axis = 0)
        DSM = arr_ny
    for j in range(diff_dim//2):
        ny_arr = np.append(DSM, np.array([np.zeros(100)]), axis = 0)
        DSM = ny_arr 
    
    if DSM.shape[0] != 546:
        nyest_arr = np.append(DSM, np.array([np.zeros(100)]), axis = 0)
        DSM = nyest_arr 
   
    # Save the extended DSM. 

    DSM.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat" + str(pat_number), sep = '\n')

