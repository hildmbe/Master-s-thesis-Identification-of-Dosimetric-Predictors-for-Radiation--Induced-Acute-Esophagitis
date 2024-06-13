from connect import *
import os
import numpy as np
#import matplotlib.pyplot as plt

import csv


outputdir = 'H:/Masteroppgave/Data_ny'

###############################################################################################
''' Denne filen brukes til å eksportere dosematriser med tilhørende dimensjoner og DICOM-posisjoner. '''

patient_db = get_current('PatientDB')

pat_numbers = []

trplan = ''


for i, pat in enumerate(pat_numbers):
    pat_info = patient_db.QueryPatientInfo(Filter={'PatientID': '^' + str(pat) +'$'})

    patient = patient_db.LoadPatient(PatientInfo=pat_info[0])

    plan = patient.Cases[0].TreatmentPlans[trplan]

    case = patient.Cases[0]
    case.SetCurrent()

    plan.SetCurrent()

    #examination = patient.Cases[0].Examinations['CT 1']

    dose = plan.TreatmentCourse.TotalDose; dose_matrix = dose.DoseValues.DoseData; dose_matrix_1d = dose_matrix.flatten()

    corner_dg = plan.TreatmentCourse.TotalDose.InDoseGrid.Corner

    voxel_size = plan.TreatmentCourse.TotalDose.InDoseGrid.VoxelSize

    dim = dose_matrix.shape

    dose_matrix_1d.tofile(outputdir + '/DoseMatrices/DoseMatrix_Patnumber' + str(pat) + '.txt', sep = "\r\n")

    with open(outputdir+'/'+'DimAndPositions/Dim_Patnumber' + str(pat) + '.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['dz, dy, dx, vs_z, vs_y, vs_x, vp_z, vp_y, vp_x'])

        csvwriter.writerow([dim[0], dim[1], dim[2], voxel_size['z'], voxel_size['y'], voxel_size['x'], corner_dg['z'], corner_dg['y'], corner_dg['x']])
