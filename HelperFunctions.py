"""
Helper functions 
"""

import csv
import numpy as np
import pydicom
import math
from skimage.measure import label
from skimage.measure import moments

# Functions to read CSV data. 

def collectCSVData_Nr3(filename):
    rows = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in (csvreader):
            row_ny = [row[0]] + [row[11]] + [row[21]] + [row[31]] + [row[41]] + [row[51]] + [row[56]]
            print(row_ny)
            y = [float(j) for j in row_ny]
            rows.append(y)
            
    return rows

def collectCSVData(filename):
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
        
            y = [float(j) for j in row]
                
    return y

def collectCSVData_Nr2(filename):
    rows = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
        
            y = [float(j) for j in row]
            rows.append(y)
    return rows

# Functions for rotating DSM vertically and horizontally. 

def rotateVertically(l, n):
    rot = np.zeros((len(l), len(l[0])))
    for i in range(len(l[n:])):
        rot[i] = l[n:][i]
        
    for j in range(len(l[:n])):
        rot[j + len(l[n:])] = l[:n][j]
    
    return rot

def rotateHorizontally(l, n):
    rot = []
    for elem in l:
        rot.append(elem.tolist()[n:] + elem.tolist()[:n])
    return np.array(rot)

####################################################################

def getVolumeforDVHs(Dose_matrix_1d, Vol_matrix_1d):
    doses = np.arange(0, 60, 1)
    volumes = np.zeros(60)

    for i, thr in enumerate(doses):
        for dose, vol in zip(Dose_matrix_1d, Vol_matrix_1d):
            if dose >= thr:
                volumes[i] += vol
    return volumes, doses

def ConvertDoseMatrixToEQD2(Dose_matrix_1d, num_frac, ab):
    doseMatrixEQD2 = np.zeros(len(Dose_matrix_1d))
    for i, dose in enumerate(Dose_matrix_1d):
        doseMatrixEQD2[i] = (dose/100)*(ab + (dose/(100*num_frac)))/(ab+2)
    
    return doseMatrixEQD2

def convertDSMtoEQD2(DSM, num_frac, ab):
    
    DSM_EQD2 = np.zeros(len(DSM.flatten()))
    for i, dose in enumerate(DSM.flatten()):
        DSM_EQD2[i] = (dose)*(ab + (dose/(num_frac)))/(ab+2)
    
    return DSM_EQD2.reshape(DSM.shape[0], DSM.shape[1])

####################################################################

# Function to collect DSM parameters such as circumferential extent, length, surface area etc.. 

def DSM_features(DoseMask, slice_thickness):

    row_inds_with_dose = np.where(DoseMask == 1)[0]

    area = len(row_inds_with_dose)/len(DoseMask.flatten())*100

    num_slices_full_coverage = 0; num_slices_with_dose = 0
    
    row_inds_with_dose_set = set(row_inds_with_dose)
    
    grade_of_circ = []

    for elem in row_inds_with_dose_set:
        grade_of_circ.append(row_inds_with_dose.tolist().count(elem))

        if row_inds_with_dose.tolist().count(elem) >= 80:
            num_slices_full_coverage += 1

        if row_inds_with_dose.tolist().count(elem) >= 1:
            num_slices_with_dose += 1
    
    grade_of_circ_arr = np.array(grade_of_circ)
    
    mean_grade_of_circ = np.mean(grade_of_circ_arr)

    n = math.ceil(1/slice_thickness)

    grade_of_circ_1cm_consecutive = []

    for i in range(len(grade_of_circ_arr)-n):
        cm1_consecutive = grade_of_circ_arr[i:(n+i)]
        grade_of_circ_1cm_consecutive.append(np.min(cm1_consecutive))

    length_full_coverage = num_slices_full_coverage*slice_thickness

    length = num_slices_with_dose*slice_thickness

    grade_of_circ_arr.sort()

    max_grade_of_circ_1cm = grade_of_circ_arr[-n] #ikke sammenhengende

    Features = {'area': area, 'length_full_coverage': length_full_coverage, 'mean_grade_of_circ':mean_grade_of_circ, 'grade_of_circ_max': max_grade_of_circ_1cm, 'length': length, 'grade_of_circ_max_concecutive': np.max(grade_of_circ_1cm_consecutive)}
    return Features

#####################################################################

# Functions from Patrick HM, Kildea J. Technical note: rtdsm-An open-source software for radiotherapy
# dose-surface map generation and analysis. Med Phys. 2022 Nov;49(11):7327-7335. doi: 10.1002/mp.15900. 
# Epub 2022 Aug 8. PMID: 35912447.

