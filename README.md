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
