"""
Performing a rotation of DSMs to map the highest dose region to the center of the dose map.
This was done in order to create average DSMs for each toxicity group
"""

import numpy as np
from extrahelpers import rotateHorizontally, rotateVertically, collectCSVData, clustermask, getCentroidofMask
from skimage.transform import resize

from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients


for pat_number in All_patients: 

    # Collect necessary data: dimensions of dose matrix, voxelsizes, generated original DSMs with dimensions.

    DSM_1d = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/Original_DSMs_EQD2_scaled/pat" + str(pat_number), dtype = float)

    DSM_shape_scaled = np.genfromtxt("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DimScaledDSM/DimScaledRot_DSM" + str(pat_number) , dtype = int)

    DSM = DSM_1d.reshape((DSM_shape_scaled[0], DSM_shape_scaled[1]))

    target_Gy = max(DSM_1d)*0.9 #Used for most patients. Adjusted when the rotation was not optimal

    target_ind_x = 50
    target_ind_y = int(DSM_shape_scaled[0]/2)

    # Creating a cluster for the target dose. 

    cluster = clustermask(DSM, target_Gy)
    centroid = getCentroidofMask(cluster)

    # Finding the centroid of the cluster 

    current_ind_x = int(round(centroid[0],0))
    current_ind_y = int(round(centroid[1],0))

    # Rotating the DSM horizontally until the x value of the centroid is located in
    # the center of the map.
    
    for i in range(0,100):
        DSM_rot_x = rotateHorizontally(DSM, i)
        cluster_rot_x = clustermask(DSM_rot_x, target_Gy)
        centroid_rot_x = getCentroidofMask(cluster_rot_x)
        current_ind_x = int(round(centroid_rot_x[0],0))
        if current_ind_x == target_ind_x:
            break

    # Displacing the DSM vertically until the y value of the centroid is located in
    # the center of the map.
    
    for j in range(DSM_shape_scaled[0]):
        DSM_rot = rotateVertically(DSM_rot_x, j)
        cluster_rot = clustermask(DSM_rot, target_Gy)
        centroid_rot = getCentroidofMask(cluster_rot)
        current_ind_y = int(round(centroid_rot[1],0))
        if current_ind_y == target_ind_y:
            break

    # For the patients who had difficult dose maps to rotate: the range og i and j and the 
    # target Gy was manually adjusted until the best rotation was reached. 

    # Saving the rotated DSM 

    # DSM_rot.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMs_EQD2_scaled_rotated/pat" + str(pat_number), sep = '\n')
    

    # Plot the DSM, the cluster mask (rotated) and the rotated DSM to visually check the rotation. 
    # Not optimal rotation: adjust target_Gy and range of the vertical/horisontal rotation if necessary and try again. 

    import matplotlib.pyplot as plt 
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    plt.title("Patient nr. " + str(pat_number))
    ax1.pcolormesh(DSM, cmap='jet')
    ax1.plot(centroid[0], centroid[1], 'o', color='black', markerfacecolor='red')
    ax1.plot(50, int(DSM_shape_scaled[0]/2), 'o', color='black',markerfacecolor='black')

    
    ax2.pcolormesh(cluster_rot, cmap = 'hot')
    ax2.plot(50, DSM_rot.shape[0]/2, 'o', color='black',markerfacecolor='black')
    ax2.plot(centroid_rot[0], centroid_rot[1], 'o', color='black',markerfacecolor='red')

    f = ax3.pcolormesh(DSM_rot, cmap = 'jet')
    ax3.plot(50, DSM_shape_scaled[0]/2, 'o', color='black',markerfacecolor='black')
    for ax in fig.get_axes():
        ax.label_outer()
    ax1.set_title("DSM - Patient nr. " + str(pat_number))
    ax2.set_title("Cluster_rotated"); ax3.set_title("DSM scaled and rotated")
    ax1.set_xticks(np.linspace(0, 100, 4));ax2.set_xticks(np.linspace(0, 100, 4));ax3.set_xticks(np.linspace(0, 100, 4))
    ax1.set_yticks(np.linspace(0, DSM_shape_scaled[0], 8));ax2.set_yticks(np.linspace(0, DSM_shape_scaled[0], 8));ax3.set_yticks(np.linspace(0, DSM_shape_scaled[0], 8))
    ax1.set_ylabel("Position along the Esophagus (cm)")
    ax2.grid()
    ax3.grid()
    plt.show()

