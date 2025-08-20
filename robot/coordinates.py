#  Imports
# Robot Imports
from workspace import *
from converter import *
from color import *
from pickAndPlace import *
from pyniryo import *

# 
import time
from datetime import datetime

import os

# import yolov5 folder and the scripts
home_path = os.path.expanduser('~')
project_path = os.path.join(home_path, 'robotDetectPick', 'yolov5')
sys.path.append(project_path)
import detect as dt

# import yolov5 folder and the scripts
home_path = os.path.expanduser('~')
project_path = os.path.join(home_path, 'robotDetectPick', 'solvepnp')
sys.path.append(project_path)
import SolvePNP as solvepnpfptest



# Define the coordinates of the observation pose 
observation_pose = PoseObject(
    x=0.16, y=0.0, z=0.35,
    roll=0.0, pitch=1.57, yaw=0.0,
)

# Define the coordinates of the observation pose 
observation_pose2 = PoseObject(
    x=0.142, y=-0.141, z=0.266,
    roll=-2.974, pitch=1.379, yaw=2.656,
)

# Place pose
place_pose = PoseObject(
    x=0.0, y=-0.2, z=0.12,
    roll=0.0, pitch=1.57, yaw=-1.57
)

# Define Robot's Position
home = ([25,0,30,0,90,0]) #observation
obs = ([25,0,40,0,90,0]) #observation

# Place green objects in a different position
place_upGreen = ([0,25,25,0,90,90])
place_downGreen = ([0,25,15,0,90,90])

# Place blue objects in a different position
place_upBlue = ([0,-20,20,0,90,-90])
place_downBlue = ([0,-20,12,0,90,-90])


# Initializing variables
offset_size = 0.05
max_catch_count = 4
detectedCounter = 0
catch_count = 0	
timeToPick = 4.15
speedOffset = 0.0
robot_x_coordinate_system = [] # define list for robot x-coordinates
robot_y_coordinate_system = [] # define list for robot y-coordintaes   
world_x_coordinate_system = [] # define list for world x-coordinates
world_y_coordinate_system = [] # define list for world y-coordintaes   
rollCoordinates = 2.994
pitchCoordinates = 1.527
yawCoordinates = -1.606


def retrieve_robot_coordinates():

    a = datetime.now()
    # Initialize empty variables
    pointTopLeftCorner = []
    pointTopRightCorner = []
    pointBottomRightCorner = []
    pointBottomLeftCorner = []

    # Pfad zum Home-Verzeichnis des Benutzers
    home_path = os.path.expanduser('~')

    project_path = os.path.join(home_path, 'robotDetectPick', 'robotcoordinates')

    # Read the contents of the text files
    # Open and read pointTopRightCorner.txt, read the robot coordinates of the top left corner
    with open(project_path + '/pointTopLeftCorner.txt', 'r') as file:
        # Read the lines from the file
        lines = file.readlines()
        # Extract the robot coordinates from the txtfile.
        for line in lines:
            # Convert the line to a float and add it to the pointTopLeftCorner list
            pointTopLeftCorner.append(float(line.strip()))

    # Repeat the process for the other variables and files
    # Open and read pointTopRightCorner.txt, read the robot coordinates of the bottom left corner
    with open(project_path + '/pointBottomLeftCorner.txt', 'r') as file:
        lines = file.readlines()
        # Extract the robot coordinates from the txtfile.
        for line in lines:
            pointBottomLeftCorner.append(float(line.strip()))

    # Open and read pointBottomRightCorner.txt, read the robot coordinates of the bottom right corner
    with open(project_path + '/pointBottomRightCorner.txt', 'r') as file:
        lines = file.readlines()
        # Extract the robot coordinates from the txtfile.
        for line in lines:
            pointBottomRightCorner.append(float(line.strip()))

    # Open and read pointBottomLeftCorner.txt, read the robot coordinates of the top right corner
    with open(project_path + '/pointTopRightCorner.txt', 'r') as file:
        lines = file.readlines()
        # Extract the robot coordinates from the txtfile.
        for line in lines:
            pointTopRightCorner.append(float(line.strip()))

    # Return the retrieved variables as a dictionary
    return {
        'pointTopLeftCorner': pointTopLeftCorner,
        'pointBottomLeftCorner': pointBottomLeftCorner,
        'pointBottomRightCorner': pointBottomRightCorner,
        'pointTopRightCorner': pointTopRightCorner,
        'a': a
    }



