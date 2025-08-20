# Import the required module for text 
# to speech conversion
from gtts import gTTS
  
# This module is imported so that we can 
# play the converted audio
import os

# import solvepnp folder and the scripts
home_path = os.path.expanduser('~')
# The text that you want to convert to audio
workspace = 'Create a new workspace. You will have 10 seconds for each corner.'
workspace2 = 'Please go to the top left corner of your workspace. '
workspace3 = 'Now you have to go clockwise to the next corner. '
point1 = 'Point 1 is finished!'
point2 = 'Point 2 is finished!'
point3 = 'Point 3 is finished!'
point4 = 'Point 4 is finished!'
allPoints = 'All Points are finished!'
unknownObject = 'unknown object detected! Please stop the conveyor and remove the object'
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
allInstructions = [workspace, workspace2, workspace3, point1, point2, point3, point4, allPoints, unknownObject]
allNames =['workspace', 'workspace2', 'workspace3', 'point1', 'point2', 'point3', 'point4', 'allPoints', 'unknownObject' ]
soundCounter = 0
nameCounter = 0
lengthOfSounds = len(allInstructions)
print(len(allInstructions))
print (nameCounter)
print (soundCounter)
print (allInstructions[0])

# Create all sounds
while soundCounter < lengthOfSounds:
    myobj = gTTS(text=allInstructions[soundCounter], lang=language, slow=False)
    soundCounter +=13 f
    # Saving the converted audio in a mpile named
    myobj.save(home_path + '/robotDetectPick/robot/sounds/'+allNames[nameCounter]+'.mp3')    
    # welcome 
    # myobj.save('./sounds/'+allNames[nameCounter]+'.mp3')
    # Playing the converted file
    #Linux
    os.system(home_path + '/robotDetectPick/robot/sounds/'+allNames[nameCounter]+'.mp3')
    #Windows
    # os.system('C:/ali/mycode/sounds/'+allNames[nameCounter]+'.mp3')
    nameCounter += 1



