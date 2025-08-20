#  Imports
import sys

# Linux
sys.path.append('/home/ali/bachelorarbeit/yolov5/detect.py')
sys.path.append('/home/ali/bachelorarbeit/robot/solvepnpfourpoint')
sys.path.append('/home/ali/bachelorarbeit/yolov5')
sys.path.append('/home/niryo/ali/bachelorarbeit/yolov5')




import SolvePNP as solvepnpfptest
import robotAndDetect as dt3DRobot
from threading import *

# With this library "threading", you can run both the object detection 
# and the execution of robot movements in parallel.

# Detect and SolvePNP and Robot3DMovement

class Robot(Thread):
    def run(self):
        dt3DRobot.robotMovement()

class Detect(Thread):
    def run(self):
        dt3DRobot.detectOuter()

class SolvePNP(Thread):
    def run(self):
        solvepnpfptest.solvepnpfp()

detect = Detect()
solvepnp = SolvePNP()
robot = Robot()

detect.start()
solvepnp.start()
robot.start()


