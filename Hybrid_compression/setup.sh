#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install bc -y
sudo apt-get install python3-pip -y
sudo apt-get install wget -y

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

pip3 install torch torchvision
pip3 install argparse pandas numpy scipy scikit-learn tqdm