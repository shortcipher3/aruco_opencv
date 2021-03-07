#!/bin/env python

# from https://answers.opencv.org/question/98447/camera-calibration-using-charuco-and-python/
import cv2
import argparse

parser = argparse.ArgumentParser(description='Calibrate a camera with ArUco markers')
parser.add_argument('--width', default=3, type=int, help='width of the board in squares')
parser.add_argument('--height', default=3, type=int, help='height of the board in squares')
parser.add_argument('--output', default='charuco.png', type=str, help='path to the output image')
parser.add_argument('--dictionary', default='DICT_ARUCO_ORIGINAL', choices=[x for x in dir(cv2.aruco) if x.startswith('DICT')], help='ArUco dictionary to generate markers for (default: %(default)s)') 

args = parser.parse_args()

dictionary = cv2.aruco.Dictionary_get(getattr(cv2.aruco, args.dictionary))

# Generate the dictionary something like this, or use the pattern generator helper scripts
board = cv2.aruco.CharucoBoard_create(args.height, args.width, .025, .0125, dictionary)
img = board.draw((200*args.height, 200*args.width))

#Dump the calibration board to a file
cv2.imwrite(args.output, img)
