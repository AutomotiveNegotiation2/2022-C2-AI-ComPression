#!/bin/bash

apt update -y && apt upgrade -y && apt-get install python3-pip -y
apt-get install -y libsm6 libxext6 libxrender-dev
apt install libgl1-mesa-glx -y
apt-get install curl -y


python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
pip3 install open3d==0.15.2

echo "ENV_SETUP_DONE"