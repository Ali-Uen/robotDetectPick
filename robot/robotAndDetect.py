#  Imports
from workspace import *
from converter import *
from color import *
from pickAndPlace import *
from coordinates import *
from pyniryo import *
import sys
from datetime import datetime
import pandas as pd
import evaluation as eval
import os

# import solvepnp folder and the scripts
home_path = os.path.expanduser('~')
project_path = os.path.join(home_path, 'robotDetectPick', 'solvepnp')
sys.path.append(project_path)
import SolvePNP as solvepnpfptest

# import yolov5 folder and the scripts
project_path = os.path.join(home_path, 'robotDetectPick', 'yolov5')
sys.path.append(project_path)

# Constants
global contiunueFlag
global handFlag
global listClass
contiunueFlag = False
handFlag = False


# webcam stream detecting 
def detectOuter():
        def detectInner():
                import detect as dt
                print()
                print("Execute Detection:")
                while contiunueFlag == False:
                        dt.run()
                        handFlag = True
                        time.sleep(2)
                        
                        
        detectInner()


# execute pick and place with object detection
def robotMovement():

        # Stop the conveyor belt 
        import subprocess
        subprocess.call('python3' + home_path + '/robotDetectPick/robot/stopConveyor.py', shell=True)
        workspace_name = "aliconv"  # Robot's Workspace Name
        waitWorkspace = 1
        flagWorkspace = 'no'   # Type "Yes", if you want to create a new workspace
        robot_ip_address = "192.168.0.228" # Put the IP Adress of the robot in this
        n_xy_pickCoordinatesFlag = False
        speedofConveyor = 50  # (procent)
        classOfObject = -1
        collectedObjectsCounter = 0 
        counter = 0
        emptyFlag = True
        # Connect to robot
        robot = NiryoRobot(robot_ip_address)
        # Calibrate robot if the robot needs calibration        
        print("Need Calibration?") 
        if robot.need_calibration == True:
                                print("Yes")
        if robot.need_calibration == False:
                print("No")
        # do calibration if needed
        robot.calibrate_auto()
        # Updating tool
        robot.update_tool()
        # set id of conveyor belt and start it
        conveyor_id = robot.set_conveyor()
        robot.run_conveyor(conveyor_id, speed=speedofConveyor, direction=ConveyorDirection.BACKWARD)
        # show current tool ID
        print("Current Tool ID (WS): " + str(robot.get_current_tool_id().value))
        currentToolID = robot.get_current_tool_id().value
        # create a workspace
        if flagWorkspace == 'yes':
                robot.led_ring_solid([165, 42, 42])
                createWorkspace(robot, waitWorkspace, workspace_name)
                print("Workspace " + str(workspace_name) + " saved! ")
                workspace_name = "aliconv"
                print("Workspace is finished, change the Tool fast.")
                # switch tool of robot with "changeTool"
                # changeTool(robot)
                robot.set_learning_mode(False)
                robot.led_ring_solid([165, 42, 42])
        # Moving to observation pose
        pos = (convert_data(obs))
        robot.move_pose(observation_pose)
        # show start color (white)
        robot.led_ring_solid([255, 255, 255])
        robot.release_with_tool()
        # wait for object detection and calculating the world coordinates
        time.sleep (5)
        # store world coordinates of first detected object
        oy1, ox1, classOfObject = check_y_world_coordinate()
        a = datetime.now()
        import detect as dt
        # 
        while contiunueFlag == False:
                        # checking again the y boundary coordinate, for n-objects.
                        if n_xy_pickCoordinatesFlag == True:
                                classOfObject = check_class_object()
                                # store world coordinate of n detected objects                         
                                oy1, ox1, classOfObject = check_y_world_coordinate()
                                a = datetime.now()
                        # When the object detection algorithm detects a green object, 
                        # display the detected object highlighted in green color.
                        if (classOfObject == "2" or classOfObject == "3"):
                                robot.led_ring_solid(convert_color(classOfObject))
                        # When the object detection algorithm detects a green object, 
                        # display the detected object highlighted in blue color.
                        if (classOfObject == "0" or classOfObject  == "1"):
                                robot.led_ring_solid(convert_color(classOfObject))
                        # When the object detection algorithm detects a green object, 
                        # display the detected object highlighted in red color.
                        # In addition to that, stop the conveyor and generate an error
                        if (classOfObject == "6" or classOfObject == "7"):
                                robot.led_ring_flashing(convert_color(classOfObject))
                                robot.play_sound("unknownObject.mp3")
                                robot.stop_conveyor(conveyor_id)
                                robot.unset_conveyor(conveyor_id)
                                sys.exit("Unknown Object Detected")
                        b = datetime.now()
                        timeToPerfomAction = (b-a).total_seconds()
                        x_pick_coordinates, y_pick_coordinates, averageZValue, timeToCalculate = linear_interpolation(oy1, ox1, timeToPerfomAction)
                        z_pick_coordinates = averageZValue + 0.055
                        pickAndPlace(conveyor_id, robot, x_pick_coordinates, y_pick_coordinates
                                        , z_pick_coordinates, rollCoordinates, pitchCoordinates, yawCoordinates, 
                                        place_upGreen, place_downGreen, place_upBlue, place_downBlue, classOfObject)
                        n_xy_pickCoordinatesFlag = True
                        counter += 1


                        # Saving results to an excel table for evaluation
                        eval.excel(classOfObject, solvepnpfptest.averageTime, solvepnpfptest.averageDistance, solvepnpfptest.averageSpeed, 
                                   ox1, oy1, speedofConveyor, timeToPick, x_pick_coordinates, y_pick_coordinates, timeToPerfomAction, 
                                   robot_x_coordinate_system, robot_y_coordinate_system, world_x_coordinate_system,
                                        world_y_coordinate_system, averageZValue, timeToCalculate)


                        solvepnpfptest.oy1 = 0.0 
                        solvepnpfptest.ox1 = 0.0
                        collectedObjectsCounter += 1
                        time.sleep(0.0001)

        robot.stop_conveyor(conveyor_id)
        robot.unset_conveyor(conveyor_id)
        
        # Terminate the connection to robot (NED 2).
        robot.close_connection()
