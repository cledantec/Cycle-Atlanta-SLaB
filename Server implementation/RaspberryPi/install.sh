#! /bin/bash

# run this script to install packages to Matrix+Pi
# for instructions on creating Matrix keys, visit https://matrix-io.github.io/matrix-documentation/ before running this script.

sudo apt-get install python python3 python-pip nodejs
sudo pip install flask
curl https://raw.githubusercontent.com/matrix-io/matrix-creator-quickstart/master/install.sh | sh
