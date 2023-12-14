#!/bin/bash
echo "ENV SETUP..."
sudo apt update -y && sudo apt upgrade -y && sudo apt-get install python3-pip -y
sudo apt-get install -y libsm6 libxext6 libxrender-dev
sudo apt install libgl1-mesa-glx -y
sudo apt-get install curl -y
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
pip3 install open3d==0.15.2

echo "ENV_SETUP_DONE"