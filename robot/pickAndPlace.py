#  Imports
from workspace import *
from converter import *
from color import *
from pyniryo import *
from coordinates import *
import time
from datetime import datetime

def pickAndPlace(conveyor_id, robot, xCoordinates, yCoordinates, 
			 zCoordinates, rollCoordinates, pitchCoordinates, 
			 yawCoordinates, place_upGreen, place_downGreen, place_upBlue, place_downBlue, classOfObject):
			 
				# picking object
						a = datetime.now()
						robot.led_ring_solid([0, 0, 0])
						c = datetime.now()
						robot.pick_from_pose(xCoordinates, yCoordinates, zCoordinates, 
											rollCoordinates, pitchCoordinates , yawCoordinates)
						b = datetime.now()
						timeToPick = (b-a).total_seconds()
						d = datetime.now()
						timeToPick = (d-c).total_seconds()
						#current pose ausgeben lassen
						if (classOfObject == "2" or classOfObject == "3"):
							print("Bringing green object to his position")
							#travel to drop pos
							pos = (convert_data(place_upGreen))
							robot.move_pose(pos)
							time.sleep(1)
					
							#drop the object
							pos = (convert_data(place_downGreen))
							robot.move_pose(pos)
							time.sleep(1)
							robot.release_with_tool()

						if (classOfObject == "0" or classOfObject == "1"):
							print("Bringing blue object to his position")
							#travel to drop pos
							pos = (convert_data(place_upBlue))
							robot.move_pose(pos)
							time.sleep(1)
					
							#drop the object
							pos = (convert_data(place_downBlue))
							robot.move_pose(pos)
							time.sleep(1)
							robot.release_with_tool()
						robot.move_pose(observation_pose)


