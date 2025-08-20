# You can stop the Conveyor Belt

#  Imports
from pyniryo import *

workspace_name = "aliconv2"  # Robot's Workspace Name
robot_ip_address = "192.168.0.228"

# - Initialization
# Connect to robot
robot = NiryoRobot(robot_ip_address)
# Calibrate robot if the robot needs calibration        
robot.calibrate_auto()

# stop conveyor belt
conveyor_id = robot.set_conveyor()
robot.stop_conveyor(conveyor_id)
