#  Imports
from pyniryo import *


# Variables and Lists
dataList1 = []
dataList2 = []
dataList3 = []
dataList4 = []
counterWS = 0


# Function for generating a workspace without a graphical user interface (e.g. Niryo Studio).

def createWorkspace(robot, waitWorkspace, workspace_name):

    robot.move_pose(0.126, 0.0, 0.172, -0.255, 0.99, -0.025)
    robot.set_learning_mode(True)
    robot.led_ring_solid([165, 42, 42])
    robot.play_sound("workspace.mp3")
    robot.play_sound("workspace2.mp3")
    robot.wait(waitWorkspace)

    # Saving all the points in the workspace.
    # saving first point of the workspace
    dataList1 = robot.get_pose()
    print( "x: " + str(round(dataList1.x, 4)) + "  y: " + str(round(dataList1.y, 4)) +    "  z: "  +  str(round(dataList1.z, 4)))
    robot.play_sound("point1.mp3")
    robot.play_sound("workspace3.mp3")
    coordinatesPoint1 = [dataList1.x, dataList1.y, dataList1.z]
    robot.wait(waitWorkspace) 

    # saving second point of the workspace
    dataList2 = robot.get_pose()
    print( "x: " + str(round(dataList2.x, 4)) + "  y: " + str(round(dataList2.y, 4)) +    "  z: "  +  str(round(dataList2.z, 4)))
    robot.play_sound("point2.mp3")
    robot.play_sound("workspace3.mp3")
    coordinatesPoint2 = [dataList2.x, dataList2.y, dataList2.z]
    robot.wait(waitWorkspace)
	
    # saving third point of the workspace
    dataList3 = robot.get_pose()
    print( "x: " + str(round(dataList3.x, 4)) + "  y: " + str(round(dataList3.y, 4)) +    "  z: "  +  str(round(dataList3.z, 4)))
    robot.play_sound("point3.mp3")
    robot.play_sound("workspace3.mp3") 
    coordinatesPoint3 = [dataList3.x, dataList3.y, dataList3.z]
    robot.wait(waitWorkspace)
	
    # saving fourth point of the workspace
    dataList4 = robot.get_pose()
    print( "x: " + str(round(dataList4.x, 4)) + "  y: " + str(round(dataList4.y, 4)) +    "  z: "  +  str(round(dataList4.z, 4)))
    robot.play_sound("point4.mp3")
    robot.play_sound("allPoints.mp3") 
    coordinatesPoint4 = [dataList4.x, dataList4.y, dataList4.z]

    # store coordinates of points in lists
    pointTopLeftCorner = [dataList1.x, dataList1.y, dataList1.z, dataList1.roll, dataList1.pitch, dataList1.yaw]
    pointBottomLeftCorner = [dataList2.x, dataList2.y, dataList2.z, dataList2.roll, dataList2.pitch, dataList2.yaw]
    pointBottomRightCorner = [dataList3.x, dataList3.y, dataList3.z, dataList3.roll, dataList3.pitch, dataList3.yaw]
    pointTopRightCorner = [dataList4.x, dataList4.y, dataList4.z, dataList4.roll, dataList4.pitch, dataList4.yaw]


    
    # import solvepnp folder and the scripts
    home_path = os.path.expanduser('~')
    
    # Open the file in write mode
    with open(home_path + '/robotDetectPick/robotcoordinates/pointTopLeftCorner.txt', 'w') as file:
        # Write the variable values to the file
        for number in pointTopLeftCorner:
            file.write(str(number) + '\n')
                # Open the file in write mode
    with open(home_path + '/robotDetectPick/robotcoordinates/pointBottomLeftCorner.txt', 'w') as file:
        # Write the variable values to the file
        for number in pointBottomLeftCorner:
            file.write(str(number) + '\n')

    # Open the file in write mode
    with open(home_path + '/robotDetectPick/robotcoordinates/pointBottomRightCorner.txt', 'w') as file:
        # Write the variable values to the file
        for number in pointBottomRightCorner:
            file.write(str(number) + '\n')

    # Open the file in write mode
    with open(home_path + '/robotDetectPick/robotcoordinates/pointTopRightCorner.txt', 'w') as file:
        # Write the variable values to the file
        for number in pointTopRightCorner:
            file.write(str(number) + '\n')

    print("Variable has been stored in the file.")



    workspaceListLength = len(robot.get_workspace_list())
    print("All Workspace available: ")
    print(len(robot.get_workspace_list()))
    workspaceCounter = 0
    print(robot.get_workspace_list())
    while workspaceCounter < workspaceListLength-1:
        print("Workspace Counter = " + str(workspaceCounter) + " | Workspace Name: " + str(robot.get_workspace_list()[workspaceCounter]))
        if robot.get_workspace_list()[workspaceCounter] == workspace_name:
                  robot.delete_workspace(workspace_name)
        workspaceCounter += 1

    # save the workspace with the coordinates
    robot.save_workspace_from_robot_poses(workspace_name, dataList1, dataList2, dataList3, dataList4)



# While a script is running, this function can be utilized to switch the tool.
def changeTool(robot):
    toolStatus = False
    while toolStatus == False:
            robot.led_ring_solid([190, 190, 190])
            robot.update_tool
            print("Current Tool ID " + str(robot.get_current_tool_id().value))
            if robot.get_current_tool_id().value != 0:
                  toolStatus = True
            robot.set_learning_mode(True)
    robot.set_learning_mode(True)