#!/usr/bin/env python3

# python code running through the example provided here: https://github.com/opencv/opencv_contrib/blob/master/modules/aruco/tutorials/aruco_detection/aruco_detection.markdown

import cv2
import numpy as np

adict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)


img = cv2.imread('data/singlemarkersoriginal.jpg')
corners, ids, rejected = cv2.aruco.detectMarkers(img, adict)
#corners, ids, rejected = cv2.aruco.detectMarkers(img, adict, camera_matrix, dist_coef)
corners, ids = cv2.aruco.detectMarkers(img, adict)[:2]
output = cv2.aruco.drawDetectedMarkers(img, corners, ids)

for reject in rejected:
    pts = reject.reshape((-1,1,2)).astype(np.int32)
    cv2.polylines(output,[pts],True,(0,255,255))

cameraMatrix = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), img.shape[:2], True)
rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, cameraMatrix, None)
#cv2.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs[, rvecs[, tvecs[, _objPoints]]]) -> rvecs, tvecs, _objPoints
for i in range(ids.shape[0]):
    output = cv2.aruco.drawAxis(output, cameraMatrix, None, rvecs[i, :], tvecs[i, :], 0.1)
    #cv2.drawAxis(image, cameraMatrix, distCoeffs, rvec, tvec, length) -> image
cv2.imwrite('output/singlemarkersoutput.jpg', output)
