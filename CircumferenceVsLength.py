import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set_theme()
from Parameters import grad_01, grad_2, grad_3, armA, armB,  All_patients
from extrahelpers import collectCSVData_Nr2 


data_circ = collectCSVData_Nr2("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParameters/Circumference_median.csv")

data_length = collectCSVData_Nr2("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParameters/Length.csv")

data_mean_dose = collectCSVData_Nr2("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/EUD_AllePas.csv")

def Plot(armX, data_l, data_c, j, marker):
    counter = 0
    circ_3, circ_2, circ_01 = [], [], []
    length_3, length_2, length_01 = [], [], []
    circ_3_ekstra, circ_2_ekstra, circ_01_ekstra = [], [], []
    length_3_ekstra, length_2_ekstra, length_01_ekstra = [], [], []
    s3, s2, s01 = [], [], []
    s3_ekstra, s2_ekstra, s01_ekstra = [], [], []
    for row_c, row_l in zip(data_c, data_l):
        pat_id = row_c[0]
        if pat_id in armX:

            for elem in data_mean_dose:
                if elem[0] == pat_id:
                    #mean_dose = elem[1]
                    mean_dose = 5
                

            if pat_id in grad_3:
                circ_3.append(row_c[j])
                length_3.append(row_l[j])

                s3.append(mean_dose*5)

            elif pat_id in grad_2:
                circ_2.append(row_c[j])
                length_2.append(row_l[j])

                s2.append(mean_dose*5)
                

            elif pat_id in grad_01:
                circ_01.append(row_c[j])
                length_01.append(row_l[j])

                s01.append(mean_dose*5)

            if row_c[j]==0 and row_l[j]==0:
                place = counter*1
                counter += 1

                if pat_id in grad_3:
                    circ_3_ekstra.append(place)
                    length_3_ekstra.append(0)
                    s3_ekstra.append(mean_dose*5)
                elif pat_id in grad_2:
                    circ_2_ekstra.append(place)
                    length_2_ekstra.append(0)
                    s2_ekstra.append(mean_dose*5)
                elif pat_id in grad_01:
                    circ_01_ekstra.append(place)
                    length_01_ekstra.append(0)
                    s01_ekstra.append(mean_dose*5)



    circ_01 = np.array(circ_01)
    length_01 = np.array(length_01)
    points_01 = []

    for elem_c, elem_l in zip(circ_01, length_01):
        points_01.append(np.sqrt(elem_c**2 + elem_l**2))

    sorted_indiced = np.argsort(points_01)
    circ_01_included = circ_01[sorted_indiced]
    len_01_included = length_01[sorted_indiced]

    n_01 = int(np.floor(len(circ_01)*0.15))
    print(n_01)

    x_90_01 = circ_01_included[n_01:]
    y_90_01 = len_01_included[n_01:]

# Determine the minimum and maximum values of the selected points
    min_x_01, max_x_01 = np.min(x_90_01), np.max(x_90_01)
    min_y_01, max_y_01 = np.min(y_90_01), np.max(y_90_01)
######################################################################

    circ_2 = np.array(circ_2)
    length_2 = np.array(length_2)
    points_2 = []

    for elem_c, elem_l in zip(circ_2, length_2):
        points_2.append(np.sqrt(elem_c**2 + elem_l**2))

    sorted_indiced = np.argsort(points_2)
    circ_2_included = circ_2[sorted_indiced]
    len_2_included = length_2[sorted_indiced]
    n_2 = int(np.floor(len(circ_2)*0.15))
    x_90_2 = circ_2_included[n_2:]
    y_90_2 = len_2_included[n_2:]

# Determine the minimum and maximum values of the selected points
    min_x_2, max_x_2 = np.min(x_90_2), np.max(x_90_2)
    min_y_2, max_y_2 = np.min(y_90_2), np.max(y_90_2)

# Plot the scatter plot
################################################################################

    circ_3 = np.array(circ_3)
    length_3 = np.array(length_3)
    points_3 = []

    for elem_c, elem_l in zip(circ_3, length_3):
        points_3.append(np.sqrt(elem_c**2 + elem_l**2))

    sorted_indiced = np.argsort(points_3)
    circ_3_included = circ_3[sorted_indiced]
    len_3_included = length_3[sorted_indiced]

    n_3 = int(np.floor(len(circ_3)*0.15))
    x_90_3 = circ_3_included[n_3:]
    y_90_3 = len_3_included[n_3:]

# Determine the minimum and maximum values of the selected points
    min_x_3, max_x_3 = np.min(x_90_3), np.max(x_90_3)
    min_y_3, max_y_3 = np.min(y_90_3), np.max(y_90_3)
    #sns.set_style('whitegrid')
# Plot the box around the 90% points
    plt.plot([min_x_3, max_x_3, max_x_3, min_x_3, min_x_3], [min_y_3, min_y_3, max_y_3, max_y_3, min_y_3], color='blue', linestyle = 'dashed', alpha = 0.7)
    plt.plot([min_x_2, max_x_2, max_x_2, min_x_2, min_x_2], [min_y_2, min_y_2, max_y_2, max_y_2, min_y_2], color='orange', linestyle = 'dashed', alpha = 0.7)
    plt.plot([min_x_01, max_x_01, max_x_01, min_x_01, min_x_01], [min_y_01, min_y_01, max_y_01, max_y_01, min_y_01], color='green', linestyle = 'dashed', alpha = 0.7)

    plt.scatter(circ_3, length_3, label = '3 (n=15)', marker = marker, s = s3, alpha = 0.7)
    plt.scatter(circ_2, length_2, label = '2 (n=23)',  marker = marker, s=s2, alpha = 0.7)
    plt.scatter(circ_01, length_01, label = '0-1 (n=40)', marker = marker, s=s01, alpha = 0.7)
    plt.scatter(circ_3_ekstra, length_3_ekstra, marker = marker, s = s3_ekstra, color = 'blue', alpha = 0.7)
    plt.scatter(circ_2_ekstra, length_2_ekstra, marker = marker, s = s2_ekstra,  color = 'orange', alpha = 0.7)
    plt.scatter(circ_01_ekstra, length_01_ekstra, marker = marker, s = s01_ekstra, color = 'green', alpha = 0.7)
    plt.xlabel('Average proportion of circumference receving $\geq$ 30 Gy (%)', fontsize = 20)
    #plt.plot(np.linspace(0, 100, 100), np.ones(100)*6.5)
    plt.ylabel('Absolute esophageal length receving \n  $\geq$ 30 Gy (cm)', fontsize = 20)
    plt.suptitle('45 Gy / 30 fractions', fontsize = 22)
    plt.ylim((-1, 19))
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)
    plt.legend(loc=2,title = 'Esophagitis CTCAE', fontsize = 14, title_fontsize = 14)
    plt.show()   

    

Plot(armB, data_length, data_circ, 41, 'o')
         

