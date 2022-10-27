#!/bin/bash

apt-get update -y
apt-get upgrade -y
apt-get install bc -y
apt-get install python3-pip -y
apt-get install wget -y


python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

pip3 install torch torchvision
pip3 install argparse pandas numpy scipy scikit-learn tqdm matplotlib 