def PolygonArea(x,y):
    """
    Uses Gauss's shoelace algorithm to estimate the area of a polygon.

    Parameters
    ----------
    x, y : list or numpy.ndarray
        X and Y coordinates of points comprising the polygon

    Returns
    ----------
    area : float
        Area of the polygon.
    """
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def get_pointcloud(ROI_Name, RS_filepath, excludeMultiPolygons=True):
    """
    Creates a formatted array of an ROI's vertex data in addition to an array of
    slice centroids using a Dicom RTStruct file as input.

    Parameters
    ----------
    ROI_Name : str
        The name of the ROI (region of interest) to retrive contour data for.
    RS_filepath : str
        The path to the RS-DICOM file.
    excludeMultiPolygons : bool, optional
        Flag to indicate if multiple closed polygonal regions on the same slice
        of the reference image are kept or not (primarily used to exclude points
        that define holes in the center of the main contour polygon). Defaults
        to True. If True, only the points comprising the largest contour on a
        slice are added to the output array.

    Returns
    -------
    contour : numpy.ndarray
        Array of the ROI's vertex data, formatted into a list of coordinate 
        points (M x 3).
    CoMList : numpy.ndarray
        Array of the centroid coordinates for each slice of the ROI (M x 3).

    Notes
    -------
    Because of how the function get_cubemarch_surface() handles pointcloud data,
    the user must explictly specify how to handle multiple closed polygons on the
    same axial slice of the image used for contouring. Failure to do this will 
    result in them being combined into one continous polygon. By default, only
    the largest polygons are kept per slice. If inclusion of multiple polygons
    is specified to be allowed by the user, a coordinate of np.nan values will
    be added to the output arrays to differentiate the additional polygons from
    the rest of the structure.
    """
    #Function updated April 2023 by HP to better account for the following situations:
        #- Cases where the contours are not drawn on axial image slices
        #- Cases where DICOM pointcloud data is not provided in ascending Z order
        #   (as has been observed for contours provided by MIMvista)
    #STEP 1: get the raw mesh data
    mesh = contourdata_from_dicom(ROI_Name, RS_filepath)
    #STEP2: prep output data arrays
    xdata, ydata, zdata = [], [], []
    Ztracking = [[],[],[]]     #used to check for duplicate Z (axial) indices
    CoMList = []
    extrax, extray, extraz = [], [], [] #holds point data for extra polygons per slice
    extraCOM = []
    nonAxialSlices = False  #flag to indicate if structure slices are not aligned with image slices
    #STEP3: begin adding data
    for plane in mesh:
        #get points for point cloud
        xvals = (plane[0::3])
        yvals = (plane[1::3])
        zvals = (plane[2::3])
        #STEP3A: Check if structure slices are aligned with axial imaging plane
            #If not aligned, rtdsm will report how unaligned the slices are and
            #will align the slice at its average Z location
        if len(list(set(zvals))) > 1 and nonAxialSlices==False:
            print('WARNING: Slice is angled away from axial image plane')
            zmax = min(zvals)
            zmin = max(zvals)
            indmin = zvals.index(zmin)
            indmax = zvals.index(zmax)
            p1,p2 = np.array([xvals[indmin],yvals[indmin],zmin]),np.array([xvals[indmax],yvals[indmax],zmax])
            h = np.linalg.norm(p1-p2)
            o = zmax - zmin
            angle = math.degrees(math.asin(o/h))
            print('angle:',angle,'degrees')
            nonAxialSlices = True
        if nonAxialSlices == True:
            #use the average Z position instead of the actual Z values
            zval = round(sum(zvals)/len(zvals),2)
            zvals = [zval] * len(zvals)
        else:
            zval = plane[2]
        #STEP3B: Get the slice's polygon and calculate its area and CoM
        points = np.array([plane[0::3],plane[1::3]]).T
        area, COM = PolygonArea(points[:,0],points[:,1]), list(np.append(points.mean(axis=0),[zval]))
        #STEP3C: Check for other slices at the same Z location. If another slice
            #does exist, the largest will be kept and the smaller will be saved
            #to a secondary array that is added at the end of the pointcloud array
            #after a buffer of NaN data
            #NOTE: this is done to accomadate the method used to create the
            #the surface mesh of the contour
        if zval in Ztracking[0] and area > Ztracking[1][Ztracking[0].index(zval)]:
            #The prexisting slice is smaller. Replace with the new one
            extraCOM.append(CoMList[Ztracking[0].index(zval)]) #swap and update the COMs
            CoMList[Ztracking[0].index(zval)] = COM
            Ztracking[1][Ztracking[0].index(zval)] = area #update the area in the tracking
            Ztracking[2][Ztracking[0].index(zval)] += 1
            #move the smaller polygon points to the extra arrays
            oldindex = zdata.index(zvals[0])
            if Ztracking[2][Ztracking[0].index(zval)] > 2:
                extrax.append(np.nan)   #done to seperate two polygons on the same slice
                extray.append(np.nan)
                extraz.append(np.nan)
            extrax.extend(xdata[oldindex:])
            extray.extend(ydata[oldindex:])
            extraz.extend(zdata[oldindex:])
            #replace the old pointcloud ones with new
            xdata, ydata, zdata = xdata[:oldindex], ydata[:oldindex], zdata[:oldindex]
            xdata.extend(xvals)
            ydata.extend(yvals)
            zdata.extend(zvals)
        elif zval in Ztracking[0]:
            #The prexisting slice is larger. Add the new one to the extra array
            Ztracking[2][Ztracking[0].index(zval)] += 1
            extraCOM.append(COM)
            if Ztracking[2][Ztracking[0].index(zval)] > 2:
                extrax.append(np.nan)   #done to seperate two polygons on the same slice
                extray.append(np.nan)
                extraz.append(np.nan)
            extrax.extend(xvals)
            extray.extend(yvals)
            extraz.extend(zvals)
        else:
            #No other polygon exists on the slice, proceed normally
            Ztracking[0].append(zval)
            Ztracking[1].append(area)
            Ztracking[2].append(1)
            CoMList.append(COM)
            xdata.extend(xvals)
            ydata.extend(yvals)
            zdata.extend(zvals)
    #STEP 4: Final cleanup of the data
    #STEP4A: If excludeMultiPolygons FALSE, append extra arrays to the normal ones
    if excludeMultiPolygons == False and len(extraz)>0:
        if zdata[-1] == extraz[0]:
            xdata.append(np.nan)    #add a row of nan data if needed to prevent
            ydata.append(np.nan)    #point data for two polygons on the same slice
            zdata.append(np.nan)    #being confused as a single polygon
        xdata.extend(extrax)
        ydata.extend(extray)
        zdata.extend(extraz)
        CoMList.extend(extraCOM)
    #STEP4B: Ensure CoM data is presented in ascending Z position order
    CoMList = np.asarray(CoMList)
    if (CoMList[0,2] > CoMList[-1,2]):
        CoMList = np.flipud(CoMList)
        extraCOM = np.flipud(extraCOM)
        #the pointcloud data does not need to be switched as get_cubemarch_surface()
        #will do it automatically 
    #STEP5: Return the pointcloud and CoM data
    contour = np.array([xdata,ydata,zdata]).T
    return contour, CoMList


