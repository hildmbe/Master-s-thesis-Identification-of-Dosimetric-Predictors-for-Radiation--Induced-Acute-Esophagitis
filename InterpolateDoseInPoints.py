from connect import *
import numpy as np
import csv

###############################################################################################

outputdir = 'H:/Masteroppgave/'

# Function to interpolate at the given point. Uses built-in functions in RayStation. 
# Returns the interpolated dose in the given point. 
def findDoseAlongContour(point, pointFoR):
    '''points er de aktuelle punktene i hver slice som skal samples. Points har altså en lengde på 100'''
    p = {'x': point[0], 'y': point[1], 'z': point[2]}
    PointDose = plan.TreatmentCourse.TotalDose.InterpolateDoseInPoint(Point = p, PointFrameOfReference = pointFoR)
    return PointDose

# Used to collect the coordinates of the sample points from file. 
def collectdataNy(filename):
    sample_points_total = np.genfromtxt(filename, dtype = float)/10
    
    sample_points_ordered = np.reshape(sample_points_total, (int(len(sample_points_total)/3), 3))
    
    return sample_points_ordered.tolist() 

patients = []

for pat_number in patients:
    
    patient_db = get_current('PatientDB')

    pat_info = patient_db.QueryPatientInfo(Filter={'PatientID': '^' + str(pat_number) +'$'})

    patient = patient_db.LoadPatient(PatientInfo=pat_info[0])

    plan = patient.Cases[0].TreatmentPlans[trplan]
    case = patient.Cases[0]
    case.SetCurrent()

    plan = patient.Cases[0].TreatmentPlans[trplan]
    plan.SetCurrent()

    examination = get_current("Examination")

    beam_set = get_current('BeamSet')

    pointFoR = beam_set.FrameOfReference

    # Collecting the samplepoints from 'Find_samplepoints.py'
    
    matrix_of_points = collectdataNy(outputdir + 'SamplePoints/pat' + str(pat_number))

    # Finding the dose in each of these samplepoints and storing them in DSM_1d
    
    DSM_1d = []
    for point in matrix_of_points:
        
        DSM_1d.append(findDoseAlongContour(point, pointFoR))
        
    DSM_1d = np.array(DSM_1d)

    # Saving the DSMs

    DSM_1d.tofile(outputdir + 'DSMs/DSMpat' + str(pat_number) + '.txt', sep = "\r\n")

