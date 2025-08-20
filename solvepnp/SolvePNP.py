import sys
import os
home_path = os.path.expanduser('~')
project_path = os.path.join(home_path, 'robotDetectPick', 'yolov5')
sys.path.append(project_path)
project_path = os.path.join(home_path, 'robotDetectPick', 'robot')
sys.path.append(project_path)
import numpy as np
import cv2 as cv
import detect as dt
import time
from datetime import datetime


# Calculating speed of two frames
def calculating_speed(y1, y2, time_difference):
    # Berechne die Geschwindigkeit Zentimeter pro Sekunde
    if (y2 > y1) and (y2 != 0.0) :
        distance = y2 - y1
        speed = distance / time_difference
        return speed, distance, time_difference
    elif (y1 > y2):
        distance = y1 - y2
        speed = distance / time_difference
        return speed, distance, time_difference
                                


def solvepnpfp():
                    
    # Load camera calibration intrinsic and extrinsic parameters
    with np.load(home_path + 'robotDetectPick/solvepnp/results/CameraParams.npz') as file:
        mtx, dist, rvecs, tvecs = [file[i] for i in ('cameraMatrix','dist','rvecs','tvecs')]
    # Define lists
    global allObjects3D
    global allObjects3Dcenter
    global world_coordinate_system
    points4Coordinates = []
    global allPoints3D
    allPoints3D = []
    global allObjects3D
    allObjects3D = []
    allObjects3Dcenter = []
    speedList = []
    distanceList = []
    timeList = []
    world_coordinate_system = []
    coordinates3D = [0]*4 
    object_point_in_world_all = [0]*4

    # Define Variable's
    global oy1
    global ox1
    global averageSpeed
    global yBoundary
    global averageTime
    global averageDistance
    averageDistance = 0.0
    averageTime = 0.0
    yBoundary = 29.0
    averageSpeed = 0.0
    oy1 = 0.0 
    ox1 = 0.0
    frameFLag = False
    y1 = 0.0
    y2 = 0.0
    t = 0.0
    firstRunFlag = True
    sleepFlag = False
    firstSleepFlag = False
    y_center_pixel = 0.0
    speedCounter = 0
    start_time = 0.0
    firstStart_time = 0.0
    firstEnd_time = 0.0
    a = 0.0
    b = 0.0
    sleepCounter = 0
    # Defining the dimensions of the world coordinate system
    x = 14.6   # in CentiMeter
    y =  30    # in CentiMeter
    z = 0.8    # in CentiMeter   
    # Webcam Resolution
    image_width = 640
    image_height = 480
    
    # represents a 3d world coordinate system, contains four 3d points
    world_coordinate_system = np.array([[0, 0, 0], 
                                        [x, 0, 0], 
                                        [x, y, 0], 
                                        [0, y, 0]], 
                                       dtype=np.float32)
                                    
    time.sleep(5)
    points4Coordinates = dt.pointArrayCenter
    # 2D coordinates of the 4 points (landmarks) of the WCS in the image
    # Top Left Point
    u = points4Coordinates[2]          # [0]
    v = points4Coordinates[3]         # [1]
    # Bottom Left Point
    u2 = points4Coordinates[0]         # [2]
    v2 = points4Coordinates[1]        # [3]
    # Top Right Point
    u3 = points4Coordinates[6]        # [4]           
    v3 = points4Coordinates[7]        # [5]
    # Bottom Right Point
    u4 = points4Coordinates[4]        # [6]
    v4 = points4Coordinates[5]        # [7]

    # These variables hold the coordinates of the four corners of a bounding box that 
    # surrounds the detected object. Each corner is represented by a pair of 2D points
    x_oben_links_pixel = dt.allCoordinatesPerDetectionPixelArray[0]
    y_oben_links_pixel = dt.allCoordinatesPerDetectionPixelArray[1]
    x_unten_links_pixel = dt.allCoordinatesPerDetectionPixelArray[2]
    y_unten_links_pixel = dt.allCoordinatesPerDetectionPixelArray[3]
    x_unten_rechts_pixel = dt.allCoordinatesPerDetectionPixelArray[4]
    y_unten_rechts_pixel = dt.allCoordinatesPerDetectionPixelArray[5]
    x_oben_rechts_pixel = dt.allCoordinatesPerDetectionPixelArray[6]
    y_oben_rechts_pixel = dt.allCoordinatesPerDetectionPixelArray[7]

    # contains four 2d points of the landmarks in pixel coordinates 
    image_point_pixel = np.array([[u, v], 
                            [u2, v2], 
                            [u3, v3], 
                            [u4, v4]], 
                           dtype=np.float32)
    # contains four 2d points of detected objects (all corners of bounding-box) in pixel coordinates 
    object_pixel = np.array([[x_oben_links_pixel, y_oben_links_pixel], 
                            [x_unten_links_pixel, y_unten_links_pixel], 
                            [x_unten_rechts_pixel, y_unten_rechts_pixel], 
                            [x_oben_rechts_pixel, y_oben_rechts_pixel]], 
                           dtype=np.float32)

    # get the rotation and translation vector of own defined world coordinate system
    ret, rvecs, tvecs = cv.solvePnP(world_coordinate_system, image_point_pixel, mtx, dist)
    extrinsicMatrix = np.zeros((3, 4))
    # Extract distortion coefficients
    k1, k2, p1, p2, k3 = dist[0]
    # Extract intrinsic parameters
    fx = mtx[0, 0]
    fy = mtx[1, 1]
    cx = mtx[0, 2]
    cy = mtx[1, 2]
    # Define the intrinsic parameters
    # defines a 3x3 camera intrinsic matrix 
    K = np.array([[fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]])
    # Camera matrix with focal length only (fx, fy)
    KonlyF = np.array([[fx, 0, 0, 0],
                [0, fy, 0, 0],
                [0, 0, 1, 0]])
    # Convert the array to the desired format
    new_rvecs = np.array([rvecs])
    new_tvecs = np.array([tvecs])
    # Transformation into the world coordinate space
    rvec = new_rvecs[counter]
    tvec = new_tvecs[counter]

    # takes the rotation vector rvec as input and returns the corresponding rotation matrix R
    R, _ = cv.Rodrigues(rvec)
    # inverse rotation vector
    rvec_inv = -rvec
    R_inv, _ = cv.Rodrigues(rvec_inv)
    # inverse translation vector
    t_inv = -tvec
    # Transformation from camera to world coordinates, inverse rotation and translation are combined.
    # This transformation matrix T transforms points from camera coordinates to world coordinates. 
    T_camera_to_world = np.hstack((R_inv, t_inv))
    T_camera_to_world = np.vstack((T_camera_to_world, [0, 0, 0, 1]))
    transformationMatrix = np.hstack((R, tvec))
    # represents the extrinsic matrix, which combines the rotation and translation 
    extrinsicMatrix[:3, :3] = R
    extrinsicMatrix[:, 3] = tvec[:, 0]
    # Make extrinisic Matrix 4x4
    extrinsicMatrix_4x4 = np.vstack((extrinsicMatrix, [0, 0, 0, 1]))
    # multiplying the camera intrinsic matrix K with a horizontally stacked matrix 
    # consisting of the rotation matrix R and the translation vector
    # tvec --> projectionsmatrix 3x4
    P = K @ np.hstack((R, tvec))
    # Create the homography matrix 3x3 from the projection matrix 4x4
    p11, p12, p13, p14 = P[0]
    p21, p22, p23, p24 = P[1]
    p31, p32, p33, p34 = P[2]
    homographyMatrix = np.array([[p11, p12, p14], [p21, p22, p24], [p31, p32, p34]])
    # inverse Homography Matrix 3x3
    inverseHomographyMatrix = np.linalg.inv(homographyMatrix)

    # with allPoints3d you can check if your solvepnp function worked properly, when the points are similar to your defined world coordinates, then the test is sucessful
    def test_world_coordinates():
        counter = 0
        for i in range (4):
            # load 2d pixel coordinates 
            point2D = np.array([image_point_pixel[counter][0], image_point_pixel[counter][1], 1]).reshape(3, 1)
            # Estimating the world coordinates of the points (landmarks with given pixel coordinates of the landmarks
            
            if allPoints3D == []:
                point3Dw = inverseHomographyMatrix.dot(point2D)
                w = point3Dw[2, 0]
                matPoint3D = np.divide(point3Dw, w)
                # save world coordinates in list
                allPoints3D.append(matPoint3D)

    def estimate_world_coordinates_of_object_with_bb():
        counter = 0
        for i in range (4): 
            # Estimating the world coordinates of the detected object with given pixel coordinates of every corner of bounding-box
            if allObjects3D == []: 
                object2d = np.array([object_pixel[counter][0], object_pixel[counter][1], 1]).reshape(3, 1)
                object3Dw = inverseHomographyMatrix.dot(object2d)
                w = object3Dw[2, 0]
                matObject3D = np.divide(object3Dw, w)
                allObjects3D.append(matObject3D)
            counter += 1
        allPoints3D = np.hstack(allPoints3D)    
        allObjects3D = np.hstack(allObjects3D)
        allPoints3D = allPoints3D.T
        allObjects3D = allObjects3D.T

    waiting_period_in_seconds = 0.0001
    # estimate world coordinates and speed of detected object with given pixel coordinates of center
    while True:
        # Time.Sleep um die Ressourcen der CPU nicht unnötig zu verbrauchen
        time.sleep(waiting_period_in_seconds)
        if firstSleepFlag == True:
                sleepCounter += 1
        
        # extract pixel coordinates of detected object and transform pixel coordinates to world coordinates
        if y_center_pixel != dt.allCoordinatesPerDetectionPixelArrayCenter[1]:
            firstRunFlag = False
            x_center_pixel = dt.allCoordinatesPerDetectionPixelArrayCenter[0]
            y_center_pixel = dt.allCoordinatesPerDetectionPixelArrayCenter[1]
            allObjects3Dcenter = []
            object_pixel_center = np.array([[x_center_pixel, y_center_pixel]], 
                                dtype=np.float32)
            # Estimating the world coordinates of the detected object center  
            object2dcenter = np.array([object_pixel_center[0][0], object_pixel_center[0][1], 1]).reshape(3, 1)
            object3Dwcenter = inverseHomographyMatrix.dot(object2dcenter)
            w = object3Dwcenter[2, 0]
            matObject3Dcenter = np.divide(object3Dwcenter, w)
            allObjects3Dcenter.append(matObject3Dcenter)
            allObjects3Dcenter = np.hstack(allObjects3Dcenter)
            allObjects3Dcenter = allObjects3Dcenter.T[:1]

            # set two distances
            if speedCounter == 0 or speedCounter == 2:
                y1 = allObjects3Dcenter [0][1]
                a = datetime.now()
                if speedCounter == 2:
                    speedCounter = 0
            if speedCounter == 1:
                y2 = allObjects3Dcenter [0][1]
                b = datetime.now()
            speedCounter += 1

            # calculate time difference of two given world coordinates
            if y1 > 0.0 and y2 > 0.0:
                if (a > b):
                    seconds = a - b
                if (b > a):
                    seconds = b - a
                seconds = seconds.total_seconds() - (waiting_period_in_seconds *  (sleepCounter))
                # Check if the time difference can have errors in the calculation.
                if seconds < 0 or waiting_period_in_seconds == 0:
                    print("second number is negative")
                if waiting_period_in_seconds == 0:
                    print("number is zero")

                # calculate speed with given two world coordinates
                speedDistanceTime = calculating_speed(y1 , y2, seconds)
                 
                # store all calculated distances, speed and time difference in a list to estimate the mean value
                speedList.append(speedDistanceTime[0])
                distanceList.append(speedDistanceTime[1])
                timeList.append(speedDistanceTime[2])
                # Calculate the mean values so far
                summe = sum(speedList), sum(distanceList), sum(timeList)
                anzahl = len(speedList), len(distanceList), len(timeList)
                averageSpeed = summe[0] / anzahl[0]
                averageSpeed = round(averageSpeed, 4)
                averageDistance = summe[1] / anzahl[1]
                averageTime = summe[2] / anzahl[2]
                averageAllVariables = averageSpeed, averageDistance, averageTime
                sleepCounter = 0
            
            # world coordinates of detected object cant be bigger than y boundary
            if y1 > (y+5) or y2 > (y+5):
                y1 = 0.0
                y2 = 0.0
            # after the detected object is picked, reset all variables for next object to detct
            if y1 >= yBoundary or y2 >= yBoundary:
                if y1 > y2:
                    oy1 = y1 
                    ox1 = allObjects3Dcenter [0][0]
                    y1 = 0.0
                    y2 = 0.0
                    speedList = []
                    distanceList = []
                    timeList = []
                if y1 < y2:
                    oy1 = y2 
                    ox1 = allObjects3Dcenter [0][0]
                    y1 = 0.0
                    y2 = 0.0
                    speedList = []
                    distanceList = []
                    timeList = []
            firstSleepFlag = True

if __name__ == '__main__':
    solvepnpfp()

