#!/bin/bash
FILE=$1
BASE=${FILE##*/}
BASE=${BASE%.*}
JOINT=_
EXT=bstrap
OUTPUT=$2
MODEL_PATH=$3
echo "PREPROCESSING START!"
StartTime=$(date +%s.%N)
python3 run.py --file_name $FILE
EndTime=$(date +%s.%N)
diff=$( echo "scale=1;($EndTime - $StartTime)*1000" | bc -l) 
echo "PREPROCESSING TIME : $diff msec"

echo "PRETRAIND START!"
StartTime=$(date +%s.%N)
python3 train_bootstrap.py --file_name $BASE --epochs 4 --timesteps 64 --model_weights_path $MODEL_PATH --gpu 0
EndTime=$(date +%s.%N)
diff=$( echo "scale=1;($EndTime - $StartTime)*1000" | bc -l) 
echo "PRETRAINED TIME : $diff msec"


echo Using $MODEL_PATH for encoding
echo "ADAPTIVE COMPRESSION START!"
StartTime=$(date +%s.%N)
python3 compress_adaptive.py --file_name $BASE --bs 64 --timesteps 64 --output $OUTPUT  --model_weights_path $MODEL_PATH --gpu 0
EndTime=$(date +%s.%N)
diff=$( echo "scale=1;($EndTime - $StartTime)*1000" | bc -l) 	
echo "ADAPTIVE COMPRESSION TIME : $diff msec"