def store_coordinates():

    # Call the function to retrieve the robot coordinates
    robot_coordinates = retrieve_robot_coordinates()

    # Access the individual variables if needed
    pointTopLeftCorner = robot_coordinates['pointTopLeftCorner']
    pointBottomLeftCorner = robot_coordinates['pointBottomLeftCorner']
    pointBottomRightCorner = robot_coordinates['pointBottomRightCorner']
    pointTopRightCorner = robot_coordinates['pointTopRightCorner']
    a = robot_coordinates['a']

    # Points of coordinatesystem of robot
    x1w, y1w, z1w = pointTopLeftCorner[0], pointTopLeftCorner[1], pointTopLeftCorner[2]
    x2w, y2w, z2w = pointBottomLeftCorner[0], pointBottomLeftCorner[1], pointBottomLeftCorner[2]
    x3w, y3w, z3w = pointBottomRightCorner[0], pointBottomRightCorner[1], pointBottomRightCorner[2]
    x4w, y4w, z4w = pointTopRightCorner[0], pointTopRightCorner[1], pointTopRightCorner[2]
    robot_x_coordinate_system.append([x1w, x2w, x3w, x4w])
    robot_y_coordinate_system.append([y1w, y2w, y3w, y4w])

    # storing all z coordinates in an array
    zValues = [z1w, z2w, z3w, z4w]

    # average z-coordinate
    averageZValue =  sum(zValues)/len(zValues)

    # Points of the world coordinate system
    x1, y1, z1 = solvepnpfptest.world_coordinate_system[0][0], solvepnpfptest.world_coordinate_system[0][1], solvepnpfptest.world_coordinate_system[0][2]
    x2, y2, z2 = solvepnpfptest.world_coordinate_system[1][0], solvepnpfptest.world_coordinate_system[1][1], solvepnpfptest.world_coordinate_system[1][2]
    x3, y3, z3 = solvepnpfptest.world_coordinate_system[2][0], solvepnpfptest.world_coordinate_system[2][1], solvepnpfptest.world_coordinate_system[2][2]
    x4, y4, z4 = solvepnpfptest.world_coordinate_system[3][0], solvepnpfptest.world_coordinate_system[3][1], solvepnpfptest.world_coordinate_system[3][2]
    world_x_coordinate_system.append([x1,x2,x3,x4])
    world_y_coordinate_system.append([y1,y2,y3,y4])


    # Store the variables in a dictionary
    variables = {
        'pointTopLeftCorner': pointTopLeftCorner,
        'pointBottomLeftCorner': pointBottomLeftCorner,
        'pointBottomRightCorner': pointBottomRightCorner,
        'pointTopRightCorner': pointTopRightCorner,
        'x1w': x1w, 'y1w': y1w, 'z1w': z1w,
        'x2w': x2w, 'y2w': y2w, 'z2w': z2w,
        'x3w': x3w, 'y3w': y3w, 'z3w': z3w,
        'x4w': x4w, 'y4w': y4w, 'z4w': z4w,
        'averageZValue': averageZValue,
        'a': a,
        'x1': x1, 'y1': y1, 'z1': z1,
        'x2': x2, 'y2': y2, 'z2': z2,
        'x3': x3, 'y3': y3, 'z3': z3,
        'x4': x4, 'y4': y4, 'z4': z4
    }

    return variables

def check_class_object():
        
        if dt.allCoordinatesPerDetection != []:
            classOfObject = dt.allCoordinatesPerDetection[0][0]
            return classOfObject   


def check_y_world_coordinate():
        
        # Points of detected object in world coordinates
        oy1 = solvepnpfptest.oy1
        ox1 = solvepnpfptest.ox1

        # waiting till detected objects horizontal coordinate is passing the Y (horizontal) coordinate boundary
        while oy1 <= solvepnpfptest.yBoundary:
                classObject = check_class_object()
                oy1 = solvepnpfptest.oy1
                ox1 = solvepnpfptest.ox1
                
                time.sleep(0.0001)

        return oy1, ox1, classObject



def linear_interpolation(oy1, ox1, timeToPerfomAction): 

    allCoordinates = store_coordinates()
    x1 = allCoordinates['x1']
    x2 = allCoordinates['x2']
    x4w = allCoordinates['x4w']
    x2w = allCoordinates['x2w']
    y1 = allCoordinates['y1']
    y3 = allCoordinates['y3']
    y2w = allCoordinates['y2w']
    y4w = allCoordinates['y4w']
    averageZValue = allCoordinates['averageZValue']
    a = allCoordinates['a']


    # Linear interpolation: calculate vertical coordinate for pick and place
    x_interpolation_factor = (ox1 - x1) / (x2 - x1)
    x_pick_coordinates = x4w + x_interpolation_factor * (x2w - x4w)

    # Linear interpolation: calculate horizontal coordinate for pick and place
    b = datetime.now()
    timeToCalculate = (b-a).total_seconds()
    totalTime = timeToPick + timeToPerfomAction + timeToCalculate
    Y = oy1 + solvepnpfptest.averageSpeed * (totalTime)
    Y = Y - solvepnpfptest.yBoundary + speedOffset
    y_interpolation_factor = (Y - y1) / (y3 - y1)
    y_pick_coordinates = y2w + y_interpolation_factor * (y4w - y2w)

    return x_pick_coordinates, y_pick_coordinates, averageZValue, timeToCalculate