def contourdata_from_dicom(ROI_Name, RS_filepath):
    """
    Extracts the raw contour vertex data of a specified ROI from a RS-DICOM file.

    Parameters
    ----------
    ROI_Name : str
        The name of the ROI (region of interest) to retrive contour data for.
    RS_filepath : str
        The path to the RS-DICOM file.

    Returns
    -------
    contour : numpy.ndarray
        An array of the raw contour vertex data of the ROI. See Notes for 
        details.

    See Also
    --------
    get_pointcloud : Returns formatted contour point data and slice 
    centroids.

    Notes
    ------
    Contour data is returned in the same format it is stored in the Dicom. This 
    is in the form of n 1D arrays, where n is the number of closed polygonal 
    slices that comprise the contour. The points that comprise each slice are
    given in the 1D arrays as a sequence of (x,y,z) triplets in the Patient-
    Based Coordinate System.

    If the ROI name given does not exist in the Dicom file, the function
    returns the list of ROIs in the file and raises an exception.
    """
    #STEP1: Open the Dicom file and check if the requested ROI is present
    rs = pydicom.read_file(RS_filepath)
    ROI_index,ROIlist = None,[]
    for index, item in enumerate(rs.StructureSetROISequence):
        ROIlist.append(item.ROIName)
        if item.ROIName == ROI_Name:
            ROI_index = index
            break
    if ROI_index == None:
        raise Exception('An ROI with the name specified does not exist in the Dicom file. The available structures are:\n',ROIlist)
    #STEP2: Get all contour points from RS file (organized as: [[x0-N, y0-N, z0-N][x0-N, y0-N, z0-N]] )
    contour = []
    for item in rs.ROIContourSequence[ROI_index].ContourSequence:
        contour.append(item.ContourData)
    #return np.array(contour)
    return contour

def clustermask(DSM,value,connectivity=1):
    # Brukt til å hente ut største clusteret for å rotere DSM-ene. 

    #STEP1: mask DSM to only include voxels above the dose vslue
    Mask = (DSM>=value).astype(int)
    #STEP2: find all the connected clusters
    clusters = label(Mask,connectivity=connectivity)
    if clusters.max() != 0:
        largest = (clusters == np.argmax(np.bincount(clusters.flat)[1:])+1).astype(int)
        return largest
    else:
        print("WARNING! No voxels greater than",value,"Gy exist in the DSM. Returning 'None' instead of a cluster mask.")
        return None
        
def getCentroidofMask(DoseMask):
    locs = np.transpose(np.nonzero(DoseMask))
    M = moments(DoseMask)
    centroid = (M[0,1]/M[0,0], M[1,0]/M[0,0]) 
    return centroid
