#!/usr/bin/env python3

# modified from https://github.com/opencv/opencv_contrib/blob/master/modules/ovis/samples/aruco_ar_demo.py

import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description='Save an AR example as a video')
parser.add_argument('--input', default='data/input.mp4', type=str, help='path to the input video (default: %(default)s)')
parser.add_argument('--output', default='output/output.mp4', type=str, help='path to the output video (default: %(default)s)')
parser.add_argument('--dictionary', default='DICT_4X4_50', choices=[x for x in dir(cv2.aruco) if x.startswith('DICT')], help='ArUco dictionary to generate markers for (default: %(default)s)')
parser.add_argument('--camera-matrix', default=None, type=str, help='path to the camera matrix and distortion coefficients, if None uses the default (default: %(default)s)')
parser.add_argument('--marker-length', default=5, type=float, help="the length of the marker's side in meters (default: %(default)s)")

args = parser.parse_args()

dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, args.dictionary))

frame = cv2.imread(args.input)

# random calibration data. your mileage may vary.
imsize = (1664, 1664)#frame.shape[:2]
K = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)

# AR scene
cv2.ovis.addResourceLocation("packs/Sinbad.zip") # shipped with Ogre

win = cv2.ovis.createWindow("arucoAR", imsize, flags=0)
win.setCameraIntrinsics(K, imsize)
win.createEntity("figure", "Sinbad.mesh", (0, 0, 5), (1.57, 2.50, 0))
win.createLightEntity("sun", (0, 0, 100))

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

# video capture
#cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, imsize[0])
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imsize[1])

# video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#vw = cv2.VideoWriter(args.output, fourcc, 15, (frame.shape[1], frame.shape[0]))
vw = cv2.VideoWriter(args.output, fourcc, 15, (1016, 1016))

k = 0
while cv2.ovis.waitKey(1) != 27:
    #img = cap.read()[1]
    win.setBackground(frame)
    corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary)

    cv2.waitKey(1)

    if ids is None:
        continue

    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(corners, args.marker_length, K, None)[:2]
    win.setCameraPose(tvecs[0].ravel(), rvecs[0].ravel(), invert=True)
    rendered_frame = win.getScreenshot()
    print(frame.shape)
    print(rendered_frame.shape)
    vw.write(rendered_frame)
    cv2.imwrite(args.output+'.png', rendered_frame)
    k = k + 1
    if k > 100:
        break
vw.release()

