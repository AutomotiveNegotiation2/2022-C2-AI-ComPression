#!/bin/bash
FILE=$1
BASE=${FILE##*/}
BASE=${BASE%.*}
MODEL_PATH=$2
hdim1=$3
hdim2=$4
n_layers=$5
batch_size=$6
emb_size=$7
epoch=$8
python3 train_bootstrap.py --file_name $BASE --epochs $epoch --timesteps 64 --model_weights_path $MODEL_PATH --gpu 0 --hdim1 $hdim1 --hdim2 $hdim2 --n_layers $n_layers --batch_size $batch_size --emb_size $emb_size


