#!/bin/bash

apt-get update -y
apt-get upgrade -y
apt-get install bc -y
apt-get install python3-pip -y
apt-get install wget -y
apt-get install python3-tk -y
apt-get install curl -y

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

pip install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
pip3 install argparse pandas numpy scipy scikit-learn tqdm matplotlib 