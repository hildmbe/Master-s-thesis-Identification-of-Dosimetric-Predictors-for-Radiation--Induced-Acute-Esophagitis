"""
File used to create average DSMs per grade of esophagitis
"""

import numpy as np
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
import os

DSMs_3s= []

curr3 = [elem for elem in grad_3 if elem in All_patients]

# Loading the DSMs with grade 3 esophagitis and storing them in DSMs_3s

counter_3 = 0
for pat_number in curr3:
    dir_path_DSM = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/"
    
    for root, dirs, files in os.walk(dir_path_DSM):
        for file in files: 
    
            if file.endswith("pat" + str(pat_number)):
                #print (root+'/'+str(file))

                DSM_1d= np.genfromtxt(root+'/'+str(file), dtype = float)

    dir_path_dim = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/"
    
    for root1, dirs1, files1 in os.walk(dir_path_dim):
        for file1 in files1: 
            if file1.endswith("DSM" + str(pat_number)):
                #print (root1+'/'+str(file1))

                dim = np.genfromtxt(root1+'/'+str(file1), dtype=int)
    
    dims = 546

    counter_3 += 1
    DSM = DSM_1d.reshape((dims, 100))

    DSMs_3s.append(DSM)


# Calculate the average of the DSMs in the grade 3 group
avgDSM_3 = np.average(DSMs_3s, axis = 0)
avgDSM_3 = avgDSM_3.reshape(546, 100)

labels_3 = []

for elem in np.arange(0, avgDSM_3.shape[0]*0.05, 5):
    labels_3.append(str(elem))

##################################################################################
DSMs_2s= []

curr2 = [elem for elem in grad_2 if elem in All_patients]

counter_2 = 0

# Loading the DSMs with grade 2 esophagitis and storing them in DSMs_2s

for pat_number in curr2:
    dir_path_DSM = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/"
    
    for root, dirs, files in os.walk(dir_path_DSM):
        for file in files: 
    
            if file.endswith("pat" + str(pat_number)):
                #print (root+'/'+str(file))

                DSM_1d= np.genfromtxt(root+'/'+str(file), dtype = float)

    dir_path_dim = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/"
    
    for root1, dirs1, files1 in os.walk(dir_path_dim):
        for file1 in files1: 
            if file1.endswith("DSM" + str(pat_number)):
                #print (root1+'/'+str(file1))

                dim = np.genfromtxt(root1+'/'+str(file1), dtype=int)
    
    dims = 546

    counter_2 += 1
    DSM = DSM_1d.reshape((dims, 100))

    DSMs_2s.append(DSM)


# Calculate the average of the DSMs in the grade 2 group. 
avgDSM_2 = np.average(DSMs_2s, axis = 0)
avgDSM_2 = avgDSM_2.reshape(546, 100)

labels_2 = []

for elem in np.arange(0, avgDSM_2.shape[0]*0.05, 5):
    labels_2.append(str(elem))

####################################################################################
DSMs_01s = []

curr01 = [elem for elem in grad_01 if elem in All_patients]
counter_01 = 0
# Loading the DSMs with grade 0-1 esophagitis and storing them in DSMs_01s
for pat_number in curr01:
    dir_path_DSM = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated_extended/"
    
    for root, dirs, files in os.walk(dir_path_DSM):
        for file in files: 
    
            if file.endswith("pat" + str(pat_number)):
                #print (root+'/'+str(file))

                DSM_1d= np.genfromtxt(root+'/'+str(file), dtype = float)

    dir_path_dim = "C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/"
    
    for root1, dirs1, files1 in os.walk(dir_path_dim):
        for file1 in files1: 
            if file1.endswith("DSM" + str(pat_number)):
                #print (root1+'/'+str(file1))

                dim = np.genfromtxt(root1+'/'+str(file1), dtype=int)
                

                #DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/EQD2_DSM_ab10_extended/Grad_3/pat"+str(pat_number), dtype = float)
                #dim = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/Arm_B/Grad_3/DimScaledRot_DSM" +str(pat_number), dtype=int)

    dims = 546

    counter_01 += 1
    DSM = DSM_1d.reshape((dims, 100))

    DSMs_01s.append(DSM)


# Calculate the average of the DSMs for the grade 0-1 group. 
avgDSM_01 = np.average(DSMs_01s, axis = 0)
avgDSM_01 = avgDSM_01.reshape(546, 100)


labels_01 = []

for elem in np.arange(0, avgDSM_01.shape[0]*0.05, 5):
    labels_01.append(str(elem))
    
##########################################################################

# Creating average dose difference maps between the grades of esophagitis. 

difDSM_301 = (avgDSM_3.flatten() - avgDSM_01.flatten()).reshape(dims, 100)
difDSM_32 = (avgDSM_3.flatten() - avgDSM_2.flatten()).reshape(dims, 100)
difDSM_201 = (avgDSM_2.flatten() - avgDSM_01.flatten()).reshape(dims, 100)

