from workspace import *
from converter import *
from pyniryo import *



# Define RGB List
rgb = [0, 0, 0]

# Define rgb values for the detected objects
def convert_color(color):
    if (color == "GREEN" or color == "2" or color == "3"):
        rgb =  [0, 255, 0]
        return (rgb)
    if (color == "BLUE" or color == "0" or color == "1"):
        rgb =  [0, 0, 255]
        return (rgb)
    if (color == "RED" or color == "6" or color == "7"):
        rgb =  [255, 0, 0]
        return (rgb)

def showColor(robot, objectColor):
    if (objectColor.name == "RED" or objectColor.name == "BLUE" or objectColor.name == "GREEN"):
                if objectColor.name == "RED":
                    robot.led_ring_flashing(convert_color(objectColor.name), 1.5, 1, True)
                else:
                    robot.led_ring_flashing(convert_color(objectColor.name))



def showColor_Detect(robot, listClass, listCounter, correctorCounter):
    if (listClass[listCounter-correctorCounter] == "greencircle" 
        or listClass[listCounter-correctorCounter] == "bluecircle" 
        or listClass[listCounter-correctorCounter] == "redcircle" or 
        listClass[listCounter-correctorCounter] == "greensquare" or 
        listClass[listCounter-correctorCounter] == "bluesquare" or
          listClass[listCounter-correctorCounter] == "redsquare"):
                if listClass[listCounter-correctorCounter] == "RED":
                    robot.led_ring_flashing(convert_color(listClass, listCounter, correctorCounter), 
                                            1.5, 1, True)
                else:
                    robot.led_ring_flashing(convert_color(listClass, listCounter, correctorCounter))
                            

      