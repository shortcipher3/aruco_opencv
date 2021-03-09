#!/usr/bin/env python3

# python code running through the example provided here: https://github.com/opencv/opencv_contrib/blob/master/modules/aruco/tutorials/aruco_detection/aruco_detection.markdown

import cv2
import numpy as np

import argparse

parser = argparse.ArgumentParser(description='Run detection across a video')
parser.add_argument('--input', default='data/input.mp4', type=str, help='path to the input video')
parser.add_argument('--output', default='output/output.mp4', type=str, help='path to the output video')
parser.add_argument('--dictionary', default='DICT_4X4_50', choices=[x for x in dir(cv2.aruco) if x.startswith('DICT')], help='ArUco dictionary to generate markers for (default: %(default)s)')
parser.add_argument('--camera-matrix', default=None, type=str, help='path to the camera matrix and distortion coefficients, if None uses the default')

args = parser.parse_args()

dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, args.dictionary))

# initialize video
vc = cv2.VideoCapture(args.input)
if not vc.isOpened():
    print("Unable to open video")
    quit()
flag, frame = vc.read()
if not flag:
    print("No frame read")
    quit()

# video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
vw = cv2.VideoWriter(args.output, fourcc, vc.get(cv2.CAP_PROP_FPS), (frame.shape[1], frame.shape[0]))


# detection parameters
if args.camera_matrix is None:
    cameraMatrix = cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), frame.shape[:2], True)
    distCoeff = None
else:
    arr = np.load(args.camera_matrix)
    cameraMatrix = arr['cameraMatrix']
    distCoeff = arr['distCoeffs']

# detect and draw markers
detector_params = cv2.aruco.DetectorParameters_create()
#detector_params.minMarkerDistanceRate = 0.2
while flag:
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, dictionary=dictionary, parameters=detector_params, cameraMatrix=cameraMatrix, distCoeff=distCoeff)
    output = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # draw rejected markers
    for reject in rejected:
        pts = reject.reshape((-1,1,2)).astype(np.int32)
        cv2.polylines(output,[pts],True,(0,255,255))

    # estimate and draw marker pose
    rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, cameraMatrix, distCoeff)
    if ids is not None:
        for i in range(ids.shape[0]):
            output = cv2.aruco.drawAxis(output, cameraMatrix, distCoeff, rvecs[i, :], tvecs[i, :], 0.1)
    else:
        print("No markers found!")
        print(f"corners {corners} ids {ids} rejected {rejected}")
    vw.write(output)
    flag, frame = vc.read()

vw.release()