##########################################################################
import matplotlib.pyplot as plt 

# Plotting the average DSMs

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
f1 = ax1.pcolormesh(avgDSM_01, cmap='jet', vmin = 0, vmax = 60)
f2 = ax2.pcolormesh(avgDSM_2, cmap='jet', vmin = 0, vmax = 60)
f3 = ax3.pcolormesh(avgDSM_3, cmap='jet', vmin = 0, vmax = 60)
CS1 = ax1.contour(avgDSM_01, levels = [10, 20, 30, 40, 50], colors=['black', 'black','black','black','black'], linewidths=1.5, linestyles = 'dotted' )
CS2 = ax2.contour(avgDSM_2, levels = [10, 20, 30, 40, 50], colors= ['black', 'black','black','black','black'], linewidths=1.5, linestyles = 'dotted')
CS3 = ax3.contour(avgDSM_3, levels = [10, 20, 30, 40, 50], colors = ['black', 'black','black','black','black'], linewidths=1.5, linestyles = 'dotted')

fmt = {}; fmt2 = {}; fmt3 = {}
strs = ['10Gy','20Gy', '30Gy', '40Gy', '50Gy']
for l, s in zip(CS1.levels, strs):
    fmt[l] = s

for l, s in zip(CS2.levels, strs):
    fmt2[l] = s

for l, s in zip(CS3.levels, strs):
    fmt3[l] = s

ax1.clabel(CS1, CS1.levels[::1], inline=True, fmt=fmt, fontsize=7)
ax2.clabel(CS2, CS2.levels[::1], inline=True, fmt=fmt2, fontsize=7)
ax3.clabel(CS3, CS3.levels[::1], inline=True, fmt=fmt3, fontsize=7)
#for ax in fig.get_axes():
    #ax.set_ylim(0,max(len(DSM1),len(DSM2)))
#fig.colorbar(f1, ax=ax1, label = "Gy")
#fig.colorbar(f2, ax=ax2, label = "Gy")
fig.colorbar(f3, ax=ax3, label = "Gy (EQD2)")
fig.suptitle("All patients")

ax1.set_yticks(np.arange(0, avgDSM_01.shape[0], 5/0.05), labels=labels_01)
ax2.set_yticks(np.arange(0, avgDSM_2.shape[0], 5/0.05), labels= ["", "", "", "", "", ""])
ax3.set_yticks(np.arange(0, avgDSM_3.shape[0], 5/0.05), labels= ["", "", "", "", "", ""])
ax1.set_xticks([]); ax2.set_xticks([]); ax3.set_xticks([]); 
ax1.set_ylabel("Length along the Esophagus (cm)")
ax1.set_title("Esophagitis \n CTCAE 0-1 (n=88)", fontsize = 10); ax2.set_title("Esophagitis \n CTCAE 2 (n=45)", fontsize = 10); ax3.set_title("Esophagitis \n CTCAE 3 (n=33)", fontsize = 10)
fig.supxlabel("Relative length along circumference", fontsize = 10)
fig.tight_layout()
plt.show()

# Plotting the average dose difference maps

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
f1 = ax1.pcolormesh(difDSM_301, cmap='coolwarm', vmin = -4, vmax = 25)
f2 = ax2.pcolormesh(difDSM_32, cmap = 'coolwarm', vmin = -4, vmax = 25)
f3 = ax3.pcolormesh(difDSM_201, cmap='coolwarm', vmin = -4, vmax = 25)

for ax in fig.get_axes():
    ax.set_ylim(0,max(len(avgDSM_3),len(avgDSM_2)))

cb = fig.colorbar(f3, ax=ax3, label = "$\Delta$Gy (EQD2)")
fig.suptitle("All patients")
#fig.suptitle("45 Gy / 30 fractions")
ax1.set_xticks([]); ax2.set_xticks([]); ax3.set_xticks([]); 
ax1.set_ylabel("Length along the Esophagus (cm)")
ax1.set_yticks(np.arange(0, avgDSM_01.shape[0], 5/0.05), labels=labels_01)
ax2.set_yticks(np.arange(0, avgDSM_3.shape[0], 5/0.05), labels= ["", "", "", "", "", ""])
ax3.set_yticks(np.arange(0, avgDSM_3.shape[0], 5/0.05), labels= ["", "", "", "", "", ""])
ax1.set_title("Esophagitis \n CTCAE 3 - CTCAE 01", fontsize = 10); ax2.set_title("Esophagitis \n CTCAE 3 - CTCAE 2", fontsize = 10); ax3.set_title("Esophagitis \n CTCAE 2 - CTCAE 01", fontsize = 10)
fig.supxlabel("Relative length along circumference", fontsize = 10)
fig.tight_layout()
plt.show()


