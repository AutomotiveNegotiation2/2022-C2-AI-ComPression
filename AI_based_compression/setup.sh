#!/bin/bash
echo "AI _setup ..."
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install bc -y
sudo apt-get install python3-pip -y
sudo apt-get install wget -y

pip3 install torch torchvision
pip3 install argparse pandas numpy scipy scikit-learn tqdm

echo "AI setup done"