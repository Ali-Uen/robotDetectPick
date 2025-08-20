# importing required libraries
import numpy as np
import cv2 as cv
import glob


# find chessboard corners - object points and image points


# chessboard has 9 squares in the horizontal direction and 6 squares in the vertical direction
chessboardSize = (9,6)

# image resolution: width of 640 pixel and a height of 480 pixels
frameSize = (640,480)



# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# 3d coordinates of the chessboard corners
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)

# reshape the coordinates
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

# scaling object points, each size of chessboard square in millimeters
size_of_chessboard_squares_mm = 25
objp = objp * size_of_chessboard_squares_mm

# create empty lists 
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# retrieve a list of image file paths that match the filename pattern, store in images 
images = glob.glob('/home/niryo/ali/bachelorarbeit/robot/images/*.jpg')

# Iterating over images
for image in images:

    # reading the image and converting to grayscale
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # finding chessboard corners with opencv function 
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        
        # drawing and displaying the chessboard corners to the user
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        print(img)
        k = cv.waitKey(0) & 0xFF
        if k == ord('s'):
            cv.imwrite('pose'+image, img)

# clean up, destroy all OpenCV windows
cv.destroyAllWindows()

# Camera Calibration
# perform the camera calibration and store the parameters in their variables
ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)


# print the results
print()
print("Cameria calibrated ", ret)
print("\nCamera Matrix:\n", cameraMatrix)
print("\nDistortion Parameters:\n", dist)
print("\nRotation Vectors:\n", rvecs)
print("\nTranslation Vectors:\n", tvecs)

# saving calibration parameters
calib_data_path = '/home/niryo/ali/bachelorarbeit/robot/results'
np.savez(
    f"{calib_data_path}/CameraParams",
    cameraMatrix=cameraMatrix,
    dist=dist,
    rvecs=rvecs,
    tvecs=tvecs,
)

# Undistortion of an image
img = cv.imread('/home/niryo/ali/bachelorarbeit/robot/images/my_photo-1.jpg')
h,  w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# Undistort using camera calibration parameters
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('/home/niryo/ali/bachelorarbeit/robot/results/caliResult1.png', dst)

# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('/home/niryo/ali/bachelorarbeit/robot/results/caliResult3.png', dst)


# calculate the mean error, divided by the number of calibration
# images to obtain the average error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )






