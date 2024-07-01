""" 
============== 
Loading ROI data from an RT Structure Dicom file and finding the DICOM coordinates of points on the
esophageal surface where dose is to be sampled. These points will be saved and then the dose in these
points will be found in file 'InterpolateDoseInPoints.py'
==============
""" 

###############################################################################

import numpy as np
import os
from shapely.geometry import LineString, Point
import pyvista as pv
import math
from HelperFunctions import collectCSVData, get_pointcloud
from Parameters import All_patients, grad_01, grad_2, grad_3, armA, armB

for pat_number in All_patients:
    
    # Collect RS-file, dose matrix with dimensions and positions for each patient. 

    dir_path = "D:/Data/RS-DICOMfiles/"  + str(pat_number) 
    
    for root, dirs, files in os.walk(dir_path):
        for file in files: 
    
            if file.endswith('.dcm'):
                print (root+'/'+str(file))


    Filename1 = root+'/'+str(file)
    data_dim_sliceThickness = collectCSVData("D:/Data/DimAndPositions/Dim_Patnumber" + str(pat_number) +".csv")
    dim = [int(x) for x in data_dim_sliceThickness[0:3]]
    voxelsizes = data_dim_sliceThickness[3:6]
    voxelpositions = data_dim_sliceThickness[6:]

    # Reading the contour points of the esophagus. 
    
    pointdata, centroiddata = get_pointcloud('Esophagus',Filename1)

    # Finding the z coordinate of the esophageal slices
    
    slice_pos = centroiddata[:, 2]

    num_slice = 0
    
    slice_intersections = np.empty((100*(len(slice_pos)), 3)) # Where the intersection points is going to be stored

    # A loop for every slice of the esophageal contour
    
    s = 0 # index of the intersection points. When a intersection point is found: s+= 1
    
    for elem in slice_pos: 

        # Finding the contour points of the slice
        
        ind_of_points_in_slice = np.where(pointdata[:, 2] == elem)[0]
        num_slice += 1

        # Creating a connected spline of the contour points

        points_per_slice = np.empty((len(ind_of_points_in_slice), 3)) 

        points_per_slice[0:len(ind_of_points_in_slice)-1] = pointdata[ind_of_points_in_slice[0]:ind_of_points_in_slice[-1], :] 

        points_per_slice[-1] = pointdata[ind_of_points_in_slice[0]]
        
        spline = pv.Spline(points_per_slice, n_points = 100) #1000

        # Calculating the centroid of the spline

        centroid = [sum(spline.points[:, 0])/len(spline.points[:, 0]), sum(spline.points[:,1])/len(spline.points[:, 1])] 

        # Locating the left-most point in the connected spline
        
        min_dist = 1
        pointX_upperright = []; pointY_upperright = []
        for i, (point_x, point_y) in enumerate(zip(spline.points[:,0], spline.points[:,1])):
            if point_y >= centroid[1] and point_x >= centroid[0]:
                pointX_upperright.append(point_x)
                pointY_upperright.append(point_y)
                ind = i

        for point_x, point_y in zip(pointX_upperright, pointY_upperright):
            if abs(point_y-centroid[1]) < min_dist:
                min_dist = abs(point_y-centroid[1])
                min_dist_x = point_x
                min_dist_y = point_y 
        
        correct_inds_x = np.where(spline.points[:, 0] == min_dist_x)[0]
        correct_inds_y = np.where(spline.points[:, 1] == min_dist_y)[0]

        correct_inds = [elem for elem in correct_inds_x if elem in correct_inds_y]
        correct_ind = correct_inds[0]

        A = (centroid[0], centroid[1])
        B = (min_dist_x, min_dist_y)
        B1 = (centroid[0]*20, centroid[1])

        if correct_ind != 99: #999
            C = (spline.points[correct_ind+1,0], spline.points[correct_ind+1, 1])
        else:
            C = (spline.points[0,0], spline.points[0, 1])

        line1 = LineString([A, B]) # evt A til (centroid[0]*10, centroid[1]) har ikke noe å si
        line2 = LineString([B, C])

        int_pt = line1.intersection(line2)
        point_of_intersection = int_pt.x, int_pt.y 

        # Equiangular rays emerging from the centroid of the spline

        sample_points = np.linspace(0,360, 100)
        
        for i in sample_points:
            y3 = np.sin(math.radians(i))*(point_of_intersection[0]-centroid[0]) + centroid[1]
            x3 = np.cos(math.radians(i))*(point_of_intersection[0]-centroid[0]) + centroid[0]

            if i == 90:
                E = (centroid[0], centroid[1] + 10)
            elif i == 270:
                E = (centroid[0], centroid[1] - 10)
            else:
                
                a = (y3-centroid[1])/(x3-centroid[0])
                b = -centroid[0]*((y3-centroid[1])/(x3-centroid[0])) + centroid[1]
        
                if (x3 > centroid[0]):
                    E = (x3 + 10 , a*(x3+10)+b)
                else: 
                    E = (x3 - 10 , a*(x3-10)+b)

            # Creating line between the centroid of the slice and E 
            
            line3 = LineString([A, E])

            # Trying to find an intersection points between the spline points and line 3. 
            # When the intersection point is found: the x, y and z coordinates of the intersection point is stored in slice_intersections. 
            for j in range(len(spline.points[:,0])-1):
                if j < (len(spline.points[:,0])-1):
                    point_a = (spline.points[:,0][j], spline.points[:,1][j])
                    point_b = (spline.points[:,0][j+1], spline.points[:,1][j+1])
                else:
                    point_a = (spline.points[:,0][j], spline.points[:,1][j])
                    point_b = (spline.points[:,0][0], spline.points[:,1][0])

                line = LineString([point_a, point_b])
            
                try:
                    int_pt_1 = line.intersection(line3)
                    point_of_intersection_1 = int_pt_1.x, int_pt_1.y

                    slice_intersections[s] = [point_of_intersection_1[0], point_of_intersection_1[1], elem]
                    s+=1

                    break
                except:
                    continue
                    
    # Saving the coordinates of the all the intersection points. 

    slice_intersections = np.array(slice_intersections.flatten())
    

    # slice_intersections.tofile("C:/Users/hmibe/OneDrive/Dokumenter/Masteroppgave/Data/SamplePoints/pat" + str(pat_number), sep = "\r\n")

