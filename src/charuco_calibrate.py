#!/bin/env python

# from https://answers.opencv.org/question/98447/camera-calibration-using-charuco-and-python/
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Calibrate a camera with ArUco markers')
parser.add_argument('--feed', default="0", type=str, help='video to read')
parser.add_argument('--dictionary', default='DICT_ARUCO_ORIGINAL', choices=[x for x in dir(cv2.aruco) if x.startswith('DICT')], help='ArUco dictionary to generate markers for (default: %(default)s)') 
parser.add_argument('--width', default=3, type=int, help='width of the board in squares')
parser.add_argument('--height', default=3, type=int, help='height of the board in squares')
parser.add_argument('--output', default="charuco_calibration.npz", type=str, help='')

args = parser.parse_args()

dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, args.dictionary))

# Generate the dictionary something like this, or use the pattern generator helper scripts
board = cv2.aruco.CharucoBoard_create(args.height, args.width, .025, .0125, dictionary)
#board = cv2.aruco.CharucoBoard_create(3,3,.025,.0125,dictionary)
#img = board.draw((200*3,200*3))
#
##Dump the calibration board to a file
#cv2.imwrite('charuco.png',img)


#Start capturing images for calibration
cap = cv2.VideoCapture(args.feed)

allCorners = []
allIds = []
decimator = 0
for i in range(1000):

    ret,frame = cap.read()
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        break
    res = cv2.aruco.detectMarkers(gray, dictionary)

    if len(res[0])>0:
        res2 = cv2.aruco.interpolateCornersCharuco(res[0], res[1], gray, board)
        if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%3==0:
            allCorners.append(res2[1])
            allIds.append(res2[2])

        cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    decimator+=1

imsize = gray.shape

#Calibration fails for lots of reasons. Release the video if we do
try:
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(allCorners, allIds, board, imsize, None, None)
    np.savez(args.output, cameraMatrix=cameraMatrix, distCoeffs=distCoeffs)
    print(f'cameraMatrix {cameraMatrix} \ndistCoeffs {distCoeffs}')
except:
    cap.release()

cap.release()
cv2.destroyAllWindows()
