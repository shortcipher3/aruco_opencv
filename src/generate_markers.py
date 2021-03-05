#!/usr/bin/env python3

import cv2
import argparse

parser = argparse.ArgumentParser(description='Generate ArUco marker images in png format')
parser.add_argument('--size', default=400, type=int, help='size in pixels of the side length of the marker')
parser.add_argument('--output-prefix', default='marker', type=str, help='prefix to store the generated markers at')
parser.add_argument('--dictionary', default='DICT_ARUCO_ORIGINAL', choices=[x for x in dir(cv2.aruco) if x.startswith('DICT')], help='ArUco dictionary to generate markers for (default: %(default)s)')

args = parser.parse_args()

adict = cv2.aruco.Dictionary_get(getattr(cv2.aruco, args.dictionary))

index = 0
while True:
    try:
        marker_img = adict.drawMarker(index, args.size)
    except:
        break
    cv2.imwrite(f'{args.output_prefix}_{index:04d}.png', marker_img)
    index = index + 1



