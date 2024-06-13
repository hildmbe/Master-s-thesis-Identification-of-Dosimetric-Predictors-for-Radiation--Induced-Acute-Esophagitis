""" 
Performing a pixelwise multiple comparisons permutation test 
between the grades of esophagitis. 
""" 
import numpy as np
from skimage.transform import resize
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients

"""
Creating 3 groups to be compared: g1, g2, g3. Each group corresponds to a CTCAE grade of esophagitis. 

Creating g3 group
""" 

g3dsms = []

curr_3 = [elem for elem in grad_3 if elem in armB] # Switch between arms during testing 

for pat_number in curr_3:

    if pat_number in armB: 

        # Collect generated DSMs with dimensions and store it in variables. 

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to. 
        
        dims = 546

    elif pat_number in armA: 

        # Collect generated DSMs with dimensions and store it in variables.

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.

        dims = 546

    else: 

        # Collect generated DSMs with dimensions and store it in variables.

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.

        dims = 546

    #Reshape flattened DSM to 2d-array

    DSM = DSM_1d.reshape((dims, 100))

    g3dsms.append(resize(DSM, (300, 100)).flatten())
    
""" 
Creating g01 group
""" 

g01dsms = []

curr_01 = [elem for elem in grad_01 if elem in armB]

for pat_number in curr_01:

    if pat_number in armB: 
        
        # Collect generated DSMs with dimensions and store it in variables.
        
        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)
        
        # Define the correct extended dimension for the flattened DSM to be reshaped to.
        
        dims = 546
    elif pat_number in armA: 
        # Collect generated DSMs with dimensions and store it in variables.
        
        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.
        
        dims = 546

    else: 

        # Collect generated DSMs with dimensions and store it in variables.

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.

        dims = 546

    DSM = DSM_1d.reshape((dims, 100))

    g01dsms.append(resize(DSM, (300, 100)).flatten())

""" 
Creating g2 group
""" 


g2dsms = []

curr_2 = [elem for elem in grad_2 if elem in armB]

for pat_number in curr_2:

    if pat_number in armB: 

        # Collect generated DSMs with dimensions and store it in variables.

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.
        
        dims = 546

    elif pat_number in armA: 
        
        # Collect generated DSMs with dimensions and store it in variables.
        
        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)
        
        # Define the correct extended dimension for the flattened DSM to be reshaped to.
        
        dims = 546

    else: 

        # Collect generated DSMs with dimensions and store it in variables.

        DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/EQD2_DSM_ab10_extended/EQD2ab10EXTENDED_pat"+str(pat_number), dtype = float)
        dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" +str(pat_number), dtype=int)

        # Define the correct extended dimension for the flattened DSM to be reshaped to.

        dims = 546

    DSM = DSM_1d.reshape((dims, 100))

    g2dsms.append(resize(DSM, (300, 100)).flatten())

g01arr = np.array(g01dsms); g2arr = np.array(g2dsms); g3arr = np.array(g3dsms); g02arr = np.array(g01dsms+g2dsms);g23arr = np.array(g3dsms+g2dsms)

# Function to perform MCP tests between two outcome groups: g1 and g2. 

