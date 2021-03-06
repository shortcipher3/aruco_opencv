FROM ubuntu:20.04
ENV WORKSPACE=/workspace

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  apt-utils \
  build-essential \
  ca-certificates \
  checkinstall \
  cmake \
  git \
  gphoto2 \
  graphviz \
  gstreamer1.0-libav \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-base-apps \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-ugly \
  gstreamer1.0-tools \
  libavcodec-dev \
  libavdevice-dev \
  libavfilter-dev \
  libavformat-dev \
  libavresample-dev \
  libavutil-dev \
  libcanberra-gtk-module \
  libdc1394-22-dev \
  libfreetype6-dev \
  libgphoto2-dev \
  libgstreamer1.0 \
  libgstreamer1.0-dev \
  libgstreamer-plugins-bad1.0-0 \
  libgstreamer-plugins-base1.0-0 \
  libgstreamer-plugins-base1.0-dev \
  libgstreamer-plugins-good1.0-0 \
  libgstrtspserver-1.0 \
  libgstrtspserver-1.0-dev \
  libgtk2.0-dev \
  libjpeg-dev \
  liblapack-dev \ 
  libmp3lame-dev \
  libogre-1.12 \
  libogre-1.12-dev \
  libopenblas-dev \
  libopencore-amrnb-dev \
  libopencore-amrwb-dev \
  libswscale-dev \
  libswscale-dev \
  libtbb-dev \
  libtheora-dev \
  libtiff5-dev \
  libv4l-dev \
  libvorbis-dev \
  libxine2-dev \
  libxml2 \
  libxml2-dev \
  libxslt1-dev \
  libxvidcore-dev \
  pkg-config \
  python3 \
  python3-dev \
  python3-gst-1.0 \
  python3-numpy \
  python3-pip \
  python3-pyqt5 \
  python3-setuptools \
  ubuntu-restricted-extras \
  unzip \
  v4l-utils \
  vim \
  wget \
  x264 \
  yasm \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
  Cython \
  Pillow \
  RISE \
  av \
  bokeh \
  easydict \
  flask \
  hickle \
  imageio \
  jupyter \
  jupyterlab \
  lxml \
  matplotlib \
  moviepy \
  pandas \
  pims \
  pymongo \
  pyyaml \
  scikit-image \
  scipy \
  six \
  sk-video \
  sklearn \
  tensorboard \
  tensorflow \
  werkzeug

RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension && \
  jupyter-nbextension install rise --py --sys-prefix && \
  jupyter-nbextension enable rise --py --sys-prefix && \
  jupyter serverextension enable --py jupyterlab --sys-prefix
ARG OPENCV_ROOT=/opt/opencv
ARG CONTRIB_ROOT=/opt/opencv_contrib
ARG OGRE_DIR=/usr/share/OGRE/cmake/modules/

RUN touch /usr/lib/x86_64-linux-gnu/libOgreGLSupport.a \
  && git clone --depth 1 https://github.com/opencv/opencv.git $OPENCV_ROOT \
  && git clone --depth 1 https://github.com/opencv/opencv_contrib.git $CONTRIB_ROOT \
  && mkdir $OPENCV_ROOT/build \
  && cd $OPENCV_ROOT/build \
  && cmake \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH="$CONTRIB_ROOT/modules" \
  -D PYTHON2_EXECUTABLE="/usr/bin/python3.8" \
  -D PYTHON_INCLUDE_DIR="/usr/include/python3.8" \
  -D PYTHON_INCLUDE_DIR2="/usr/include/x86_64-linux-gnu/python3.8" \
  -D PYTHON_LIBRARY="/usr/lib/x86_64-linux-gnu/libpython3.8.so" \
  -D PYTHON3_NUMPY_INCLUDE_DIRS="/usr/local/lib/python3.8/dist-packages/numpy/core/include/" \
  -D BUILD_DOCS=OFF \
  -D BUILD_EXAMPLES=OFF \
  -D BUILD_opencv_ovis=ON \
  -D WITH_EIGEN=ON \
  -D WITH_GPHOTO2=ON \
  -D WITH_GSTREAMER=ON \
  -D WITH_LAPACK=ON \
  -D WITH_TBB=ON \
  $OPENCV_ROOT/build $OPENCV_ROOT \
  && make -j"$(nproc)" \
  && make install \
  && rm -rf $OPENCV_ROOT \
  && rm -rf $CONTRIB_ROOT

# ENVIRONMENT SETUP
RUN mkdir $WORKSPACE \
  && ln -s /usr/lib/x86_64-linux-gnu/OGRE-1.12/ /usr/lib/x86_64-linux-gnu/OGRE \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/cubemap.zip  -O /usr/share/OGRE/Media/packs/cubemap.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/cubemapsJS.zip -O /usr/share/OGRE/Media/packs/cubemapsJS.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/dragon.zip -O /usr/share/OGRE/Media/packs/dragon.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/fresneldemo.zip -O /usr/share/OGRE/Media/packs/fresneldemo.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/ogretestmap.zip -O /usr/share/OGRE/Media/packs/ogretestmap.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/ogredance.zip -O /usr/share/OGRE/Media/packs/ogredance.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/skybox.zip -O /usr/share/OGRE/Media/packs/skybox.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/Sinbad.zip -O /usr/share/OGRE/Media/packs/Sinbad.zip \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/packs/DamagedHelmet.zip -O /usr/share/OGRE/Media/packs/DamagedHelmet.zip \
  && mkdir -p /usr/share/OGRE/Media/volumeTerrain/ \
  && wget https://github.com/OGRECave/ogre/raw/master/Samples/Media/volumeTerrain/volumeTerrainBig.zip -O /usr/share/OGRE/Media/volumeTerrain/volumeTerrainBig.zip
WORKDIR $WORKSPACE

