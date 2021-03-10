# ArUco

Exploring potential applications of ArUco fiducial markers.

## Installation

### ArUco Installation

To get access to the ArUco fiducial markers in python/opencv:

```
pip install opencv-contrib-python
```

### OGRE Installation

OGRE is a 3D library that can be used in conjunction with ArUco to create augmented reality
applications.  There is an OVIS module in OpenCV that uses OGRE, but it is not in the
`opencv-contrib-python` installation by default.  So we will need to build from source.

The docker folder has Dockerfile examples for building OpenCV with OGRE support.

I have successfully run the [ovis demo](https://github.com/opencv/opencv_contrib/blob/master/modules/ovis/samples/ovis_demo.py)
by running

```
docker build -t cv_ovis -f docker/Dockerfile .
xhost +
docker run --rm -ti --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v $(pwd):/data cv_ovis /bin/bash
python3 ovis_demo.py
```

It is slow though, since it isn't running on GPU.

## Marker Preparation

Generate marker images with `generate_markers.py` or use the [MarkerPrinter](https://github.com/opencv/opencv_contrib/tree/master/modules/aruco/misc/pattern_generator)
which supports svg/pdf, but doesn't support as many dictionaries.

## Scripts

Some examples steps in order.

### Create the charuco board
```
python3 src/generate_charuco_board.py --width 16 --height 9 --output output/charuco_board_16x9_dict_4x4_100.png --dictionary DICT_4X4_100
```
Print the result for a later step.

### Create the ArUco markers
```
python3 src/generate_markers.py --output output/marker_ --dictionary DICT_4X4_50
```
Print the results for later steps.

### Calibrate with the charuco board
```
python3 src/charuco_calibrate.py --width 9 --height 16 --dictionary DICT_4X4_100 --feed data/charuco_calibration.mp4 --output output/charuco_calibration.npz
```
Use your own video with the printed dictionary if calibrating your own camera.

### Detect the markers
```
python3 src/aruco_example.py --dictionary DICT_4X4_50 --input data/4x4_50_markers.png --camera-matrix data/charuco_calibration.npz --output output/4x4_50_markers.png
```

### Show Sinbad in a still image without detecting markers
```
python3 src/aruco_ar_no_markers.py --input data/4x4_50_markers.png --camera-matrix data/charuco_calibration.npz
```

### Show Sinbad and detect markers
```
python3 src/aruco_ar_demo.py --input data/4x4_50_markers.png --marker-length=1 --camera-matrix data/charuco_calibration.npz --dictionary DICT_4X4_50
```

### Show Sinbad, detect markers, and save video
```
python3 src/aruco_ar_video_demo.py --input data/4x4_50_markers.png --marker-length=1 --camera-matrix data/charuco_calibration.npz --dictionary DICT_4X4_50 --output output/ar.mp4
```
