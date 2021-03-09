#!/usr/bin/env python3

# modified from https://github.com/opencv/opencv_contrib/blob/master/modules/ovis/samples/aruco_ar_demo.py

import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description='Create an AR example with a still image')
parser.add_argument('--input', default='data/input.jpg', type=str, help='path to the input image (default: %(default)s)')
parser.add_argument('--camera-matrix', default=None, type=str, help='path to the camera matrix and distortion coefficients, if None uses the default (default: %(default)s)')

args = parser.parse_args()

frame = cv2.imread(args.input)

# random calibration data. your mileage may vary.
imsize = (800, 600)
K = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)

# AR scene
cv2.ovis.addResourceLocation("packs/Sinbad.zip") # shipped with Ogre

win = cv2.ovis.createWindow("arucoAR", imsize, flags=0)
win.setBackground(frame)
win.setCameraIntrinsics(K, imsize)
win.createLightEntity("sun", (0, 0, 0))

# manually set entity position
t_pos = (5, 0, 25)
r_pos = (0, 0, np.pi)
win.createEntity("figure", "Sinbad.mesh", t_pos, r_pos)
win.updateEntityPose("figure", (0, 0, 0), (0, np.pi, 0))
win.updateEntityPose("figure", (0, 0, 0), (np.pi/16, 0, 0))

# actions that Sinbad can perform
actions = {
    0: "IdleBase",
    1: "IdleTop",
    2: "RunBase",
    3: "RunTop",
    4: "HandsClosed",
    5: "HandsRelaxed",
    6: "DrawSwords",
    7: "SliceVertical",
    8: "SliceHorizontal",
    9: "Dance",
    10: "JumpStart",
    11: "JumpLoop",
    12: "JumpEnd",
}
win.playEntityAnimation("figure", actions[9], True)

k = 0
while True:
    keypress = cv2.ovis.waitKey(1)
    #print(keypress)
    if keypress == 27:
        break
    #win.setEntityPose("figure", tvecs[idx].ravel(), rvecs[idx].ravel())

