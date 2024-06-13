''' Brukes til å lage konfidensintervaller og plotting. '''

import numpy as np
import matplotlib.pyplot as plt
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
from HelperFunctions import collectCSVData, collectCSVData_Nr2 
import seaborn as sns
from mne.stats import bootstrap_confidence_interval 


data = collectCSVData_Nr2("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParameters/Length_full_coverage.csv")

'''data = collectCSVData_Nr2("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParametersArmB30frac/areaXdose.csv")

for row in data1:
    if row[0] in armA:
        data.append(row)'''

current3 = [elem for elem in grad_3 if elem in All_patients]
Tot_3 = []
counter_3 = 0
for row in data:
    pat_id = row[0]
    if pat_id in current3:
        #row = np.array(row)
        Tot_3.append(row[1:])
        if row[41] >= 5:
            counter_3+=1

Tot_arr3 = np.array(Tot_3)
ci_low_3, ci_up_3 = bootstrap_confidence_interval(Tot_arr3, random_state=0, stat_fun='mean', n_bootstraps = 10000, ci=0.95)

print(counter_3)
current2 = [elem for elem in grad_2 if elem in All_patients]
Tot_2 = []; 
counter_2 = 0
for row in data:
    pat_id = row[0]
    if pat_id in current2:
        #row = np.array(row)
        Tot_2.append(row[1:])
        if row[41] >= 5:
            counter_2 +=1
Tot_arr2 = np.array(Tot_2)
print(counter_2)

ci_low_2, ci_up_2 = bootstrap_confidence_interval(Tot_arr2, random_state=0, stat_fun='mean', n_bootstraps = 10000, ci=0.95)

current01 = [elem for elem in grad_01 if elem in All_patients]
Tot_01 = []
counter_01 = 0
for row in data:
    pat_id = row[0]
    if pat_id in current01:
        #row = np.array(row)
        Tot_01.append(row[1:])
        if row[41] >= 5:
            counter_01+=1
Tot_arr01 = np.array(Tot_01)
print(counter_01)
ci_low_01, ci_up_01 = bootstrap_confidence_interval(Tot_arr01, random_state=0, stat_fun='mean', n_bootstraps = 10000, ci=0.95)


x = np.arange(0, 60, 1)

mean3 = np.mean(Tot_3, axis = 0); mean2 = np.mean(Tot_2, axis = 0); #mean01 = np.mean(Tot_01, axis = 0)

 
sns.set_style("darkgrid")
fig = plt.figure()
with sns.axes_style("darkgrid"):
    ax1 = fig.add_subplot()
#ax2 = fig.add_subplot(122)

ax1.plot(x, mean3, label = '3 (n=15)')
#plt.fill_between(x, mean3-stdev3, mean3+stdev3, alpha = 0.3)
ax1.fill_between(x, ci_low_3, ci_up_3, alpha = 0.3)


ax1.plot(x, np.mean(Tot_2, axis = 0), label = '2 (n=22)')
ax1.fill_between(x, ci_low_2, ci_up_2, alpha = 0.3)


ax1.plot(x, np.mean(Tot_arr01, axis = 0), label = '0-1 (n=45)')
ax1.fill_between(x, ci_low_01, ci_up_01, alpha = 0.3)

ax1.legend(loc = 3, title = 'Esophagitis CTCAE', fontsize = 20, title_fontsize = 20)

ax1.set_xlabel('Dose $EQD_2$ (Gy)', fontsize = 20)
#ax1.set_ylabel('Length irradiated to full circumferential \n coverage (cm)', fontsize = 20)
#ax1.set_ylabel('Relative surface area (%)', fontsize = 20)
#ax1.set_ylabel("Relative surface area (%) multiplied with \n the mean dose within that area (Gy)", fontsize = 20)
ax1.set_ylabel('Max circumference irradiated (%)', fontsize = 20)
ax1.tick_params(axis='x', labelsize=18)
ax1.tick_params(axis='y', labelsize=18)
 
#ax1.set_xlim((0, 60))
#ax1.set_ylim((-2, 28))
plt.suptitle('60 Gy / 40 fractions', fontsize = 22)
plt.show()
