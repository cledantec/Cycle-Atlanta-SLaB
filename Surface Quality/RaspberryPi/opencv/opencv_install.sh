sudo aptitude -y install build-essential git cmake pkg-config
sudo aptitude -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo aptitude -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo aptitude -y install libxvidcore-dev libx264-dev
sudo aptitude -y install libgtk2.0-dev libatlas-base-dev gfortran

wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.0.0.zip
unzip opencv_contrib.zip

sudo pip install virtualenv virtualenvwrapper
sudo pip3 install virtualenv virtualenvwrapper
sudo pip install numpy
sudo pip3 install numpy

cd ~/opencv-3.0.0/
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.0.0/modules \
	-D BUILD_EXAMPLES=ON ..

sudo make
sudo make install
sudo ldconfig

cd /usr/local/lib/python3.4/site-packages/
sudo mv cv2.cpython-34m.so cv2.so