def MCP(g1, g2, Np):
    
    total_data = np.concatenate((g1, g2), axis = 0)

    E_mean_obs = np.average(g1, axis = 0) # Event vs Non-event outcome groups. 
    N_mean_obs = np.average(g2, axis=0)

    # Calculating the observed dose difference 
    
    observed_dose_diff = (E_mean_obs-N_mean_obs)

    dose_diff_per_permutation = np.empty((Np,len(total_data[0,:]))) # Where the dose difference maps for each permutation is going to be stored. 

    # Performing Np permutations
    for i in range(Np):
        # shuffle the labels and create two "new outcome groups" 
        np.random.shuffle(total_data)

        E = total_data[0:len(g1)] # The new shuffled outcome groups. 
        N = total_data[len(g1):]

        # Calculate the dose difference map of the permutation and store it in dose_diff_per_permutation
        
        E_mean = np.average(E, axis = 0)
        N_mean = np.average(N, axis=0)
        dose_diff = (E_mean-N_mean)

        dose_diff_per_permutation[i] = dose_diff

    # Calculate the standard deviation over every pixel over all the permutations. 
    Std_over_permutations = np.std(dose_diff_per_permutation,axis=0)

    # Normalize the dose difference maps of all the permutations by dividing with the standard deviation
    dose_diff_per_permutation_normalized = dose_diff_per_permutation/Std_over_permutations

    # Normalize the observed dose difference as well
    observed_dose_diff_normalized = observed_dose_diff/Std_over_permutations

    # Calculate the maximum normalized dose difference for each permutation
    T_max_per_permutation = np.max(dose_diff_per_permutation_normalized, axis = 1)

    # Calculate the maximum normalized dose difference in the observed sample
    T_max_obs = np.max(observed_dose_diff_normalized)

    # Calculate the adjusted p-value of the test 
    pval = len(np.where(T_max_per_permutation > T_max_obs)[0])/Np

    # creating a p-value map by calculating the (1-alpha) quantile for several alpha values (0.01, 0.05, 0.1). 
    
    T_star = np.quantile(T_max_per_permutation, 0.95)

    T_star_sig_01 = np.quantile(T_max_per_permutation, 0.99)

    T_star_sig_1 = np.quantile(T_max_per_permutation, 0.9)

    pvalmap = np.ones(len(observed_dose_diff_normalized))

    for i, elem in enumerate(observed_dose_diff_normalized):
        if elem > T_star and elem <= T_star_sig_01 :
            pvalmap[i] = 0.049
        elif elem > T_star_sig_01:
            pvalmap[i] = 0.0099
        elif elem > T_star_sig_1 and elem <= T_star:
            pvalmap[i] = 0.099
        
    formatted = "{:.7f}".format(pval) 

    print("pval:  "+ str(formatted)) 

    return E_mean_obs, N_mean_obs, observed_dose_diff_normalized, dose_diff_per_permutation, Std_over_permutations, pvalmap

# Performing a MCP test with 10 000 permutations. 
# Plotting the result

g3Mean, g01Mean, observed_dose_diff, dose_differences, std, pvalmap = MCP(g3arr, g01arr, 10000)

import matplotlib.pyplot as plt 
from matplotlib import colors, colorbar

fig, (a1,a2,a3) = plt.subplots(1,3)

fig.suptitle("60 Gy / 40 fractions")

# Plot the mean DSM of each group.
f1 = a1.pcolormesh(g3Mean.reshape(300, 100),cmap='jet', vmin = 0, vmax = 60)
f2 = a2.pcolormesh(g01Mean.reshape(300, 100),cmap='jet', vmin = 0, vmax = 60)
cb1 = fig.colorbar(f1, ax=a1)
cb2 = fig.colorbar(f2, ax=a2)
a1.set_title('Esophagtis \n CTCAE 3 (n=15)', fontsize = 10)
a2.set_title('Esophagtis \n CTCAE 0-1 (n=45)', fontsize = 10)

# Plot the p-value map
a3.set_title('p-value map', fontsize = 10)

a1.set_yticks(np.arange(0, 300, 5*300/27.3), labels=['0.0','5.0', '10.0', '15.0', '20.0', '25.0'])
a2.set_yticks(np.arange(0, 300, 5*300/27.3), labels= ["", "", "", "", "", ""])
a3.set_yticks(np.arange(0, 300, 5*300/27.3), labels= ["", "", "", "", "", ""])
a1.set_xticks([]); a2.set_xticks([]); a3.set_xticks([]); 
cmapMCP = colors.ListedColormap(['white','lightgrey' ,'grey','#151515'])
norm = colors.BoundaryNorm([0,0.01, 0.05, 0.1, 1], cmapMCP.N)

f3 = a3.pcolormesh(pvalmap.reshape(300, 100), cmap = cmapMCP, norm = norm)
fig.colorbar(f3, ax = a3)
CS1 = a1.contour(pvalmap.reshape(300, 100), levels = [0.05], colors = 'white', linewidths=1.5)
CS2 = a2.contour(pvalmap.reshape(300, 100), levels = [0.05], colors ='white', linewidths=1.5)
a1.set_ylabel('Length along the Esophagus (cm)', fontsize = 10)
fig.supxlabel("Relative length along circumference", fontsize = 10)
fig.tight_layout()
plt.show()

