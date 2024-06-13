"""
Program to create BoxPlots of the DSM parameters. 
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns; sns.set_theme()
import pandas as pd
from Parameters import grad_01, grad_2, grad_3, armA, armB, All_patients
from HelperFunctions import collectCSVData_Nr3

def SeveralBoxPlots(data):
    total = []

    group_01, group_2, group_3 = [], [], []

    for row in data:
        length1 = []
        pat_id = row[0]
        if pat_id in armB:
            for i, elem in enumerate(row[1:-1]):
                
                length = []
                length.append(pat_id)
                length.append(elem)
                    
                length.append(10+(i*10))
                    
                if pat_id in grad_01:
                    length.append("0-1")
                    group_01.append(elem)
                    
                elif pat_id in grad_2:
                    length.append("2") 
                    group_2.append(elem)
                    
                elif pat_id in grad_3:
                    group_3.append(elem)
                    length.append("3")
                    
                total.append(length)
            length = []
            length.append(pat_id)
            length.append(row[-1])
                    
            length.append(55)
            if pat_id in grad_01:
                length.append("0-1")
            elif pat_id in grad_2:
                length.append("2") 
            elif pat_id in grad_3:
                length.append("3")
                    
            total.append(length)
        elif pat_id in armA:
            for i, elem in enumerate(row[1:-1]):
                    
                length = []
                length.append(pat_id)
                length.append(elem)
                        
                length.append(10+(i*10))
                        
                if pat_id in grad_01:
                    length.append("0-1 ")
                    
                elif pat_id in grad_2:
                    length.append("2 ") 
                    
                elif pat_id in grad_3:
                    length.append("3 ")
                        
                total.append(length)
            length = []
            length.append(pat_id)
            length.append(row[-1])
                    
            length.append(55)
            if pat_id in grad_01:
                length.append("0-1 ")
            elif pat_id in grad_2:
                length.append("2 ") 
            elif pat_id in grad_3:
                length.append("3 ")
                    
            total.append(length)

    
    df = pd.DataFrame(total, columns= ['Pat_id', 'ValueParam', 'Dose EQD2 (Gy)', 'Esophagitis'])
    
    df.to_excel("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/OutputSheet.xlsx",
             sheet_name='Sheet_name_1') 
    hatches = (['']*6 + ['/////']*6)*6
    colors = ['cornflowerblue' , 'cornflowerblue' ,"darkorange", "darkorange", '#6CE159', '#6CE159']
    hue_order = ['3 ', '3' , '2 ', '2', '0-1 ' , '0-1']
    sns.set_palette(colors)
    sns.set_style("darkgrid")
    flierprops = dict(marker='d', markersize=5, markerfacecolor='black')
    boxprops = dict(linewidth=1.5, alpha = 0.7)
    medianprops = dict(linewidth=1.5, color='black')

    ax = sns.boxplot(x='Dose EQD2 (Gy)', y='ValueParam', hue="Esophagitis", data=df, hue_order = hue_order, showmeans = True, gap = 0.2, meanprops={"marker":"o",
                       "markerfacecolor":"white", 
                       "markeredgecolor":"black",
                      "markersize":"4"},  medianprops = medianprops, linewidth=1.5, fill = True, fliersize = 5, flierprops = flierprops, boxprops = boxprops)

    # select the correct patches
    patches = [patch for patch in ax.patches if type(patch) == mpl.patches.PathPatch]
    # the number of patches should be evenly divisible by the number of hatches
    h = hatches * (len(patches) // len(hatches))
    print(h)
    i = 0
    # iterate through the patches for each subplot
    for patch, hatch in zip(patches, hatches):
        if hatch == '/////':
            patch.set_hatch(hatch)
            fc = patch.get_facecolor()
            patch.set_edgecolor('black')
            #patch.set_facecolor('none')
            #patch.set_edgecolor(fc)
            #patch.set_facecolor('none')

    l = ax.legend(ncol=3, title = 'Esophagitis CTCAE')
    hat = ['', '/////']*3
    for lp, hatch in zip(l.get_patches(), hat):
        if hatch == '/////':
            lp.set_hatch(hatch)
            fc = lp.get_facecolor()
            lp.set_edgecolor('black')
            #lp.set_facecolor('none')

    ax.text(2.8, 34.5, '45 Gy / 30 fractions', fontsize = 14)
    ax.text(2.8, 32.5, '60 Gy / 40 fractions', fontsize = 14)
    plt.grid()
    ax.set_xlabel("Dose $EQD_2$",fontsize=18)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    
    #plt.xticks([20, 25, 30, 35, 40, 45])
    #plt.ylabel("Relative surface area (%)", fontsize = 18)
    plt.ylabel("Relative surface area (%) multiplied with \n the mean dose within that area (Gy)", fontsize = 18)
    #plt.title("Esophageal length of full coverage")
    plt.show()
    

data = collectCSVData_Nr3("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/DSMParameters/areaXdose.csv")
